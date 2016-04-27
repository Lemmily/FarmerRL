"""
Created on 23 Dec 2013

@author: Emily
"""

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 60

LIMIT_FPS = 20

INFO_BAR_WIDTH = 25

MAP_VIEW_WIDTH = SCREEN_WIDTH - INFO_BAR_WIDTH  # viewport for map screen
MAP_VIEW_WIDTH_HALF = MAP_VIEW_WIDTH / 2
MAP_VIEW_HEIGHT = 40
MAP_VIEW_HEIGHT_HALF = 20

MAP_WIDTH = 80  # actual map size
MAP_HEIGHT = 60  # map size

PANEL_HEIGHT = SCREEN_HEIGHT - MAP_VIEW_HEIGHT
PANEL_WIDTH = SCREEN_WIDTH - INFO_BAR_WIDTH
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT

MSG_X = 2
MSG_WIDTH = SCREEN_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1

ui = None
game_msgs = []
date = []

con = None
con_char = None
inf = None

land = None
tiles = []
objects = []

# ## FLAGS
msg_redraw = True
