'''
Created on 23 Dec 2013

@author: Emily
'''
import libtcodpy as libtcod
import R
import map_plot
import UI
import entities

DAYS = [
    ['Monday', 1],
    ['Tuesday', 2],
    ['Wednesday', 3],
    ['Thursday', 4],
    ['Friday', 5],
    ['Saturday', 6],
    ['Sunday', 7]
]

MONTHS = [
    ['January', 1, 31],
    ['February', 2, 28],
    ['March', 3, 31],
    ['April', 4, 30],
    ['May', 5, 31],
    ['June', 6, 30],
    ['July', 7, 31],
    ['August', 8, 31],
    ['September', 9, 30],
    ['October', 10, 31],
    ['November', 11, 30],
    ['December', 12, 31],
]

libtcod.namegen_parse("data/names.txt")

SLOW_SPEED = 8
NORM_SPEED = 12
FAST_SPEED = 20
FASTEST_SPEED = 30
game_speed = NORM_SPEED

turns = 0
pause = False
fov_recompute = True
info_redraw = True
debug_mode = False


def new_game():
    global mouse, key, fov_recompute, cam_x, cam_y, game_state
    global you, land, objects
    mouse = libtcod.Mouse()
    key = libtcod.Key()

    cam_x, cam_y = 0, 0

    fov_recompute = True

    game_state = "playing"

    R.land = land = map_plot.Map(R.MAP_WIDTH, R.MAP_HEIGHT)
    R.tiles = land.tiles
    R.objects = objects = []
    you = R.you = entities.Player()
    objects.append(you)


def advance_time():
    global date, sub_turns, turns, msg_redraw

    turns += game_speed

    if turns >= 60:
        turns = 0

        date[0] += 1

    if date[0] == 24:
        old_day = date[1][1]
        new_day = old_day + 1
        if new_day > 7:
            new_day = 1
        date[0] = 0  # set hours to zero
        date[1][0] = DAYS[new_day - 1][0]  # set the new day name - newDay -1 because array 0ness
        date[1][1] = new_day  # day reference value
        date[1][2] += 1  # increase the actual numerical date by a day

        for plant in R.land.plants:
            plant.age_up()

    if date[1][2] > date[2][2]:  # // if current day is more than the months max days, increase month.
        old_month = date[2][1]
        new_month = old_month + 1

        if new_month >= 12:
            new_month = 1

        date[1][2] = 1
        date[2][0] = MONTHS[new_month - 1][0]  # /change month name
        date[2][1] = MONTHS[new_month - 1][1]  # //change month date value
        date[2][2] = MONTHS[new_month - 1][2]  # //change max days in month.

    if date[2][1] > 12:  # //if the month is over 12, increase the year/

        ##
        # ## Do anything that needs to be the start of the year here. BUT use the old year
        # #

        date[2][0] = MONTHS[0][0]  # //change month name to first month
        date[2][1] = MONTHS[0][1]  # //change month date value to first month
        date[2][2] = MONTHS[0][2]  # //change max days in month to first month's
        date[3] += 1  # //increase year

        # #
        # ## Do anything that needs to be the start of the year here. AND use the new year
        # #
    msg_redraw = True


def scrolling_map(p, hs, s, m):
    """
    Get the position of the camera in a scrolling map:

     - p is the position of the player.
     - hs is half of the screen size
     - s is the full screen size.
     - m is the size of the map.
    """
    if p < hs or m < s:
        return 0
    elif p > m - hs:
        return m - s
    else:
        return p - hs


def handle_mouse():
    pass


