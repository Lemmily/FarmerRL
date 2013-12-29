'''
Created on 23 Dec 2013

@author: Emily
'''

import libtcodpy as libtcod
import R
import math

class Object:
    def __init__(self, x=0, y=0, char="@", name="blob", colour=libtcod.white, blocks=False, always_visible=False,
                    item=None, type_ = "object"):
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.type = type_
        self.colour = colour
        self.blocks = blocks
        self.always_visible = always_visible
        
        self.item = item
        if item:
            self.item.parent = self
            
        
    def _set_x(self,x):
        self.x = x
    def _set_y(self,y):
        self.y = y
    def _get_x(self):
        return self.x
    def _get_y(self):
        return self.y
    
    def clear(self, cam_x = 0, cam_y =0): 
        #erase the character that represents this object
        libtcod.console_put_char(R.con_char, self.x -cam_x, self.y- cam_y, " ", libtcod.BKGND_NONE)
        
    def draw(self, cam_x=0, cam_y=0):
        
        if (self.x >= cam_x and self.x < cam_x + R.MAP_VIEW_WIDTH and
                self.y >= cam_y and self.y < cam_y + R.MAP_VIEW_HEIGHT):
            
                pos_x = self.x - cam_x
                pos_y = self.y - cam_y
                
#                 libtcod.console_put_char(R.con, pos_x, pos_y, " ")
                libtcod.console_set_default_foreground(R.con_char, self.colour)
#                 libtcod.console_put_char_ex(R.con_char, pos_x, pos_y, self.char, self.colour, self.colour)
                libtcod.console_put_char(R.con_char, pos_x, pos_y, self.char, libtcod.BKGND_NONE)
        
class Mover(Object):
    def __init__(self, x=0, y=0, char="@", name="blob", colour=libtcod.white, blocks=False, always_visible=False,
                        fighter=None, you=None, pather=None, ai=None):
        Object.__init__(self, x, y, char, name, colour, blocks, always_visible)
        self.direction = "S"
        self.you = you
        if you:
            self.you.parent = self
        

    def move(self, dx, dy):
        #move by the given quantity, if the destination is not blocked
        if not is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
            return True
        return False
     
    def move_p(self, dx, dy):
        #move by the given quantity
        self.x += dx
        self.y += dy
       
    def move_towards(self, target_x, target_y):
        #vector from this object to the other and the distance
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        self.move(dx, dy)

    def distance(self, x, y):
        #return the distance to some coordinates
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)
    
class Player(Mover):
    def __init__(self):
        Mover.__init__(self, name = "Player", char = "&")
        self.skills = Skills()  

class Item(Object):
    def __init__(self):
        Object.__init__()
        

skill_list_1 = [ #// 0_name:string, 1_attribute, 2_needTraining:Boolean, 3_desc:String,[4_dependsOn],[5_dependants]
                 ["Appraise", "int", False, "Used to analyse an item for monetary value, and contributing factors",["none"],["none"]],
                 ["Armour", "str", False, "How well you can wear armour. Negates some of the penalties of heavier armour",["none"],["none"]],
                 ["Dodge", "dex", False, "Improves your chance of dodging attacks and traps",["none"],["none"]],
                 ["Fighting", "dex", False, "Improves your chance of hitting and your damage in melee",["none"],["none"]],
                 ["Tilling", "str", False, "The skill at which you can till the land.",["none"],["none"]],
                 ["Fertiliser", "int", False, "The knowledge on Fertilisers and their use on different plants.",["none"],["none"]],
                 ["Harvest", "dex", False, "The skill of harvesting plants. Some will need high skill to reap the rewards.",["none"],["none"]],
                 ["Plant Expertise", "int", False, "To successfully identify plants and the information about them; this skill is required",["none"],["none"]],
                ]
# Skill manager
class Skills:
    def __init__(self):
        pass
        self.dict = {}
        for line in skill_list_1:
            self.dict[line[0]] = Skill( line[0], line[1])
        
        
    def skill_level_check(self,skill):
        
        sk_exp = self.dict[skill].exp
        
        return sk_exp #TODO: nake lookup table to look up what level the skill is at. for now just retrun this/

class Skill:
    def __init__(self,name,group="None"):
        self.name = name
        self.group = group
        self.exp = 0
            
def is_blocked(x, y):
    #first test the map tile
    if x > len(R.tiles) - 1 or x < 0:
        return True
    if y > len(R.tiles[x]) - 1 or y < 0:
        return True
    if R.tiles[x][y].blocked:
        return True
    #now check for any blocking objects
#     for object_ in R.world_obj:
#         if object_.blocks and object_.x == x and object_.y == y:
#             return True
    return False

