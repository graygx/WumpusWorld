# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 01:30:47 2022

@author: Gordon
"""

from dataclasses import dataclass
from enum import Enum
import numpy as np

class Orientation(Enum):
    North = 1
    East = 2
    South = 3
    West = 4

class Action(Enum):
    Forward = 1
    TurnLeft = 2
    TurnRight = 3
    Shoot = 4
    Grab = 5
    Climb = 6
        
@dataclass
class Coords:
    x: int
    y: int
    
    def isAdjacentTo(self,coords):
        return ((self.x == coords.x) and (np.abs(coords.y - self.y) == 1)) or ((self.y == coords.y) and (np.abs(coords.x - self.x) == 1))
    
    def cells_adjacent(self,gridwidth, gridheight):
        coords_lst=[]
        
        if self.x > 0:
            coords_lst.append(Coords(self.x-1,self.y))
        
        if self.x < (gridwidth-1):
            coords_lst.append(Coords(self.x+1,self.y))
            
        if self.y > 0:
            coords_lst.append(Coords(self.x,self.y-1))
            
        if self.y < (gridheight-1):
            coords_lst.append(Coords(self.x,self.y+1))
            
        return coords_lst
        
        
    

@dataclass
class AgentState:
    
    location: Coords = Coords(0,0)
    orientation: Orientation = Orientation.North
    has_gold: bool = False
    has_arrow: bool = True
    is_alive: bool = True
    
    def turnLeft(self):
        if self.orientation.name == Orientation.West.name:
            self.orientation = Orientation.South
        elif self.orientation.name == Orientation.East.name:
            self.orientation = Orientation.North
        elif self.orientation.name == Orientation.North.name:
            self.orientation = Orientation.West
        elif self.orientation.name == Orientation.South.name:
            self.orientation = Orientation.East
    def turnRight(self):
        if self.orientation.name == Orientation.West.name:
            self.orientation = Orientation.North
        elif self.orientation.name == Orientation.East.name:
            self.orientation = Orientation.South
        elif self.orientation.name == Orientation.North.name:
            self.orientation = Orientation.East
        elif self.orientation.name == Orientation.South.name:
            self.orientation = Orientation.West
        
    def forward(self,gridwidth,gridheight):
        if self.orientation.name == Orientation.East.name:
            self.location = Coords(min(gridwidth-1,self.location.x+1), self.location.y)
        elif self.orientation.name == Orientation.West.name:
            self.location = Coords(max(0,self.location.x-1), self.location.y)
        elif self.orientation.name == Orientation.South.name:
            self.location = Coords(self.location.x, max(0,self.location.y-1))
        elif self.orientation.name == Orientation.North.name:
            self.location = Coords(self.location.x, min(gridheight-1,self.location.y+1))
        
    def show_state(self):
        print("Location:", self.location, "orientation:", self.orientation, "hasGold:", self.has_gold, "hasArrow:", self.has_arrow, "isAlive:", self.is_alive)

    def use_arrow(self):
        self.has_arrow = False
        
    def move_action(self,action,gridwidth,gridheight):
        if action == Action.TurnLeft.name:
            self.turnLeft()
        elif action == Action.TurnRight.name:
            self.turnRight()
        elif action == Action.Forward.name:
            self.forward(gridwidth,gridheight)
        else:
            pass
        

@dataclass
class Percept():
    stench: bool
    breeze: bool
    glitter: bool
    bump: bool
    scream: bool
    isTerminated: bool
    reward: float
    
    def show_percept(self):
        print("stench:", self.stench, "breeze:", self.breeze, "glitter:", self.glitter, "bump:", self.bump, "scream:", self.scream, "isTerminated:", self.isTerminated, "reward:", self.reward)
