# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 16:11:00 2022

@author: Gordon
"""
from environment import Environment
from agentstate import AgentState, Orientation, Action, Coords, Percept
from naiveagent import NaiveAgent
    
def main(num_lives=1):
    for i in range(num_lives):
        print("Life ",i+1,"/",num_lives)
        env = Environment(4,4,0.2,False)
        agent = NaiveAgent()
        percept = Percept(False, False, False, False, False, False, 0)
        runEpisode(env, agent, percept)

def runEpisode(env, agent, percept):
    while (not percept.isTerminated):
        nextAction = agent.nextAction(percept)
        print("Action:", nextAction)
        percept = env.applyAction(nextAction)
        print(env.visualize())
        print(percept.show_percept())
      


if __name__ == "__main__":
    num_lives=1
    main(num_lives)