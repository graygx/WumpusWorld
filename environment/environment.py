# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 04:02:04 2022

@author: Gordon
"""
import pygame
from dataclasses import dataclass, field
from agentstate import AgentState, Orientation, Action, Coords, Percept
import numpy as np
import random


BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400


@dataclass
class Environment:
    

    _width: int = 4
    _height: int = 4
    _pit_prob: float = 0.2
    _climb_without_gold: bool = False


    
    _screen: pygame.display = None
    _clock: pygame.time = None
    _block_size: int = 100 #Set the size of the grid block

    
    _agent_state: AgentState = field(default_factory=AgentState)
    _pit_locs: list = field(default_factory=list)
    _terminated: bool = False
    _wumpus_loc: Coords = None
    _wumpus_alive: bool = True
    _gold_loc: Coords = None
    
        
        
    def __post_init__(self):
        
        x = random.randint(0,self._width)
        y = random.randint(0,self._height)
        if (x == 0) and (y == 0):
            x = random.randint(self._width)
            y = random.randint(self._height) 
        self._wumpus_loc = Coords(x,y)
        
        x = random.randint(0,self._width)
        y = random.randint(0,self._height)
        if (x == 0) and (y == 0):
            x = random.randint(self._width)
            y = random.randint(self._height) 
        self._gold_loc = Coords(x,y)
        
        cell_indx = []
        for x in range(0,self._width):
            for y in range(0,self._height):
                cell_indx.append(Coords(x,y))
        
        filtered=[]
        for cell in cell_indx:
            if random.random() < self._pit_prob:
                filtered.append(cell)
        
        self._pit_locs = filtered
                
        
        
    #     pygame.init()
    #     self._screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    #     self._clock = pygame.time.Clock()
    #     self._screen.fill(BLACK)
    #     pygame.display.set_caption("Welcome to Wumpus World")

    #     running = True
    #     try:
    #         while running:
    #             self.drawGrid()
    #             for event in pygame.event.get():
    #                 if event.type == pygame.QUIT:
    #                     running = False
    #             pygame.display.update()
    #         pygame.quit()
    #     except SystemExit:
    #         pygame.quit()
    
    def drawGrid(self):
        for x in range(0, WINDOW_WIDTH, self._block_size):
            for y in range(0, WINDOW_HEIGHT, self._block_size):
                rect = pygame.Rect(x, y, self._block_size, self._block_size)
                pygame.draw.rect(self._screen, WHITE, rect, 1)
                
    def __is_pit_at(self,coords):
        if coords in self._pit_locs:
            return True
        else:
            return False
        
    def __is_wumpus_at(self,coords):
        if coords == self._wumpus_loc:
            return True
        else:
            return False
        
    def __is_agent_at(self,coords):
        if coords == self._agent_state.location[0]:
            return True
        else:
            return False
        
    def __is_glitter_at(self,coords):
        if self._gold_loc == self._agent_state.location[0]:
            return True
        else:
            return False
        
    def __is_gold_at(self,coords):
        if coords == self._gold_loc:
            return True
        else:
            return False
        
    def __is_wumpus_hit(self):
        
        if ((self._agent_state.has_arrow == True) and (self._wumpus_alive == True)):
            if ((self._agent_state.orientation == Orientation.East) and (self._agent_state.location[0].x < self._wumpus_loc.x) and (self._agent_state.location[0].y == self._wumpus_loc.y)):
                return True
            elif ((self._agent_state.orientation == Orientation.West) and (self._agent_state.location[0].x > self._wumpus_loc.x) and (self._agent_state.location[0].y == self._wumpus_loc.y)):
                return True
            elif ((self._agent_state.orientation == Orientation.South) and (self._agent_state.location[0].x == self._wumpus_loc.x) and (self._agent_state.location[0].y > self._wumpus_loc.y)):
                return True
            elif ((self._agent_state.orientation == Orientation.North) and (self._agent_state.location[0].x == self._wumpus_loc.x) and (self._agent_state.location[0].y < self._wumpus_loc.y)):
                return True
            else:
                return False
        else:
            return False
    
    def __is_pit_adjacent(self,coords):
        return any([cell in self._pit_locs for cell in coords.cells_adjacent(self._width,self._height)])
    
    def __is_wumpus_adjacent(self,coords):
        return any([self._wumpus_loc == cell for cell in coords.cells_adjacent(self._width,self._height)])
    
    def __is_breeze(self):
        return self.__is_pit_adjacent(self._agent_state.location[0])
        
    def __is_stench(self):
        return ((self.__is_wumpus_adjacent(self._agent_state.location[0])) or (self.__is_wumpus_at(self._agent_state.location[0])))
    
    def applyAction(self,action):
        if self._terminated:
            return Percept(False,False,False,False,False,True,0)
        else:
            if action == Action.Forward.name:
                prev_loc = self._agent_state.location[0]
                self._agent_state.forward(self._width,self._height)
                self._terminated = ((self.__is_wumpus_at(self._agent_state.location[0])) and (self._wumpus_alive)) or (self.__is_pit_at(self._agent_state.location[0]))
                self._agent_state.is_alive = not self._terminated
                if self._agent_state.has_gold:
                    self._gold_loc = self.agent_state.location
                if self._agent_state.is_alive:
                    reward = -1
                else:
                    reward = -1001
                return Percept(self.__is_stench(),self.__is_breeze(),self.__is_glitter_at(self._agent_state.location[0]),prev_loc == self._agent_state.location[0],False,not self._agent_state.is_alive,reward)
            
            elif action == Action.TurnLeft.name:
                self._agent_state.turnLeft()
                return Percept(self.__is_stench(),self.__is_breeze(),self.__is_glitter_at(self._agent_state.location[0]),False,False,False,-1)
            
            elif action == Action.TurnRight.name:
                self._agent_state.turnRight()
                return Percept(self.__is_stench(),self.__is_breeze(),self.__is_glitter_at(self._agent_state.location[0]),False,False,False,-1)
            
            elif action == Action.Grab.name:
                self._agent_state.has_gold = self.__is_gold_at(self._agent_state.location[0])
                if self._agent_state.has_gold:
                    self._gold_loc = self._agent_state.location[0]
                    
                return Percept(self.__is_stench(),self.__is_breeze(),self.__is_glitter_at(self._agent_state.location[0]),False,False,False,-1)
            
            elif action == Action.Climb.name:
                in_start_loc = self._agent_state.location[0] == Coords(0,0)
                success = self._agent_state.has_gold and in_start_loc
                self._terminated = success or (self._climb_without_gold and in_start_loc)
                if success:
                    reward = 999
                else:
                    reward = -1
                return Percept(self.__is_stench(),self.__is_breeze(),self.__is_glitter_at(self._agent_state.location[0]),False,False,False,reward)
            
            elif action == Action.Shoot.name:
                hadarrow = self._agent_state.has_arrow
                if hadarrow:
                    reward = -11
                else:
                    reward = -1
                self._agent_state.use_arrow()
                wumpuskilled = self.__is_wumpus_hit()
                self._wumpus_alive = not wumpuskilled
                return Percept(self.__is_stench(),self.__is_breeze(),self.__is_glitter_at(self._agent_state.location[0]),False,wumpuskilled,False,reward)

    def visualize(self):
        if (self._wumpus_alive):
            wumpus_symbol = "W" 
        else: 
            wumpus_symbol = "w"
        for y in np.arange(self._height-1,0,-1):
            for x in np.arange(0,self._width):
                if self.__is_agent_at(Coords(x,y)):
                    print("A",end='')
                else:
                    print(" ",end='')
                    
                if self.__is_pit_at(Coords(x,y)):
                    print("P",end='')
                else:
                    print(" ",end='')
                    
                if self.__is_gold_at(Coords(x,y)):
                    print("G",end='')
                else:
                    print(" ",end='')
                    
                if self.__is_wumpus_at(Coords(x,y)):
                    print(wumpus_symbol,end='')
                else:
                    print(" ",end='')
                print("|",end='')
            print("\n")      
        
        
                
    
