import pulsekit
import time
import typing
import shapely as sp
from .agent import Agent, AgentState
from .visibility import Visibility


class Model(object):

    def __init__(self,
                 arena,
                 occlusions,
                 real_time: bool = False,
                 time_step: float = 0.1):
        self.arena = arena
        self.occlusions = occlusions
        self.real_time = real_time
        self.time_step = time_step
        self.agents: typing.Dict[str, Agent] = {}
        self.visibility = Visibility(arena=self.arena, occlusions=self.occlusions)
        self.last_step = None
        self.time = 0
        self.running = False
        self.episode_count = 0
        self.step_count = 0
        self.before_step = None
        self.after_step = None
        self.before_stop = None
        self.after_stop = None
        self.before_reset = None
        self.after_reset = None
        self.on_close = None
        self.view: typing.Optional["View"] = None
        self.paused = False

    def set_agents_state(self, agents_state: typing.Dict[str, AgentState],
                         delta_t: float = 0):
        for agent_name, agent_state in agents_state.items():
            if agent_name in self.agents:
                self.agents[agent_name].set_state(agent_state)
        self.__update_state__(delta_t)

    def __update_state__(self,
                         delta_t: float = 0):
        pass

    def pause(self):
        self.paused = not self.paused

    def add_agent(self, name: str, agent: Agent):
        self.agents[name] = agent
        agent.name = name
        agent.model = self

    def reset(self):
        if self.running:
            self.stop()
        if self.before_reset is not None:
            self.before_reset()
        self.running = True
        self.episode_count += 1
        for name, agent in self.agents.items():
            agent.reset()
        observations = self.get_observations()
        for name, agent in self.agents.items():
            agent.start()
        self.last_step = time.time()
        self.step_count = 0
        if self.after_reset is not None:
            self.after_reset()

    def stop(self):
        if not self.running:
            return
        if self.before_stop is not None:
            self.before_stop()
        self.running = False
        if self.after_stop is not None:
            self.after_stop()

    def is_valid_state(self, agent_polygon: sp.Polygon, collisions: bool) -> bool:
        if not self.arena.contains(agent_polygon):
            return False
        if collisions:
            for occlusion in self.occlusions:
                if agent_polygon.intersects(occlusion):
                    return False
        return True

    def get_observations(self):
        agent_visibility = {src_name: {dst_name: None for dst_name in self.agents} for src_name in self.agents}
        observations = {}
        for src_name, src_agent in self.agents.items():
            observations[src_name] = {}
            for dst_name, dst_agent in self.agents.items():
                if agent_visibility[src_name][dst_name] is None:
                    if src_name == dst_name:
                        is_visible = True
                    else:
                        is_visible = self.visibility.line_of_sight(src=src_agent.state.location,
                                                                   dst=dst_agent.state.location)
                    agent_visibility[src_name][dst_name] = is_visible
                    agent_visibility[dst_name][src_name] = is_visible
            observations[src_name]["agent_states"] = {}
            for dst_name, is_visible in agent_visibility.items():
                if is_visible:
                    observations[src_name]["agent_states"][dst_name] = self.agents[dst_name].state.location, self.agents[dst_name].state.direction
                else:
                    observations[src_name]["agent_states"][dst_name] = None
        return observations

    def get_observation(self,
                        agent_name: str,
                        polygonal: bool = False) -> dict:
        observation = {}
        src_point = sp.Point(self.agents[agent_name].state.location)
        if polygonal:
            visibility_polygon = self.visibility.get_visibility_polygon(src_point.state.location, src_point.state.direction)
        else:
            walls_by_distance = self.visibility.walls_by_distance(src=src_point)
        parsed_walls = []
        for wall_number, vertices, distance in walls_by_distance:
            parsed_walls.append((distance, self.wall_direction(src=src_point, wall_number=wall_number)))
        observation["walls"] = parsed_walls
        observation["agent_states"] = {}
        for dst_name, dst_agent in self.agents.items():
            if agent_name == dst_name:
                is_visible = True
            else:
                dst_point = sp.Point(dst_agent.state.location)
                if polygonal:
                    dst_polygon = dst_agent.get_polygon()
                    is_visible = dst_polygon.intersects(visibility_polygon)
                else:
                    is_visible = self.visibility.line_of_sight(src=src_point,
                                                               dst=dst_point,
                                                               walls_by_distance=walls_by_distance)
            if is_visible:
                observation["agent_states"][dst_name] = self.agents[dst_name].state.location, self.agents[dst_name].state.direction
            else:
                observation["agent_states"][dst_name] = None
        return observation

    def step(self) -> float:
        if not self.running:
            return 0

        if self.paused:
            return 0

        with pulsekit.CodeBlock("model.before_step"):
            if self.before_step is not None:
                self.before_step()

        with pulsekit.CodeBlock("model.real_time_wait"):
            if self.real_time:
                while self.last_step + self.time_step > time.time():
                    pass

        with pulsekit.CodeBlock("model.step"):
            self.last_step = time.time()
            with pulsekit.CodeBlock("update_agents_state"):
                for name, agent in self.agents.items():
                    dynamics = agent.dynamics
                    distance, rotation = dynamics.change(delta_t=self.time_step)
                    new_state = agent.state.update(rotation=rotation,
                                                   distance=distance)
                    agent_polygon = agent.get_polygon(state=new_state)
                    if self.is_valid_state(agent_polygon=agent_polygon,
                                           collisions=agent.collision):
                        agent.set_state(state=new_state)
                    else: #try only rotation
                        new_state = agent.state.update(rotation=rotation,
                                                       distance=0)
                        agent_polygon = agent.get_polygon(state=new_state)
                        if self.is_valid_state(agent_polygon=agent_polygon,
                                               collisions=agent.collision):
                            agent.set_state(state=new_state)
                        else: #try only translation
                            new_state = agent.state.update(rotation=0,
                                                           distance=distance)
                            agent_polygon = agent.get_polygon(state=new_state)
                            if self.is_valid_state(agent_polygon=agent_polygon,
                                                   collisions=agent.collision):
                                agent.set_state(state=new_state)
            with pulsekit.CodeBlock("agent_steps"):
                for name, agent in self.agents.items():
                    agent.step(delta_t=self.time_step)
            self.time += self.time_step
            self.step_count += 1

        with pulsekit.CodeBlock("model.after_step"):
            if self.after_step is not None:
                self.after_step()
        return self.time_step

    def close(self):
        if self.running:
            self.stop()
        if self.on_close:
            self.on_close()
