'''
Created on 1 Mar 2013

@author: Emily
'''
import libtcodpy as libtcod
import textwrap
import R

class UI:    
    def __init__(self, con, game_msgs=[]):
        #global con
        self.con = con
        self.game_msgs=game_msgs
      
    def menu(self, header, options, width):
        global keys
        
        if len(options) > 26: raise ValueError("cannot have a menu with more than 26 options")
        header_height = libtcod.console_get_height_rect(self.con, 0, 0,width,R.SCREEN_HEIGHT, header)
        if header_height == "":
            header_height = 0
        height = len(options) + header_height
        
        #now creates an off screen console that represents the menu windwo.
        window = libtcod.console_new(width,height)
        
        #print the header with auto-wrap
        libtcod.console_set_default_foreground(window, libtcod.white)
        libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)
        
        y = header_height
        letter_index = ord("a")
        for option_text in options:
            text = "(" + chr(letter_index) + ")" + option_text
            libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
            y += 1
            letter_index += 1
    
        x = R.SCREEN_WIDTH/2 - width/2
        y = R.SCREEN_HEIGHT/2 - height/2
        libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)
        
        
        while True:
            libtcod.console_flush()
            key = libtcod.console_wait_for_keypress(True)
            
            if key.vk == libtcod.KEY_ENTER and key.lalt:
                #Alt+Enter: toggle fullscreen
                libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    
            if key.vk == libtcod.KEY_ESCAPE or key.vk == libtcod.KEY_BACKSPACE:
                return None  #exit inventory
    
            index = key.c - ord("a")
            if index >= 0 and index < len(options): return index
            #return None
            
    def menu_size(self, header, options, width):
        global keys
        
        if len(options) > 26: raise ValueError("cannot have a menu with more than 26 options")
        header_height = libtcod.console_get_height_rect(self.con, 0, 0,width,R.SCREEN_HEIGHT, header)
        if header_height == "":
            header_height = 0
        height = len(options) + header_height
        
        #now creates an off screen console that represents the menu windwo.
        window = libtcod.console_new(width,height)
        
        #print the header with auto-wrap
        libtcod.console_set_default_foreground(window, libtcod.white)
        libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)
        
        y = header_height
        letter_index = ord("a")
        for option_text in options:
            text = "(" + chr(letter_index) + ")" + option_text
            libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
            y += 1
            letter_index += 1
    
        x = R.SCREEN_WIDTH/2 - width/2
        y = R.SCREEN_HEIGHT/2 - height/2
        libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)
        
        
        while True:
            libtcod.console_flush()
            key = libtcod.console_wait_for_keypress(True)
            
            if key.vk == libtcod.KEY_ENTER and key.lalt:
                #Alt+Enter: toggle fullscreen
                libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    
            if key.vk == libtcod.KEY_ESCAPE or key.vk == libtcod.KEY_BACKSPACE:
                return None  #exit inventory
    
            index = key.c - ord("a")
            if index >= 0 and index < len(options): return index
            
    def msgbox(self,text, width = 50):
        self.menu(text,[], width)
        
    def message(self, new_msg, colour = libtcod.white, date = None, game_msgs = []):
        # using "textwrap" split the message if necessary
        if len(game_msgs) <= 0:
            game_msgs = R.game_msgs
            
        if date is not None:
            new_msg = str(date[0]) + " " + str(date[1][0]) + " " + str(date[2][0]) + " " + new_msg
            
        new_msg_lines = textwrap.wrap(new_msg, R.MSG_WIDTH)
    
        for line in new_msg_lines:
            #if the buffer is full, then remove some messages to make room for more.
            if len(game_msgs) == R.MSG_HEIGHT - 2:
                del game_msgs[0]
    
                #add the new line as a tuple, with text and the colour.
            R.game_msgs.append( (line, colour) )
        R.msg_redraw = True