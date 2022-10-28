# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 20:50:05 2022

@author: Gordon
"""

# from agent import Agent
import random
from agentstate import Action, Coords, Orientation, AgentState
import networkx as nx
from dataclasses import dataclass, field
import matplotlib.pyplot as plt
import numpy as np


@dataclass
class BeelineAgent():

    width: int
    height: int
    agent_state: AgentState = field(default_factory=AgentState)
    safe_locations: list = field(default_factory=list)
    escape_plan: list = field(default_factory=list)
    plan_created: bool = False

    def create_escape_plan(self):
        self.plan_created = True

        G = nx.Graph()
        G.add_nodes_from(
            list(set([item for sublist in self.safe_locations for item in sublist])))

        for node in G.nodes:
            connected_nodes = node.cells_adjacent(self.width, self.height)
            for adj_node in connected_nodes:
                if adj_node in G.nodes:
                    G.add_edge(node, adj_node)

        plt.Figure()
        nx.draw(G)
        plt.show(block=False)
        plt.pause(3)
        plt.close()

        shortest_path = nx.shortest_path(
            G, self.agent_state.location, Coords(0, 0))

        self.escape_plan = self.create_escape_actions(shortest_path)

    def create_escape_actions(self, path):

        escape_plan = []
        agent_predict_orient = self.agent_state.orientation

        while len(path) > 1:
            start = path.pop(0)
            end = path[0]
            if (start.x == end.x):
                if (start.y < end.y):
                    heading = Orientation.North
                else:
                    heading = Orientation.South
            else:
                if (start.x < end.x):
                    heading = Orientation.East
                else:
                    heading = Orientation.West

            if (agent_predict_orient.name == Orientation.North.name) and (heading.name == Orientation.East.name):
                escape_plan.append(3)
            elif (agent_predict_orient.name == Orientation.South.name) and (heading.name == Orientation.East.name):
                escape_plan.append(2)
            elif (agent_predict_orient.name == Orientation.West.name) and (heading.name == Orientation.East.name):
                escape_plan.append(2)
                escape_plan.append(2)
            elif (agent_predict_orient.name == Orientation.North.name) and (heading.name == Orientation.West.name):
                escape_plan.append(2)
            elif (agent_predict_orient.name == Orientation.South.name) and (heading.name == Orientation.West.name):
                escape_plan.append(3)
            elif (agent_predict_orient.name == Orientation.East.name) and (heading.name == Orientation.West.name):
                escape_plan.append(2)
                escape_plan.append(2)
            elif (agent_predict_orient.name == Orientation.South.name) and (heading.name == Orientation.North.name):
                escape_plan.append(2)
                escape_plan.append(2)
            elif (agent_predict_orient.name == Orientation.East.name) and (heading.name == Orientation.North.name):
                escape_plan.append(2)
            elif (agent_predict_orient.name == Orientation.West.name) and (heading.name == Orientation.North.name):
                escape_plan.append(3)
            elif (agent_predict_orient.name == Orientation.North.name) and (heading.name == Orientation.South.name):
                escape_plan.append(2)
                escape_plan.append(2)
            elif (agent_predict_orient.name == Orientation.East.name) and (heading.name == Orientation.South.name):
                escape_plan.append(3)
            elif (agent_predict_orient.name == Orientation.West.name) and (heading.name == Orientation.South.name):
                escape_plan.append(2)

            escape_plan.append(1)
            agent_predict_orient = heading

        return escape_plan

    def nextAction(self, percept):

        if (self.agent_state.has_gold):
            if (self.agent_state.location == Coords(0, 0)):
                return Action(6).name
            else:
                if not self.plan_created:
                    self.create_escape_plan()
                    print('____________')
                    print('Indiana Jones Time!! Escape Plan:', self.escape_plan)
                    print('^^^^^^^^^^^^')

                nextmove = self.escape_plan.pop(0)
                self.agent_state.move_action(
                    Action(nextmove).name, self.width, self.height)
                return Action(nextmove).name

        elif (percept.glitter):
            self.agent_state.has_gold = True
            return Action(5).name
        else:
            dice_roll = random.randint(1, 4)

            if Action(dice_roll).name == Action.Forward.name:
                prev_loc = self.agent_state.location

            self.agent_state.move_action(
                Action(dice_roll).name, self.width, self.height)

            if Action(dice_roll).name == Action.Forward.name:
                if prev_loc != self.agent_state.location:
                    self.safe_locations.append(
                        tuple([prev_loc, self.agent_state.location]))

            return Action(dice_roll).name