def handle_keys():
    global fov_recompute, pause, debug_mode
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    elif key.vk == libtcod.KEY_ESCAPE:
        return "exit"  # exit game

    if game_state == "playing":
        # movement keys

        if key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
            you.direction = "N"
            player_move_or_attack(0, -1)
        elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
            you.direction = "S"
            player_move_or_attack(0, 1)
        elif key.vk == libtcod.KEY_LEFT or key.vk == libtcod.KEY_KP4:
            you.direction = "E"
            player_move_or_attack(-1, 0)
        elif key.vk == libtcod.KEY_RIGHT or key.vk == libtcod.KEY_KP6:
            you.direction = "W"
            player_move_or_attack(1, 0)
        elif key.vk == libtcod.KEY_HOME or key.vk == libtcod.KEY_KP7:
            you.direction = "NW"
            player_move_or_attack(-1, -1)
        elif key.vk == libtcod.KEY_PAGEUP or key.vk == libtcod.KEY_KP9:
            you.direction = "NE"
            player_move_or_attack(1, -1)
        elif key.vk == libtcod.KEY_END or key.vk == libtcod.KEY_KP1:
            you.direction = "SW"
            player_move_or_attack(-1, 1)
        elif key.vk == libtcod.KEY_PAGEDOWN or key.vk == libtcod.KEY_KP3:
            you.direction = "SE"
            player_move_or_attack(1, 1)

        elif key.vk == libtcod.KEY_KP5:
            player_move_or_attack(0, 0)
            pass  # do nothing ie wait for the monster to come to you
        elif key.vk == libtcod.KEY_SPACE:
            pause = not pause

        else:

            key_char = chr(key.c)

            if key_char == "t":
                you.actions["till"](you)
                fov_recompute = True
            elif key_char == "p":
                you.actions["plant"](you)
                fov_recompute = True
            elif key_char == "h":
                you.actions["harvest"](you)
                fov_recompute = True
            elif key_char == "d":
                debug_mode = not debug_mode

            if debug_mode:
                if key_char == "a":
                    for plant in R.land.plants:
                        plant.age_up(10)


def player_move_or_attack(dx, dy):
    global fov_recompute, info_redraw
    print "I MOVED"
    you.move_p(dx, dy)
    if you.x >= R.MAP_WIDTH:
        you.x = R.MAP_WIDTH - 1
    if you.y >= R.MAP_HEIGHT:
        you.y = R.MAP_HEIGHT - 1

    fov_recompute = True
    info_redraw = True


def play_game():
    global key, mouse, land, you, msg_redraw

    mouse = libtcod.Mouse()
    key = libtcod.Key()
    print "play"

    while not libtcod.console_is_window_closed():

        # libtcod.console_clear(R.con);
        # libtcod.console_clear(R.con_char);
        libtcod.console_clear(0)
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if not pause:
            advance_time()

        player_action = handle_keys()

        if player_action == "exit":
            # save here
            break
        handle_mouse()

        for object_ in R.objects:
            object_.clear(cam_x, cam_y)

        if R.msg_redraw:
            update_msg_bar()

        if info_redraw:
            update_inf_bar()

        render()


def clear_consoles():
    for x in range(R.MAP_VIEW_WIDTH):  # this refers to the SCREEN position.
        for y in range(R.MAP_VIEW_HEIGHT):
            libtcod.console_set_char(con, x, y, " ")
            libtcod.console_set_char(con_char, x, y, " ")


def render():
    global fov_recompute, land, you

    cam_x = scrolling_map(you.x, R.MAP_VIEW_WIDTH_HALF + 1, R.MAP_VIEW_WIDTH, R.MAP_WIDTH)
    cam_y = scrolling_map(you.y, R.MAP_VIEW_HEIGHT_HALF, R.MAP_VIEW_HEIGHT, R.MAP_HEIGHT)

    if fov_recompute:
        fov_recompute = False

        for y in range(min(len(R.tiles[0]), R.MAP_VIEW_HEIGHT)):  # this refers to the SCREEN position. NOT map.
            for x in range(min(len(R.tiles), R.MAP_VIEW_WIDTH)):
                map_x = x + cam_x
                map_y = y + cam_y
                if map_x < len(R.tiles) and map_y < len(R.tiles[0]):
                    tile = R.tiles[map_x][map_y]
                    # libtcod.console_set_char(con, x, y, tile.char)
                    libtcod.console_put_char_ex(con, x, y, tile.char, tile.fg, tile.bg)
                    libtcod.console_set_char(con_char, x, y, " ")
                else:
                    libtcod.console_set_char_foreground(con, x, y, libtcod.chartreuse)
                    # libtcod.console_set_char(con, x, y, " ")
                    libtcod.console_put_char_ex(con, x, y, ' ', libtcod.black, libtcod.black)
                    libtcod.console_set_char(con_char, x, y, ' ')
        for thing in R.objects:
            thing.draw(cam_x, cam_y)

        you.draw(cam_x, cam_y)

    you.draw(cam_x, cam_y)
    libtcod.console_blit(con, 0, 0, R.MAP_VIEW_WIDTH, R.MAP_VIEW_HEIGHT, 0, 0, 0, 0.8, 1)
    libtcod.console_blit(con_char, 0, 0, R.MAP_VIEW_WIDTH, R.MAP_VIEW_HEIGHT, 0, 0, 0, 1, 0)
    libtcod.console_flush()


