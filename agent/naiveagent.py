# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 00:49:30 2022

@author: Gordon
"""
# from agent import Agent
import random
from agentstate import Action

class NaiveAgent():
        
    def nextAction(self,percept):
        dice_roll = random.randint(1,6)
        
        return Action(dice_roll).name