'''
Created on 23 Dec 2013

@author: Emily
'''

import libtcodpy as libtcod
import R


class Tile:
    def __init__(self, x, y, blocks, blocks_sight=False, char=" ", bg = [60,100,80], fg= [255,255,255], field = False):
        self.x = x
        self.y = y
        
        if isinstance(char, int):
            self.char = chr(char)
        else:
            self.char = char
            
        
        self.colour_bg = libtcod.Color(bg[0],bg[1],bg[2])
        self.colour_fg = libtcod.Color(fg[0],fg[1],fg[2])
        
        self.blocks = blocks
        self.blocks_sight = blocks_sight
        self.explored = False
        self.type = ""
        
        if field:
            self.field()
        
    def field(self):
        self.plant = None
        self.fertiliser = None
        self.type = "field"
        self.tilled = 0 #out of 100
        self.till(libtcod.random_get_int(0, 0, 30))
        
    def set_type(self,type_):
        self.type = type_
    def explore(self):
        self.explored = True
    
    @property
    def fg(self):
        return self.colour_fg
    @property
    def bg(self):
        return self.colour_bg

    def till(self,tilling):
        if self.type is "field":
            self.tilled += tilling
            if self.tilled > 100:
                self.tilled = 100
            
            if self.tilled > 50 and self.char != "=":
                self.char = "="
    def plant(self, plant):
        if self.type is "field":
            self.plant = plant
            self.char = plant.char
    
class Map:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.tiles = [[ Tile(ix,iy, False, field = True, 
                             bg = [libtcod.random_get_int(0,125,145), libtcod.random_get_int(0,60,90), libtcod.random_get_int(0,10,40)], 
                             fg = [129, 50, 10],
                             char = "~")
            for iy in range(h) ]
                for ix in range(w)]
        
    def get_tile(self,x,y):
        return self.tiles[x][y]
    