def update_msg_bar():
    global msg_redraw

    libtcod.console_clear(message_bar)
    libtcod.console_set_default_foreground(message_bar, libtcod.white)
    libtcod.console_print_ex(message_bar, 0, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_date())
    # print the messages, one line at a time.
    y = 2
    for (line, colour) in R.game_msgs:
        libtcod.console_set_default_foreground(message_bar, colour)
        libtcod.console_print_ex(message_bar, R.MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
        y += 1
    libtcod.console_blit(message_bar, 0, 0, R.PANEL_WIDTH, R.PANEL_HEIGHT, 0, 0, R.PANEL_Y)
    # libtcod.console_flush() #if this fluch is here it flickers the console.
    msg_redraw = False


def update_inf_bar():
    global info_redraw
    print "Info bar update"
    libtcod.console_clear(inf)
    libtcod.console_set_default_foreground(inf, libtcod.white)
    libtcod.console_print_ex(inf, 0, 0, libtcod.BKGND_NONE, libtcod.LEFT, "INFO:")
    y = 2
    for (line, colour) in get_player_tile():
        libtcod.console_set_default_foreground(inf, colour)
        libtcod.console_print_ex(inf, R.MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
        y += 1
    libtcod.console_blit(inf, R.MAP_VIEW_WIDTH, 0, R.INFO_BAR_WIDTH, R.PANEL_HEIGHT, 0, 0, 0)
    info_redraw = False


def get_player_tile():
    msg = [("" + str(you.x) + "," + str(you.y), libtcod.white)]

    tile = R.tiles[you.x][you.y]

    msg.append(("type :- " + tile.type, libtcod.light_amber))
    msg.append(("tilled :- " + str(tile.tilled) + "/100", libtcod.green))
    msg.append(("challenge :- " + str(tile.difficulty), libtcod.dark_green))

    print msg
    return msg


def get_date():
    return str(date[0]) + " " + str(date[1][0]) + " " + str(date[1][2]) + " " + str(date[2][0])


def main_menu():
    init()

    while not libtcod.console_is_window_closed():
        libtcod.console_set_default_foreground(0, libtcod.light_yellow)
        libtcod.console_print_ex(0, R.SCREEN_WIDTH / 2, R.SCREEN_HEIGHT / 2 - 2,
                                 libtcod.BKGND_NONE, libtcod.CENTER, "...*** FarmerRL ***...")
        libtcod.console_print_ex(0, R.SCREEN_WIDTH / 2, R.SCREEN_HEIGHT / 2 - 4,
                                 libtcod.BKGND_NONE, libtcod.CENTER, "By Lemmily")

        choice = R.ui.menu("", ["Play a new game", "Quit"], 24)

        if choice == 0:
            new_game()
            play_game()
        else:
            break


def init():
    global con, con_char, inf, game_msgs, date, ui, message_bar

    libtcod.console_set_custom_font("data/ont_big.png", libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(R.SCREEN_WIDTH, R.SCREEN_HEIGHT, "FarmerRL", False)
    libtcod.sys_set_fps(R.LIMIT_FPS)

    R.com = con = libtcod.console_new(R.MAP_WIDTH, R.MAP_HEIGHT)
    R.con_char = con_char = libtcod.console_new(R.MAP_WIDTH, R.MAP_HEIGHT)

    R.inf = inf = libtcod.console_new(R.INFO_BAR_WIDTH, R.SCREEN_HEIGHT - R.PANEL_HEIGHT)
    R.message_bar = message_bar = libtcod.console_new(R.PANEL_WIDTH, R.PANEL_HEIGHT)
    game_msgs = R.game_msgs = []

    ui = R.ui = UI.UI(con, game_msgs)
    date = R.date = [0, [DAYS[0][0], 1, 1], [MONTHS[0][0], 1, 31], 1000]


main_menu()
