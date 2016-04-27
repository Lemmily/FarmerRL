"""
Created on 23 Dec 2013

@author: Emily
"""

import libtcodpy as libtcod
import R

field_types = {"field": [0, 2],
               "clay": [25, 40],
               "gravel": [40, 60],
               "rock": [90, 100]

               }


class Tile:
    def __init__(self, x, y, blocks, blocks_sight=False, char=" ", bg=(60, 100, 80), fg=(255, 255, 255), field=False):
        self.x = x
        self.y = y

        if isinstance(char, int):
            self.char = chr(char)
        else:
            self.char = char

        self.colour_bg = libtcod.Color(bg[0], bg[1], bg[2])
        self.colour_fg = libtcod.Color(fg[0], fg[1], fg[2])

        self.blocks = blocks
        self.blocks_sight = blocks_sight
        self.explored = False
        self.type = ""

    def set_type(self, type_):
        self.type = type_

    def explore(self):
        self.explored = True

    @property
    def fg(self):
        return self.colour_fg

    @property
    def bg(self):
        return self.colour_bg


class Land(Tile):
    def __init__(self, x, y, blocks, blocks_sight=False, char="#", bg=(60, 100, 80), fg=(255, 255, 255), field=False):
        Tile.__init__(self, x, y, blocks, blocks_sight, char, bg, fg, field)
        self.plant = None
        self.fertiliser = None
        self.type = field_types.keys()[libtcod.random_get_int(0, 0, len(field_types) - 1)]
        self.tilled = 0  # out of 100
        self.till(libtcod.random_get_int(0, 0, 30))

    def till(self, tilling):
        if self.type is "field":
            self.tilled += tilling
            if self.tilled > 100:
                self.tilled = 100

            if self.tilled > 50 and self.char != "=":
                self.char = "="
                R.ui.message("The field looks more like a field now!")
                return True

    def sow(self, plant):
        if self.type is "field":
            self.plant = plant
            self.char = plant.char
            self.colour_fg = libtcod.Color(10, 200, 30)

    def remove_plant(self):
        R.land.plants.remove(self.plant)
        self.plant = None
        self.char = "~" # back to untilled land char.
        self.tilled = 0
        self.colour_fg = libtcod.Color(libtcod.random_get_int(0, 125, 145), libtcod.random_get_int(0, 60, 70),
                                       libtcod.random_get_int(0, 20, 40))

    @property
    def difficulty(self):
        return field_types[self.type][1]
        # libtcod.random_get_int(0, field_types[self.type][0], field_types[self.type][1])


class Map:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.tiles = [[Land(ix, iy, False, field=True,
                            bg=[libtcod.random_get_int(0, 125, 145), libtcod.random_get_int(0, 60, 90),
                                libtcod.random_get_int(0, 10, 40)],
                            fg=[129, 50, 10],
                            char="~")
                       for iy in range(h)]
                      for ix in range(w)]

        self.plants = []

    def add_plant(self, plant):
        self.plants.append(plant)

    def get_tile(self, x, y):
        return self.tiles[x][y]
