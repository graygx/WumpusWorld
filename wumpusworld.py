# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 16:11:00 2022

@author: Gordon
"""
from environment import Environment
from agentstate import AgentState, Orientation, Action, Coords, Percept
from naiveagent import NaiveAgent
from beelineagent import BeelineAgent


def main(num_lives=1):
    for i in range(num_lives):
        print("Life ", i+1, "/", num_lives)
        env = Environment(4, 4, 0.1, False)
        agent = BeelineAgent(4, 4)
        percept = Percept(False, False, False, False, False, False, 0)
        total_reward = runEpisode(env, agent, percept)
        print('Final Score:', total_reward)
        print('----------------------------------------------')
        print('----------------------------------------------')


def runEpisode(env, agent, percept):
    total = 0
    while (not percept.isTerminated):
        nextAction = agent.nextAction(percept)
        print("Action:", nextAction)
        percept = env.applyAction(nextAction)
        env.visualize()
        percept.show_percept()
        total += percept.reward
    return total


if __name__ == "__main__":
    num_lives = 50
    main(num_lives)
