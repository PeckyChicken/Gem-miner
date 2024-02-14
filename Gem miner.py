import inspect
from math import floor
from random import choice, choices, randint, shuffle
from statistics import mean
from time import sleep
from tkinter import *  # doing wildcard import to make it easier to use
from typing import Literal, Self

from animations import *
from classes import *
from constants import *
from functions import *
from images import *
from lines import *
from sounds import *

filepath = __file__+"/../"
with open(f"{filepath}/folder_name.txt") as f:
    folder_name = f.read()

card = None
fade = None

window.title(f"{folder_name}")
window.iconbitmap(filepath+f"{folder_name}/icon.ico")
window.resizable(0, 0)

gameover = False
squarey = SQUAREMARGINY

game_state = GameState()

cutscene = False
track = 0
busy = False
reqscore = 500
mode = "none"
display = False
selecting = False
mousex=mousey=0


music_on = True
sfx_on = True

c = Canvas(window,width=WIDTH,height=HEIGHT, bg="gray") #sets up canvas
c.pack(fill="both")
bg = PhotoImage(file = filepath+f"{folder_name}/Images/Backgrounds/bg.png")
bg_image = c.create_image(WIDTH/2,HEIGHT/2,image=bg)
highlight = [c.create_rectangle(5,7,6,8)]
c.delete(highlight[0])
highlight.clear()
try:
    with open(filepath+f"{folder_name}/highscore.txt","r+") as hsfile:
        highscore = hsfile.read()
        highscore = int(highscore.strip())
        hsfile.close()
except (FileNotFoundError, ValueError):
    highscore = 0

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coords = x,y

    def distance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

    def inside(self, p1, p2):
        return p1.x <= self.x <= p2.x and p1.y <= self.y <= p2.y

select_music = Music({music["mode_select"]:69818},window)
title_music = Music({music["titleA"]:13300,music["titleB"]:54850},window)
game_music = Music({music["survival1"]:52377},window)
game_music2 = Music({music["survival2"]:61075},window)
time_music = Music({music["timeA"]:40000,music["timeB"]:36000},window)
obstacle_music = Music({music["obstacle"]:56000},window)
game_over_music = Music({music["gameoverA"]:643,music["gameoverB"]:13714},window)
chroma_music = Music({music["chromablitz"]:57600},window)


title_music.play()


canplace = False
selcolor = 0

scoretext = c.create_text(40,20,text="Score",font=(FONT,10),state=HIDDEN,fill=TEXTCOL)
scoredisp = c.create_text(40,50,text=0,font=(FONT,31),state=HIDDEN,fill=TEXTCOL)

goaltext = c.create_text(40,100,text="Goal",font=(FONT,10),state=HIDDEN,fill=TEXTCOL)
goaldisp = c.create_text(40,130,text=500,font=(FONT,23),state=HIDDEN,fill=TEXTCOL)

leveltext = c.create_text(40,180,text="Level",font=(FONT,10),state=HIDDEN,fill=TEXTCOL)
leveldisp = c.create_text(40,210,text=1,font=(FONT,31),state=HIDDEN,fill=TEXTCOL)

colorselbox = [None,None]

frame = 0

gameovertext = c.create_text(WIDTH/2,HEIGHT/2-25,font=(FONT,50),fill=TEXTCOL)
finalscoretext = c.create_text(WIDTH/2,HEIGHT/2+25,font=(FONT,25),fill=TEXTCOL)
toasttext = c.create_text(WIDTH/2,HEIGHT/2 + 150,font=(FONT,15),text="Click again if you really want to restart.",state=HIDDEN,fill=TEXTCOL)

highscoretext = c.create_text(WIDTH-10,HEIGHT-20,font=(FONT,15),anchor="e",text=f"High score: {highscore}",fill="#916000")
clickcount = 0




titlebg = c.create_image(WIDTH/2,HEIGHT/2,image=backgrounds["bg"])


selected = c.create_image(470,50,image=UI["empty"],state=HIDDEN)

tutimage = c.create_image(WIDTH/2,HEIGHT/2,image=tut1,state=HIDDEN)

tools = [1,1,1,1,1] #sets up the tool squares
toolvalues = [1,1,1,1,1]

tooltext = c.create_text(470,100,text="Tools",font=(FONT,15),state=HIDDEN,fill=TEXTCOL)

class Tool:
    objects = []
    def __init__(self,image:PhotoImage,pos:int) -> None:
        self.objects.append(self)
        self.holder = c.create_image(470,(pos+1)*60+90,image=UI["tools_bg"],state=HIDDEN)
        self.image = c.create_image(470,(pos+1)*60+90,image=image,state=HIDDEN)
        self.value_display = c.create_text(490,(pos+1)*60+100,text='',font=(FONT,15),state=HIDDEN,fill=TEXTCOL)
        #self.value = 1
    def show(self):
        for item in (self.holder,self.image,self.value_display):
            c.itemconfig(item,state=NORMAL)
    def hide(self):
        for item in (self.holder,self.image,self.value_display):
            c.itemconfig(item,state=HIDDEN)

pickaxe = Tool(tool_images["pickaxe"],0)

axe = Tool(tool_images["axe"],1)

jackhammer = Tool(tool_images["jackhammer"],2)

star = Tool(tool_images["star"],3)

dice = Tool(tool_images["dice"],4)

bucket = Tool(tool_images["bucket"],3)

wand = Tool(tool_images["wand"],4)

indicator = c.create_image(0,0)

#Sets up the button squares
backsquare = c.create_image(25,375,image=UI["backbutton"],state=HIDDEN)
sfxsquare = c.create_image(25,425,image=UI["sfx_yes"])
musicsquare = c.create_image(25,475,image=UI["music_yes"])


#Buttons
grid = [0]*49 #defines the game board
pit = [randint(1,4),randint(1,4),randint(1,4)] #sets up the pit
pitobjects: list[Button] = list()

loop = 0

def get_pos(gridx,gridy):
    x = gridx*SQUARELEN+SQUAREMARGINX
    y = gridy*SQUARELEN+SQUAREMARGINY
    #Both of these are very similar, so I will talk about both together.
    #The gridx/y * squarelen works out the relative position of the square, then the distance from the wall is added on.
    #The distance from the wall is multiplied by the value so that the predicted position is in the center of the square.

    return x,y


#Makes all the title screen buttons
startb = GameButton("Start",-35,c,get_pos,window,False)
helpb = GameButton("How to play",35,c,get_pos,window,False)
fastb = GameButton("Fast Game",105,c,get_pos,window,True)

fastmode = False

survivalb = GameButton("Survival",-35,c,get_pos,window,True)
timeb = GameButton("Time Rush",35,c,get_pos,window,True)
obstacleb = GameButton("Obstacles",105,c,get_pos,window,True)
chromab = GameButton("Chromablitz",-105,c,get_pos,window,True)



playb = GameButton("Play again",95,c,get_pos,window,True)

started = False
helping = False
tutstage = 0

#*IDS
itemid = {0:UI["empty"],1:gems["red_gem"],2:gems["yellow_gem"],3:gems["green_gem"],4:gems["blue_gem"],5:tool_images["rocket_vertical"],6:tool_images["rocket_horizontal"],7:tool_images["red_diamond"],8:tool_images["yellow_diamond"],9:tool_images["green_diamond"],10:tool_images["blue_diamond"],11:tool_images["bomb"],12:bricks["bricks"],13:bricks["red_bricks"],14:bricks["yellow_bricks"],15:bricks["green_bricks"],16:bricks["blue_bricks"]} #sets up the item ids
'''1 is red, 2 is yellow, 3 is green, 4 is blue'''


board: list[Button] = list() #sets up the board
#Music loop


def draw_board():
    if not gameover:
        global board
        squarey = SQUAREMARGINY
        for object in board:
            c.delete(object) #deletes all current squares so we can redraw them
        board.clear()
        for square in range(len(grid)):
            xpos = SQUAREMARGINX+SQUARELEN*(square%GRIDROWS)+25
            ypos = (squarey+(floor(square/GRIDROWS)*SQUARESPACING))+25

            board.append(c.create_image(xpos, ypos, image=itemid[grid[square]]))
            #Draws the images via some complicated calculations. SQUARELEN is how big the images should be, and it is multiplying that by the square number to space it out.
            #It uses modulo to stop it going too far as the board is only 7x7. For the y it works out what row it is on and draws the image there. 
            #SQUAREMARGINX is how far it starts off the left of the screen.

def draw_tools():
    global tools
    tool_imgs = [pickaxe.image,axe.image,jackhammer.image,star.image,dice.image]
    toolvalues = [pickaxe.value_display,axe.value_display,jackhammer.value_display,star.value_display,dice.value_display]
    if mode == "chroma":
        tool_imgs[3], toolvalues[3] = bucket.image,bucket.value_display

    for tool, value in zip(tool_imgs,tools):
        #print(value)
        c.itemconfig(tool,state=[HIDDEN,NORMAL][value])
    for tool, value in zip(toolvalues,toolvalues):
        c.itemconfig(tool,text=str(value))
        if value > 1:
            c.itemconfig(tool,state=NORMAL)
        else:
            c.itemconfig(tool,state=HIDDEN)
    c.itemconfig(backsquare,state=NORMAL)

reserved = set()
itemid
def set_square(color,x,y,reserve=False):
    global board, reserved
    if reserve:
        reserved.add((x,y))
    else:
        if (x,y) in reserved:
            reserved.remove((x,y))
        itemid = y*GRIDROWS + x #works out the id of the list given the x and y
        grid[itemid] = color #replaces the current color with the new one
        draw_board()

def calc_reqscore(level):
    return (((level+1)%2)+1) * 500 * 10 ** (1+(level - 3) // 2)

def level_complete():
    
    # Different level system in obstacle mode
    if mode == "obstacle" and started:
        complete = 12 not in grid

    else:
        # Calculate required score for next level
        reqscore = calc_reqscore(game_state.level)
        complete = game_state.score >= reqscore
    return complete

def update_level(complete):
    global tools, reqscore, toolvalues

    if complete:
        game_state.level += 1
        if mode == "survival" and game_state.level % 10 == 0:
            play_sound_effect(sfx_on, sounds["you_know_not_what_this_is"])
        else:
            play_sound_effect(sfx_on, sounds["nextlevel"])
        
        if mode == "obstacle":
            toolvalues[randint(0, len(toolvalues)-1)] += 1
            tools[:] = [1 if i else 0 for i in toolvalues]
            game_state.moves += game_state.level
            for _ in range(game_state.level):
                set_brick()
            update_text(False)
        elif mode == "chroma":
            toolvalues = [min(value+1,5) for value in toolvalues]
            tools[:] = [1 if i else 0 for i in toolvalues]
        else:
            tools[:] = [1]*5
            toolvalues = [1]*5
        draw_tools()
        update_text(False)
        
        return True
    else:
        return False

            
def lookup(x,y):
    try:
        color = grid[y*GRIDROWS+x] #find the color of the grid square
        return color
    except IndexError:
        return 0

def Get_ID(x,y):
    return board[y*GRIDROWS+x]

def set_pit(color,pos):
    pit[pos] = color #changes color of the pit objects



def reset_color(): #sets a random square to a color
    set_square(randint(1,4),randint(0,6),randint(0,6))

def set_brick_2(color,x,y):
    set_square(12+color,x,y)
    gameover_check()

def set_brick(color=0): #sets a random square to a brick
    if 0 not in grid: return 1
    x, y = randint(0,6),randint(0,6)
    while lookup(x,y) != 0 and lookup not in reserved:
        x, y = randint(0,6),randint(0,6)
    set_square(12+color,x,y,reserve=True)
    draw_animation(x,y,brickplace,100,c,get_pos,window,event=lambda: set_brick_2(color,x,y))
    return 0

def play_place_sound(): #only putting it in a function by itself so i can call it from a window.after
    play_sound_effect(sfx_on,sounds["place"])

def time_rush():
    base_time = 1000
    loop3 = window.after(floor(base_time),time_rush)
    if gameover or gameover_check() or not started:
        c.itemconfig(bg_image,image=bg)
        window.after_cancel(loop3)
        return
    if grid.count(0) <= game_state.level%LEVELBRICKUPGRADE + 1 and not any(x in grid for x in [5,6,7,8,9,10,11]):
        if grid.count(0) == game_state.level%LEVELBRICKUPGRADE + 1:
            play_sound_effect(sfx_on,sounds["warning"])
        squares = []
        for idx,item in enumerate(grid):
            if item == 0:
                coords = get_pos(*get_2d_pos(idx))
                squares.append(c.create_image(coords[0]+SQUARELEN/2,coords[1]+SQUARELEN/2,image=UI["warning"]))
        for square in squares:
            flash(square,frames=[UI["warning"],UI["air"]],delete=True)
    if 0 in grid:
        play_sound_effect(sfx_on,sounds["brick_placed"])
    for _ in range(game_state.level//LEVELBRICKUPGRADE + 1):
        set_brick()
    if randint(1,LEVELBRICKUPGRADE) <=game_state.level%LEVELBRICKUPGRADE:
        set_brick()

def pausedloop(event:callable,times:int,pause:int,/,*,iteration=0) -> None:
    '''Repeats EVENT TIMES times with PAUSE milliseconds between each call.
    The current iteration will be passed to EVENT.
    '''
    event(iteration)
    iteration += 1
    if iteration < times:
        window.after(pause,lambda:pausedloop(event,times,pause,iteration=iteration))

def start_music():
    global repeats
    stop_music(window,mute=False)
    if music_on:
        if mode == "survival":
            [game_music,game_music2][track].play()
        elif mode == "time":
            repeats = 0
            time_music.play()
        elif mode == "obstacle":
            obstacle_music.play()
        elif mode == "chroma":
            chroma_music.play()

def start_part_2():
    global started, repeats, cutscene

    start_music()
    started = True
    cutscene = False
    if mode == "time":        
        #window.after(50,time_rush)
        time_rush()

    c.delete(card[0])
    c.delete(fade[0])
    if mode != "obstacle":
        for _ in range(4):
            if mode == 'chroma':
                set_brick(randint(1,4))
            else:
                set_brick(0)
    if mode == 'chroma':
        set_brick(randint(1,4))
    else:
        set_brick(0)

def start():
    global repeats,track,tools,toolvalues, cutscene, beathighscore, card, fade, starters
    reset_color()
    reset_color()
    draw_tools()
    draw_board()
    draw_pit()
    cutscene = True
    beathighscore = False
    toolholders = [pickaxe.holder,axe.holder,jackhammer.holder,star.holder,dice.holder]
    for holder in toolholders:
        c.itemconfig(holder,state=NORMAL)
    tools = toolvalues = [1]*5
    draw_tools()

    c.itemconfig(scoredisp,state=NORMAL)
    c.itemconfig(scoretext,state=NORMAL)

    c.itemconfig(leveldisp,state=NORMAL)
    c.itemconfig(leveltext,state=NORMAL)
    c.itemconfig(goaldisp,state=NORMAL)
    c.itemconfig(goaltext,state=NORMAL)

    c.itemconfig(tooltext,state=NORMAL)
    if mode == "obstacle":
        c.itemconfig(goaltext,text="Moves")
        c.itemconfig(goaldisp,text=str(game_state.moves))
    else:
        c.itemconfig(goaltext,text="Goal")

    c.itemconfig(selected,state=NORMAL)
    c.itemconfig(titlebg,state=HIDDEN)

    startb.set_visible(False)
    helpb.set_visible(False)
    survivalb.set_visible(False)
    chromab.set_visible(False)
    timeb.set_visible(False)
    obstacleb.set_visible(False)

    pit[:] = [randint(1,4),randint(1,4),randint(1,4)]
    draw_pit()

    fade = [c.create_image(WIDTH/2,HEIGHT/2,image=UI["fade"])]
    if mode == "obstacle":
        c.itemconfig(bg_image,image=backgrounds["obstacle_bg"])
        card = [c.create_image(WIDTH/2,HEIGHT/2,image=UI["obstacles_card"])]
    elif mode == "time":
        c.itemconfig(bg_image,image=backgrounds["time_bg"])
        card = [c.create_image(WIDTH/2,HEIGHT/2,image=UI["time_card"])]
    elif mode == "survival":
        c.itemconfig(bg_image,image=backgrounds["survival_bg"])
        card = [c.create_image(WIDTH/2,HEIGHT/2,image=UI["survival_card"])]
    elif mode == "chroma":
        c.itemconfig(bg_image,image=backgrounds["chroma_bg"])
        card = [c.create_image(WIDTH/2,HEIGHT/2,image=UI["chroma_card"])]

       
    c.itemconfig(highscoretext,state=HIDDEN)

    stop_music(window)
    if sfx_on:
        play_sound_effect(sfx_on,sounds["start"])
    track = randint(0,1)
    starters = [window.after(3600,start_part_2)]
    update_text(nextlevel=False)


def clear_board():
    global grid, busy
    busy = False
    toast("Board cleared!", 1)
    grid = [0]*49
    game_state.score += 500*game_state.level
    update_text()
    c.itemconfig(scoredisp,text=game_state.score)
    window.after(1000,reset_color)
    window.after(1000,reset_color)
    draw_board()
 
def reset_count():
    global clickcount
    clickcount = 0

def clear_toast():
    c.itemconfig(toasttext,state=HIDDEN)

def toast(msg,time=-1):
    c.itemconfig(toasttext,state=NORMAL,text=msg)
    if time >= 0:
        window.after(time*1000,clear_toast)

def ask_quit():
    global grid, clickcount, highscore, selcolor, gameover, tools, toolvalues, selecting, track, started, display
    
    play_sound_effect(sfx_on,sounds["click"])
    clickcount += 1
    toast("Click again if you want to return to the title.",2)
    if clickcount == 2:
        stop_sounds()
        clear_toast()
        if game_state.score > highscore:
            highscore = game_state.score
        with open(f"{folder_name}/highscore.txt","w+") as hsfile:
            hsfile.write(str(highscore))
            hsfile.close()
        stop_music(window)
        c.itemconfig(bg_image,image=bg)
        display = False
        started = False
        for starter in starters:
            window.after_cancel(starter)
        #Anything in these lists gets deleted or vanished
        for x in board+pitobjects:
            c.delete(x)
        for x in [scoredisp,scoretext,goaldisp,goaltext,leveldisp,leveltext,tooltext,selected,backsquare]:
            c.itemconfig(x,state=HIDDEN)
        for tool in Tool.objects:
            tool.hide()
        play_sound_effect(sfx_on,sounds["click"])
        if music_on:
            title_music.play()
        tools = [0]*5
        toolvalues = [0]*5
        update_text(False)
        grid = [0]*49
        selcolor = 0
        c.itemconfig(selected,image=UI["empty"])
        gameover = False
        c.itemconfig(titlebg,state=NORMAL)
        for button in [startb,helpb]:
            button.set_visible(True)
        
        c.itemconfig(scoredisp,text=game_state.score)
        c.itemconfig(gameovertext,text="")
        c.itemconfig(finalscoretext,text="")
        track = randint(0,1)
        game_state.reset()
    else:
        window.after(2000, reset_count)

def calc_font_size(text):
    return DEFAULTTEXTSIZE-len(text)*4

beathighscore = False

def update_text(nextlevel=True): #Updates the font size depending on how many points the player has.
    global highscore, beathighscore
    reqscore = calc_reqscore(game_state.level)

    c.itemconfig(scoredisp,font=(FONT,calc_font_size(str(game_state.score))))
    c.itemconfig(scoredisp,text=str(game_state.score))
    #if nextlevel:
    #    complete = level_complete()
    #    update_level(complete)
    if game_state.score >= highscore and not beathighscore and started:
        beathighscore = True
        play_sound_effect(sfx_on,sounds["highscore"])
        c.itemconfig(scoredisp,font=(FONT,calc_font_size(str(game_state.score))+5))
        window.after(250,lambda: c.itemconfig(scoredisp,font=(FONT,calc_font_size(str(game_state.score)))))
        highscore = game_state.score
        with open(f"{folder_name}/highscore.txt","w+") as hsfile:
            hsfile.write(str(highscore))
            hsfile.close()
    c.itemconfig(leveldisp,text=str(game_state.level))
    c.itemconfig(leveldisp,font=(FONT,calc_font_size(str(game_state.level))))
    
    if mode == "obstacle":
        c.itemconfig(goaldisp,text=str(game_state.moves))
        c.itemconfig(goaldisp,font=(FONT,calc_font_size(str(game_state.moves))))
    else:
        c.itemconfig(goaldisp,text=str(reqscore))
        c.itemconfig(goaldisp,font=(FONT,calc_font_size(str(reqscore))))

    for idx, value in enumerate(toolvalues):
        text = ''
        if value > 1: #Only write the value if it is greater than 1
            text = value
        #The list index is so python knows which value to modify
        c.itemconfig([pickaxe.value_display,axe.value_display,jackhammer.value_display,bucket.value_display,star.value_display,dice.value_display][idx],text=text)
        
update_text()


def disp_help():
    global helping
    c.itemconfig(titlebg,state=HIDDEN)
    startb.set_visible(False)
    helpb.set_visible(False)
    if tutstage == 1:
     c.itemconfig(tutimage,image=tut1,state=NORMAL)
    elif tutstage == 2:
        c.itemconfig(tutimage,image=tut2,state=NORMAL) 
    elif tutstage == 3:
        c.itemconfig(tutimage,image=tut3,state=NORMAL) 
    elif tutstage == 4:
        c.itemconfig(tutimage,image=tut4,state=NORMAL) 
    elif tutstage == 5:
        c.itemconfig(tutimage,image=tut5,state=NORMAL) 
    elif tutstage == 6:
        c.itemconfig(tutimage,image=tut6,state=NORMAL) 
    else: 
        c.itemconfig(tutimage,state=HIDDEN)
        helping = False
        c.itemconfig(bg,state=NORMAL)
        c.itemconfig(titlebg,state=NORMAL)
        startb.set_visible(True)
        helpb.set_visible(True)
#* HANDLING

def clear3x3(row,column):
    global sfx_on
    
    play_sound_effect(sfx_on,sounds["drillused"])
    
    #Clear all the vertical rows.
    clear_line("V",row-1,column,False)
    clear_line("V",row,column,False)
    clear_line("V",row+1,column,False)

    #Clear all the horizontal rows.
    clear_line("H",row,column-1,False)
    clear_line("H",row,column,False)
    clear_line("H",row,column+1,False)

def convert_colors(item,row,column,samesquare):
    global busy
    leftid = lookup(row-1,column)
    rightid = lookup(row+1,column)
    upid = lookup(row,column-1)
    downid = lookup(row,column+1)



    if samesquare:
        diamondx,diamondy = row,column
        
    else:
        #Calculates which square the diamond is on
        if 6 < leftid < 11:
            diamondx,diamondy = row-1,column
        elif 6 < rightid < 11:
                diamondx,diamondy = row+1,column
        elif 6 < upid < 11:
                diamondx,diamondy = row,column-1
        elif 6 < downid < 11:
                diamondx,diamondy = row,column+1
        else:
            print("ERROR ERROR SYSTEM OVERLOAD HUGE ERROR ARRRGGGGHHHHHHHH WHATS GOING ON WHY IS THIS HAPPENING AWFUL BUG FIX THIS RIGHT NOW!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    
    play_sound_effect(sfx_on,sounds["diamondused"])
    
    for i in range(len(grid)):
        if grid[i] == lookup(diamondx,diamondy)-6: #sets all colors of the same to the item
            x,y = get_2d_pos(i)
            draw_animation(x,y,smokes[lookup(x,y)],100,c,get_pos,window)
            set_square(11 if item == "bomb" else randint(5,6),x,y)
            game_state.score += 10*game_state.level
            update_text()
    complete = level_complete()
    update_level(complete)
    busy = False
    draw_animation(diamondx,diamondy,smokes[lookup(diamondx,diamondy)-6],100,c,get_pos,window)
    set_square(11 if item == "bomb" else randint(5,6),diamondx,diamondy)

def clear_2_lines(row,column):
    play_sound_effect(sfx_on,sounds["drillused"])
    clear_line("V",row,column,False)
    clear_line("H",row,column,False)

def big_bang(row,column):
    game_state.score += 50*game_state.level
    explode(row,column,3)
    set_square(0,row,column)

def handle_items(item,row,column):
    global busy
    leftid = lookup(row-1,column)
    rightid = lookup(row+1,column)
    upid = lookup(row,column-1)
    downid = lookup(row,column+1)
    #Checks if there is a diamond next to it
    if 6 < leftid < 11 or 6 < rightid < 11\
        or 6 < upid < 11 or 6 < downid < 11:
        if item == 'diamond':
            
            play_sound_effect(sfx_on,sounds["clearall"])
            window.after(3000,clear_board)
            return True
        convert_colors(item,row,column,False)

        return True
    
    #Checks if there is a bomb next to it
    elif 11 in (leftid,rightid,upid,downid):
        if item == "diamond":
            convert_colors("bomb",row,column,True)
            busy = False
            return True
        if item == "bomb":
            big_bang(row,column)
            return True
        clear3x3(row,column)
        return True

    #Checks if there is a drill next to it
    elif leftid in (5,6) or rightid in (5,6)\
        or downid in (5,6) or upid in (5,6):
        if item == "diamond":
            convert_colors("hdrill",row,column,True)
            busy = False
            return True
        if item == "bomb":
            clear3x3(row,column)
            return True
        clear_2_lines(row,column)
        return True


    #update_text()
    return False

def get_2d_pos(index):
    return index%7, index//7

def clear_colors(row,column):
    global busy, tools, toolvalues
    play_sound_effect(sfx_on,sounds["diamondused"])
    busy = False
    square = lookup(row,column)-6
    play_sound_effect(sfx_on,sounds["break"])
    soundplayed = False
    for i in range(len(grid)):
        if grid[i] == lookup(row,column)-6: #sets all colors of the same to gray
            currow, curcolumn = get_2d_pos(i)
            if mode == "chroma":
                soundplayed = clear_bricks((currow,curcolumn),soundplayed,color=square)
            else:
                soundplayed = clear_bricks((currow,curcolumn),soundplayed,color=0)
            draw_animation(currow,curcolumn,smokes[lookup(currow,curcolumn)],100,c,get_pos,window)
            
            set_square(0,currow,curcolumn)
            game_state.score += 10*game_state.level
            c.itemconfig(scoredisp,text=game_state.score)
            update_text()

    if mode == "chroma":
        print("")
    game_state.score += 100*game_state.level
    
    update_text()
    c.itemconfig(scoredisp,text=game_state.score)
    draw_animation(row,column,smokes[lookup(row,column)-6],100,c,get_pos,window)
    set_square(0,row,column) #removes the current diamond
    if all(0==x for x in grid):
        game_state.score += 50*game_state.level
        c.itemconfig(scoredisp,text=game_state.score)
        window.after(1000,reset_color)
        window.after(1000,play_place_sound)
        update_text()

    complete = level_complete()
    update_level(complete)


def clear_line(direction,row,column,sound=True):

    if sound:
        play_sound_effect(sfx_on,sounds["drillused"])
    queue: callable = []
    def clearself(square):
        delete = True
        curx, cury = square if direction == "H" else row, square if direction == "V" else column
        cursquare = lookup(curx,cury)
        draw_animation(curx,cury,smokes[0],100,c,get_pos,window)
        if cursquare != 0:
            game_state.score += 10*game_state.level
            
            if cursquare == 12:
                play_sound_effect(sfx_on,sounds["brick_break"])
            else:
                play_sound_effect(sfx_on,sounds["break"])
            update_text()
            c.itemconfig(scoredisp,text=game_state.score)

            if (curx,cury) != (row,column):
                func, functype = chain(curx, cury)
                if func is not None:
                    if functype in ("bomb"):
                        func()
                    else:
                        delete = False
                        queue.append(func)
        if delete:      
            set_square(0,curx,cury) #sets all squares in the column to blank
    pausedloop(clearself,GRIDROWS,50)
    for item in queue:
        item()
    if all(0==x for x in grid):
        game_state.score += 50*game_state.level
        update_text()
        c.itemconfig(scoredisp,text=game_state.score)
        window.after(1000,reset_color)
        window.after(1000,play_place_sound)


def close():
    global highscore
    if game_state.score > highscore:
        highscore = game_state.score
        with open(f"{folder_name}/highscore.txt","w+") as hsfile:
            hsfile.write(str(highscore))
            hsfile.close()
    window.destroy()

def pick_color(row):
    global canplace, tools, selcolor
    if row not in [0,3,6]: return
    clear_toast()
    clear_dice_prev()
    tools = [1 if elem==2 else elem for elem in tools]
    canplace = True #make sure that the player can place a color
    c.itemconfig(pitobjects[row//3],image=itemid[selcolor]) #sets the color to gray temporarily
    selcolor, pit[row//3] = pit[row//3], selcolor #swaps the selected color with the one in the pit
    c.itemconfig(selected,image=itemid[selcolor]) #fills the selected box with whatever color was chosen
    canplace = bool(selcolor)
    motion("This isn't needed",True)

def key_press(event):
    key = event.keysym
    if key in '123' and started and not gameover:
        keyvalue = int(key)-1
        pick_color(keyvalue*3)

def switchcolors(row,column,color):
    brick = lookup(row, column)
    if not 12 <= brick <= 16:
        print("Not a brick")
        return

    def change_color(brick, new_color):
        global grid
        play_sound_effect(sfx_on, sounds["bucketused"])
        game_state.score += 10*game_state.level
        idx = grid.index(brick)

        grid[idx] = new_color
        complete = level_complete()
        update_level(complete)
        draw_board()


    pausedloop(lambda _: change_color(brick, color), grid.count(brick), 100)

storedcoords = []
choosing = False

def motion(event,outside=False):
    global indicator,mousex,mousey,highlight,tempmousex,tempmousey
    for item in highlight:
        c.delete(item)
    highlight.clear()
    tempmousex, tempmousey = mousex,mousey
    if outside:
        tempmousex -= SQUARELEN/2
        tempmousey -= SQUARELEN/2
    else:
        mousex = event.x
        mousey = event.y #get mouse x and y
    row = floor((mousex-SQUAREMARGINY)//49-1)
    column = floor((mousey-SQUAREMARGINX)//49+1) #work out row and column of hovered space
    pos = get_pos(row,column)
    c.moveto(indicator,pos[0]+SQUARELEN*outside/2,pos[1]+SQUARELEN*outside/2)
    
    if can_place(row,column):
        if selcolor != 0:

            if lookup(row,column) != 0:
                c.itemconfig(indicator,state=HIDDEN)
                return
            if not all((lookup(row,column) == 0,
                        (
                            any((
                        (row > 0 and lookup(row-1,column)),
                        (row < 6 and lookup(row+1,column)),
                        (column < 6 and lookup(row,column+1)),
                        (column > 0 and lookup(row,column-1))))
                        ))):
                c.itemconfig(indicator,image=UI["cross"],state=NORMAL)
                return

            lines, direction, _, _ = detect_line(row,column,lookup,special=True,color=selcolor)

            if direction == "HV":
                icon = tool_images["bomb"]
            elif direction == '0' or len(lines) <= 3:
                icon = itemid[selcolor]
            elif len(lines) == 5:
                icon = itemid[selcolor+6]
            elif len(lines) == 4:
                icon = itemid[5 + (direction == "V")]
            for square in lines:
                #print(f"Row/Column, {(row,column)}. Square, {(square)}")
                if square != [row,column]:
                    highlight.append(c.create_image(get_pos(*square)[0]+SQUARELEN/2,get_pos(*square)[1]+SQUARELEN/2,image=UI["empty"]))
            c.itemconfig(indicator,image=icon,state=NORMAL)
        elif 2 in tools:
            hovered = lookup(row,column)
            if tools[0] == 2:
                if lookup(row,column) == 0:
                    highlight.append(c.create_image(get_pos(row,column)[0]+SQUARELEN/2,get_pos(row,column)[1]+SQUARELEN/2,image=UI["cross"]))
                else:
                    highlight.append(c.create_image(get_pos(row,column)[0]+SQUARELEN/2,get_pos(row,column)[1]+SQUARELEN/2,image=UI["empty"]))
            elif tools[1] == 2:
                for square in [(i,column) for i in range(7)]:
                    highlight.append(c.create_image(get_pos(*square)[0]+SQUARELEN/2,get_pos(*square)[1]+SQUARELEN/2,image=UI["empty"]))
            elif tools[2] == 2:
                for square in [(row,i) for i in range(7)]:
                    highlight.append(c.create_image(get_pos(*square)[0]+SQUARELEN/2,get_pos(*square)[1]+SQUARELEN/2,image=UI["empty"]))
            elif tools[3] == 2:
                if mode == "chroma":

                    if hovered in (13,14,15,16):
                        for currow in range(7):
                            for curcolumn in range(7):
                                square = (currow,curcolumn)
                                if lookup(*square) == hovered:
                                    highlight.append(c.create_image(get_pos(*square)[0]+SQUARELEN/2,get_pos(*square)[1]+SQUARELEN/2,image=UI["empty"]))
                    else:
                        highlight.append(c.create_image(get_pos(row,column)[0]+SQUARELEN/2,get_pos(row,column)[1]+SQUARELEN/2,image=UI["cross"]))
                else:
                    for square in [(row,i) for i in range(7)]+[(i,column) for i in range(7)]+clear_diagonal_lines(row,column,False):
                        #if square != [row,column]:
                        highlight.append(c.create_image(get_pos(*square)[0]+SQUARELEN/2,get_pos(*square)[1]+SQUARELEN/2,image=UI["empty"]))
            
        else: c.itemconfig(indicator,state=HIDDEN)
    else:
        c.itemconfig(indicator,state=HIDDEN)

def flash(item,rate=0.15,/,*,times=0,pulse=False,delete=False,frames=[None]):
    if pulse:
        if frames[0] is None:
            c.itemconfig(item,fill="#FF0000")
        else:
            c.itemconfig(item,image=frames[0])
        times += 1
    else:
        if frames[0] is None:
            c.itemconfig(item,fill=TEXTCOL)
        else:
            c.itemconfig(item,image=frames[1])
    pulse = not pulse
    if times < 4:
        window.after(round(rate*1000),lambda: flash(item,rate,times=times,pulse=pulse,frames=frames,delete=delete))
    else:
        if frames[0] is None:
            c.itemconfig(item,fill=TEXTCOL)
        else:
            c.itemconfig(item,image=frames[1])
        if delete:
            c.delete(item)

redzone = (125,245,175,395)
yellowzone = (190,245,240,395)
greenzone = (260,245,310,395)
bluezone = (330,245,380,395)



diceprev = []
#Main event
def click(event):
    global selcolor,diceprev, pit, canplace, pitobjects, grid, gameover, tools, started, helping, tutstage, highscore, music_on, sfx_on, repeats, busy, track, mode, selecting, toolvalues, storedcoords, choosing, colorselbox

    complete = level_complete()
    update_level(complete)
    mouseb = event.num
    # print(mousex,mousey)

    if choosing:
        choosing = False
        toolvalues[3] -= 1
        for item in colorselbox:
            c.delete(item)
        colorselbox[:] = [None]*2
        if toolvalues[3] == 0:
            tools[3] = 0
            c.itemconfig(bucket.image,state=HIDDEN)
        else:
            tools[3] = 1
        if inside(*redzone,mousex,mousey):
            if lookup(*storedcoords) == 13:
                return
            switchcolors(*storedcoords,13)

        elif inside(*yellowzone,mousex,mousey):
            if lookup(*storedcoords) == 14:
                return
            switchcolors(*storedcoords,14)

        elif inside(*greenzone,mousex,mousey):
            if lookup(*storedcoords) == 15:
                return
            switchcolors(*storedcoords,15)

        elif inside(*bluezone,mousex,mousey):
            if lookup(*storedcoords) == 16:
                return
            switchcolors(*storedcoords,16)
        else:
            toolvalues[3] = 1
            c.itemconfig(bucket.image,state=NORMAL)
            tools[3] = 1

            return
        


        return

    if cutscene:
        window.after_cancel(starters[0])
        #window.after_cancel(starters[1])
        stop_sounds()
        #start_music()
            
        start_part_2()
        
    if helping:
        tutstage += 1
        
        play_sound_effect(sfx_on,sounds["click"])
        disp_help()
        return

    if inside(0,450,50,500,mousex,mousey): #Is music clicked?
        if music_on:
            music_on = False
            
            play_sound_effect(sfx_on,sounds["click"])
            if not gameover or (gameover and not sfx_on):
                stop_music(window,mute=True)
            
            c.itemconfig(musicsquare, image = UI["music_no"])
        else:
            music_on = True

            for channel in channels:
                channel.set_volume(1)
            play_sound_effect(sfx_on,sounds["click"])

            c.itemconfig(musicsquare, image = UI["music_yes"])

    if inside(0,400,50,450,mousex,mousey): #Is sfx clicked?
        if sfx_on:
            sfx_on = False
            if gameover and not music_on:
                stop_music(window)
            c.itemconfig(sfxsquare, image = UI["music_no"])
        else:
            sfx_on = True
            if gameover and not music_on:
                game_over_music.play()
            play_sound_effect(sfx_on,sounds["click"])
            c.itemconfig(sfxsquare, image = UI["sfx_yes"])
    
    if started:
        if gameover and playb.is_clicked(mousex,mousey): #if the game is over run it again
            stop_music(window)
            playb.set_visible(False)
            #Anything in these lists gets deleted or vanished
            for x in board+pitobjects:
                c.delete(x)
            for x in [scoredisp,scoretext,goaldisp,goaltext,leveldisp,leveltext,tooltext,selected,backsquare]:
                c.itemconfig(x,state=HIDDEN)
            for tool in Tool.objects:
                tool.hide()
            selecting = True
            display_modes(True)
            play_sound_effect(sfx_on,sounds["click"])
            grid = [0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0]
            selcolor = 0
            c.itemconfig(selected,image=UI["empty"])
            gameover = False
            c.itemconfig(scoredisp,text=game_state.score)
            c.itemconfig(gameovertext,text="")
            c.itemconfig(finalscoretext,text="")
            track = randint(0,1)
            game_state.reset()
            
            return


        #TODO: TURN THIS INTO A FUNCTION
        if inside(445,125,495,175,mousex,mousey) and tools[0] != 0: #is pickaxe clicked?
            clear_dice_prev()
            if tools[0] == 2:
                tools[0] = 1
                clear_toast()
                clear_selection()
                return
            
            play_sound_effect(sfx_on,sounds["toolselected"])
            if selcolor != 0:
                pit = [selcolor if elem==0 else elem for elem in pit]
                selcolor = 0
                canplace = False
                draw_pit()
            c.itemconfig(selected,image=tool_images["pickaxe"])
            tools = [1 if elem==2 else elem for elem in tools]
            tools[0] = 2
            toast("The Pickaxe clears the square you click on.")
            return
        if inside(445,185,495,235,mousex,mousey) and tools[1] != 0: #is throwing axe clicked?
            clear_dice_prev()
            if tools[1] == 2:
                tools[1] = 1
                clear_toast()
                clear_selection()
                return
            
            play_sound_effect(sfx_on,sounds["toolselected"])
            if selcolor != 0:
                pit = [selcolor if elem==0 else elem for elem in pit]
                selcolor = 0
                canplace = False
                draw_pit()
            tools = [1 if elem==2 else elem for elem in tools]
            tools[1] = 2
            c.itemconfig(selected,image=tool_images["axe"])
            toast("Click on any square to clear a row with the Axe.")
            return
        if inside(445,245,495,295,mousex,mousey) and tools[2] != 0: #is jackhammer clicked?
            clear_dice_prev()
            if tools[2] == 2:
                tools[2] = 1
                clear_toast()
                clear_selection()
                return
            
            play_sound_effect(sfx_on,sounds["toolselected"])
            if selcolor != 0:
                pit = [selcolor if elem==0 else elem for elem in pit]
                selcolor = 0
                canplace = False
                draw_pit()
            tools = [1 if elem==2 else elem for elem in tools]
            tools[2] = 2
            c.itemconfig(selected,image=tool_images["jackhammer"])
            toast("Clear a whole column with the Jackhammer.")
            return
        if inside(445,305,495,355,mousex,mousey) and tools[3] != 0: #is star or bucket clicked?
            clear_dice_prev()
            if tools[3] == 2:
                tools[3] = 1
                clear_toast()
                clear_selection()
                return
            play_sound_effect(sfx_on,sounds["toolselected"])
            if selcolor != 0:
                pit = [selcolor if elem==0 else elem for elem in pit]
                selcolor = 0
                canplace = False
                draw_pit()
            tools = [1 if elem==2 else elem for elem in tools]
            tools[3] = 2
            if mode == "chroma":
                c.itemconfig(selected,image=tool_images["bucket"])
                toast("The Bucket changes the color of bricks.")
            else:
                c.itemconfig(selected,image=tool_images["star"])
                toast("Clear a line in every direction from the Star.")
            return
        if inside(445,365,495,415,mousex,mousey) and tools[4] != 0: #is shuffle clicked?
            if tools[4] == 1:
                tools = [1 if elem==2 else elem for elem in tools]
                if selcolor != 0:
                    pit = [selcolor if elem==0 else elem for elem in pit]
                    selcolor = 0
                    canplace = False
                    draw_pit()
                #update_text()
                tools[4] = 2
                toast("Use the Dice to replenish your pit.")
                play_sound_effect(sfx_on,sounds["toolselected"])
                c.itemconfig(selected,image=tool_images["dice"])
                for square in [(0,8),(3,8),(6,8)]:
                    #if square != [row,column]:
                    diceprev.append(c.create_image(get_pos(*square)[0]+SQUARELEN/2,get_pos(*square)[1]+SQUARELEN/2,image=UI["empty"]))
                return
            shuffle_pit()

        #* BUTTONS
        if inside(0,350,50,400,mousex,mousey): #Is back button clicked?
            ask_quit()

        row = floor((mousex-SQUAREMARGINY)//49-1) 
        column = floor((mousey-SQUAREMARGINX)//49+1) #work out row and column of clicked space
        if tools[0] == 2: #Removes the square for the pickaxe
            clear_toast()
            if row < 0 or row > 6 or column < 0 or column > 6:
                pass
            elif lookup (row,column) == 0:
                
                play_sound_effect(sfx_on,sounds["nomatch"])
            else:
                toolvalues[0] -= 1
                if toolvalues[0] == 0:
                    tools[0] = 0
                else:
                    tools[0] = 1
                c.itemconfig(pickaxe.image,state=HIDDEN)
                c.itemconfig(selected,image=UI["empty"])    
                
                play_sound_effect(sfx_on,sounds["pickaxeused"])
                draw_animation(row,column,smokes[0], 100,c,get_pos,window)
                if lookup(row,column) == 12:
                    play_sound_effect(sfx_on,sounds["brick_break"])
                else:
                    play_sound_effect(sfx_on,sounds["break"])
                game_state.score += 60*game_state.level
                c.itemconfig(scoredisp,text=game_state.score)
                set_square(0,row,column)
                complete = level_complete()
                update_level(complete)
                update_text()
                return
            
        if tools[1] == 2 and 0 <= column <= 6 and 0 <= row <= 6: #Removes the line for the throwing axe after checking that it is within bounds
            clear_toast()
            toolvalues[1] -= 1
            if toolvalues[1] == 0:
                tools[1] = 0
                c.itemconfig(axe.image,state=HIDDEN)
            else:
                tools[1] = 1
            c.itemconfig(selected,image=UI["empty"])
            
            play_sound_effect(sfx_on,sounds["axeused"])
            game_state.score += 120*game_state.level
            update_text()
            c.itemconfig(scoredisp,text=game_state.score)
            clear_line("H",row,column,False)
            complete = level_complete()
            update_level(complete)
            return
        
        if tools[2] == 2 and 0 <= column <= 6 and 0 <= row <= 6: #Removes the column for the jackhammer after checking that it is within bounds
            clear_toast()
            toolvalues[2] -= 1
            if toolvalues[2] == 0:
                tools[2] = 0
                c.itemconfig(jackhammer.image,state=HIDDEN)
            else:
                tools[2] = 1
            c.itemconfig(selected,image=UI["empty"])
            
            play_sound_effect(sfx_on,sounds["jackhammerused"])
            game_state.score += 120*game_state.level
            update_text()
            c.itemconfig(scoredisp,text=game_state.score)
            clear_line("V",row,column,False)
            complete = level_complete()
            update_level(complete)
            return
        if (tools[3] == 2 and 0 <= column <= 6 and 0 <= row <= 6 ) and (13 <= lookup(row,column) <= 16 if mode == "chroma" else True): #Clears the starline, or fills with the bucket, depending on the mode
            clear_toast()
            c.itemconfig(selected,image=UI["empty"])
            if mode == 'chroma':
                tools[3] = 0
                storedcoords[:] = [row,column]
                choosing = True
                colorselbox[0] = c.create_image(WIDTH/2,HEIGHT/2,image=UI["fade"])
                colorselbox[1] = c.create_image(WIDTH/2,HEIGHT/2,image=UI["colorselection"])

            else:
                toolvalues[3] -= 1
                if toolvalues[3] == 0:
                    tools[3] = 0
                    c.itemconfig(star.image,state=HIDDEN)
                else:
                    tools[3] = 1
                play_sound_effect(sfx_on,sounds["starused"])
                game_state.score += 300*game_state.level
                update_text()
                c.itemconfig(scoredisp,text=game_state.score)
                clear_line("V",row,column,sound=False)
                clear_line("H",row,column,sound=False)
                clear_diagonal_lines(row,column)
                complete = level_complete()
                update_level(complete)
                return
        try:
            if not busy:
                # *ITEM
                leftid = lookup(row-1,column)
                rightid = lookup(row+1,column)
                upid = lookup(row,column-1)
                downid = lookup(row,column+1)

                if lookup(row,column) == 5: #its a vdrill
                    busy = True
                    if handle_items("hdrill",row,column):
                        busy = False
                        return
                    clear_line("V",row,column)
                    busy = False
                    return

                if lookup(row,column) == 6: #its an hdrill
                    busy = True
                    if handle_items("hdrill",row,column):
                        busy = False
                        return
                    clear_line("H",row,column)
                    busy = False
                    return

                if lookup(row,column) > 6 and lookup(row,column) < 11: #its a diamond
                    busy = True
                    if handle_items("diamond",row,column): return
                    clear_colors(row,column)
                    return
                if lookup(row,column) == 11: #its a bomb
                    busy = True
                    if handle_items("bomb",row,column):
                        busy = False
                        return
                    game_state.score += 10*game_state.level
                    explode(row, column, 1)
                    busy = False
                    return
        except IndexError:
            pass
        if can_place(row, column) and selcolor != 0:
            # print(f'Row: {row}, Column: {column}, Row+1: {row+1}, Column+1: {column+1}, Row-1: {row-1}, Column-1: {column-1}')
            if lookup(row,column) == 0 and any((lookup(row-1,column), lookup(row+1,column), lookup(row,column+1), lookup(row,column-1))):
                pit = [randint(1,4) if elem==0 else elem for elem in pit]
                
                draw_pit()
                set_square(selcolor,row,column)
                if gameover_check():
                    return
                colorsel = selcolor
                selcolor = 0
                canplace = False
                c.itemconfig(selected,image=UI["empty"])
                lines, direction, num, linelens = detect_line(row,column,lookup) #detects any lines
                if mode == "obstacle":
                    game_state.moves -= 1
                    complete = level_complete()
                    update_level(complete)

                elif mode == "survival" or mode == "chroma":
                    if grid.count(0) <= game_state.level%LEVELBRICKUPGRADE + 1 and not any(x in grid for x in [5,6,7,8,9,10,11]):
                        play_sound_effect(sfx_on,sounds["warning"])
                        squares = []
                        for idx,item in enumerate(grid):
                            if item == 0:
                                coords = get_pos(*get_2d_pos(idx))
                                squares.append(c.create_image(coords[0]+SQUARELEN/2,coords[1]+SQUARELEN/2,image=UI["warning"]))
                        for square in squares:
                            flash(square,frames=[UI["warning"],UI["air"]],delete=True)
                tempx, tempy = row,column
                square = lookup(tempx,tempy)

                for line in lines: #if there are any lines
                    #* HANDLING LINES
                    set_square(0,line[0],line[1]) #clears all of the squares part of the line
                    game_state.score += 10*game_state.level
                    update_text()
                complete = level_complete()
                update_level(complete)
                if len (lines) >= 3:
                    if len(lines) == 3:
                        handle_gem_break(square, direction, num, tempx, tempy)
                    play_sound_effect(sfx_on,sounds["break"])
                    for item in highlight:
                        c.delete(item)
                    highlight.clear()
                    c.itemconfig(indicator, state=HIDDEN)
                if len(lines) == 4: #Finds the lines with 4 gems and changes them into a drill with the opposite direction as the line.
                    handle_drill_create(square, row, column,num, direction, tempx, tempy)
                    
                    play_sound_effect(sfx_on,sounds["drillcreated"])
                elif len(lines) == 5:
                    #finds the lines with 5 gems and changes them into a diamond
                    play_sound_effect(sfx_on,sounds["diamondcreated"])
                    diamonds = vdiamonds if direction == 'V' else hdiamonds
                    if colorsel == 1: #Red
                        draw_animation(row,column,diamonds["red"],100,c,get_pos,window,event=lambda:set_square(colorsel+6,row,column))
                    elif colorsel == 2: #Yellow
                        draw_animation(row,column,diamonds["yellow"],100,c,get_pos,window,event=lambda:set_square(colorsel+6,row,column))
                    elif colorsel == 3: #Green
                        draw_animation(row,column,diamonds["green"],100,c,get_pos,window,event=lambda:set_square(colorsel+6,row,column))
                    elif colorsel == 4: #Blue
                        draw_animation(row,column,diamonds["blue"],100,c,get_pos,window,event=lambda:set_square(colorsel+6,row,column))
                    
                elif direction == "HV": #finds the lines going in both directions, and makes a bomb
                    xpos, ypos = num
                    xlen, ylen = linelens
                    if xlen == 3:
                        handle_gem_break(square,"H",xpos,tempx,tempy,bomb=True)
                    else:
                        handle_drill_create(square,row,column,xpos,"H",tempx,tempy,bomb=True)
                    
                    if ylen == 3:
                        handle_gem_break(square,"V",ypos,tempx,tempy,bomb=True)
                    else:
                        handle_drill_create(square,row,column,ypos,"V",tempx,tempy,bomb=True)
                        
                    
                    play_sound_effect(sfx_on,sounds["bombcreated"])
                soundplayed = False
                #Need to go through all the lines again to remove all the bricks
                for line in lines:

                    soundplayed = clear_bricks(line,soundplayed,colorsel)

                c.itemconfig(scoredisp,text=game_state.score)
                if all(0==x for x in grid):
                    game_state.score += 50*game_state.level
                    update_text()
                    c.itemconfig(scoredisp,text=game_state.score)
                    window.after(1000,reset_color)
                    window.after(1000,play_place_sound)
                if len(lines) == 0:
                    play_place_sound()
                    game_state.score += game_state.level
                    update_text()
                    if mode in ("survival","chroma"):
                        if mode == "chroma":
                            color = randint(1,4)
                        else:
                            color = 0
                        #Add bricks to the board
                        for _ in range(game_state.level//LEVELBRICKUPGRADE + 1):
                            set_brick(color)
                        if randint(1,LEVELBRICKUPGRADE) < game_state.level%LEVELBRICKUPGRADE:
                            set_brick(color)
                complete = level_complete()
                update_level(complete)
                if game_state.moves <= 3:
                    if game_state.moves == 3:
                        play_sound_effect(sfx_on,sounds["warning"])
                    flash(goaldisp)
                if gameover_check():
                        return
            else:
                
                play_sound_effect(sfx_on,sounds["nomatch"])

            if gameover_check(): return
            draw_board()
        elif column == 8 and not gameover: #if not check if row is where the colors are and that they can choose a color
            pick_color(row)
            if selcolor == 0:
                canplace = False
    else:
        if display:
            if survivalb.is_clicked(mousex,mousey):
                play_sound_effect(sfx_on,sounds["click"])
                mode = "survival"
                start()

            if timeb.is_clicked(mousex,mousey):
                play_sound_effect(sfx_on,sounds["click"])
                mode = "time"
                start()

            if obstacleb.is_clicked(mousex,mousey):
                play_sound_effect(sfx_on,sounds["click"])
                mode = "obstacle"
                start()
            
            if chromab.is_clicked(mousex,mousey):
                play_sound_effect(sfx_on,sounds["click"])
                mode = "chroma"
                start()
        else:
            if startb.is_clicked(mousex,mousey):
                display_modes()
                play_sound_effect(sfx_on,sounds["click"])
            if helpb.is_clicked(mousex,mousey) and not helping:
                play_sound_effect(sfx_on,sounds["click"])
                helping = True
                tutstage = 1
                disp_help() 

def can_place(row, column):
    return row >= 0 and row < GRIDROWS and column >= 0 and column < GRIDROWS

def shuffle_pit():
    global tools,toolvalues
    clear_toast()
    tools = [1 if elem==2 else elem for elem in tools]
    clear_dice_prev()
    play_sound_effect(sfx_on,sounds["shuffleused"])
    c.itemconfig(scoredisp,text=game_state.score)

    #The program needs to find the best colors to set the pit to.
    colors = []
    lines = []
    values = []
    for x in range(0,7):
        for y in range(0,7):
            if lookup(x,y) in (0,12):
                for col in [1,2,3,4]:
                    line = detect_line(x,y,lookup,special=True,color=col)
                    if line[1] != '0' and not any(l in lines for l in line[0]):
                        lines.extend(line[0])
                        colors.append(col)
    if len(colors) == 0:
        clrs = [item for item in [1,2,3,4] if item in grid]
        if len(clrs) == 0:
            clr = randint(1,4)
        else:
            clr = choice(clrs)
        values.extend((clr,clr,randint(1,4)))

    elif len(colors) < 3:
        values[:] = colors
        for _ in range(3-len(values)):
            values.append(randint(1,4))
    else:
        values[:] = choices(colors,k=3)
    shuffle(values)
    toolvalues[4] -= 1
    if toolvalues[4] == 0:
        tools[4] = 0
        c.itemconfig(dice.image,state=HIDDEN)
    else:
        tools[4] = 1
    c.itemconfig(selected,image=UI["empty"])
    #sets the pit
    for item in pitobjects:
        c.delete(item)
    def finish(i):
        pit[:] = values
        draw_pit()
    for i in range(2,-1,-1):
        draw_animation(i*3,8,diceused,70,c,get_pos,window,event=lambda i=i: finish(i))

    gameover_check()

def handle_drill_create(square, row, column, num, direction, tempx, tempy,bomb=False):
    color = [None,"red","yellow","green","blue"][square]
    if direction == "H":
        pos = ["left","right"][num-1]
        draw_animation(tempx,tempy,hdrills[color][pos],100,c,get_pos,window,event=lambda: set_square(11 if bomb else 5,row,column))

    elif direction == "V":
        pos = ["top","bottom"][num-1]
        draw_animation(tempx,tempy,vdrills[color][pos],100,c,get_pos,window,event=lambda: set_square(11 if bomb else 6,row,column))

def handle_gem_break(square, direction, num, tempx, tempy,bomb=False):
    color = [None,"red","yellow","green","blue"][square]

    if direction == "H":
        pos = ["left","center","right"][num]
        draw_animation(tempx,tempy,hgembreaks[color][pos],500,c,get_pos,window,event=lambda tempx=tempx,tempy=tempy,bomb=bomb: finish(tempx, tempy, bomb))

    elif direction == "V":
        pos = ["top","center","bottom"][num]
        draw_animation(tempx,tempy,vgembreaks[color][pos],500,c,get_pos,window,event=lambda tempx=tempx,tempy=tempy,bomb=bomb: finish(tempx, tempy, bomb))

def finish(x,y,bomb):
    if bomb:
        set_square(11,x,y)
    else:
        draw_animation(x,y,gemvanish,100,c,get_pos,window)


def clear_dice_prev():
    for item in diceprev:
        c.delete(item)
    diceprev.clear()

def display_modes(music=False):
    global display, started
    if music and music_on:
        select_music.play()
    started = False
    display = True
    c.itemconfig(titlebg,state=HIDDEN)
    for item in [startb,helpb,fastb]:
        item.set_visible(FALSE)

    for item in [survivalb,timeb,obstacleb,chromab]:
        item.set_visible(True)

def clear_diagonal_lines(row,column,clear=True):
    currow = row
    curcolumn = column
    if not clear:
        squares = []
    while currow > 0 and curcolumn > 0:
        currow -= 1
        curcolumn -= 1
    def clearself(i):
        
        currow = i + row
        curcolumn = i + column
        
        if currow >= 7 or curcolumn >= 7:
            return

        if clear:
            if lookup(currow,curcolumn) == 12:
                #complete = level_complete()
                #update_level(complete)
                play_sound_effect(sfx_on,sounds["brick_break"])
            elif lookup(currow,curcolumn) != 0:
                play_sound_effect(sfx_on,sounds["break"])
            play_sound_effect(sfx_on,sounds["break"])
            set_square(0,currow,curcolumn)
            draw_animation(currow,curcolumn,smokes[0],100,c,get_pos,window)
        else:
            squares.append((currow,curcolumn))
    
    pausedloop(clearself,7,50)

    
    currow = row
    curcolumn = column

    while currow < 6 and curcolumn > 0:
        currow += 1
        curcolumn -= 1
    while currow >= 0 and curcolumn < 7:

        if clear:
            set_square(0,currow,curcolumn)
            draw_animation(currow,curcolumn,smokes[0],100,c,get_pos,window)
            if lookup(currow,curcolumn) == 12:
                complete = level_complete()
                update_level(complete)
                play_sound_effect(sfx_on,sounds["brick_break"])
            elif lookup(currow,curcolumn) != 0:
                play_sound_effect(sfx_on,sounds["break"])
        else:
            squares.append((currow,curcolumn))
        currow -= 1
        curcolumn += 1
    if not clear:
        return squares

def chain(x,y):
    cursquare = lookup(x,y)
    func: callable|None = None
    functype: str|None = None
    if cursquare == 5: 
        func = (lambda x=x,y=y: clear_line("V",x,y))
        functype = "line"
    if cursquare == 6:
        func = (lambda x=x,y=y: clear_line("H",x,y))
        functype = "line"
    if cursquare == 11:
        func = (lambda x=x,y=y: explode(x,y,1))
        functype = "bomb"
    if 7 <= cursquare <= 10:
        func = (lambda x=x,y=y: clear_colors(x,y))
        functype = "diamond"
    return func, functype

#print(explosions)
def explode(row, column, radius):
    queue = []
    play_sound_effect(sfx_on,sounds["boom"])
    for x in range(row-radius,row+radius+1):
        for y in range(column-radius,column+radius+1):
            if not(x < 0 or x > 6 or y < 0 or y > 6):
                func = None
                if (x,y) != (row,column):
                    func, _ = chain(x,y)
                if func is not None:
                    queue.append(func)
                else:
                    set_square(0,x,y)
                game_state.score += game_state.level
    set_square(0,row,column)
    draw_animation(row,column,explosions,75,c,get_pos,window)
    for item in queue:
        item()
    if all(0==x for x in grid):
        toast("Board cleared!", 1)
        game_state.score += 50*game_state.level
        update_text()
        c.itemconfig(scoredisp,text=game_state.score)
        window.after(1000,reset_color)
        window.after(1000,play_place_sound)
    #complete = level_complete()
    #update_level(complete)
    update_text()

def clear_bricks(gem,soundplayed=False,color=0):
    #This next part checks all the blocks around where the gem is.
    #If any bricks were there it breaks them
    x, y = gem[0], gem[1]+1
    soundplayed = breakbrick(x,y,not soundplayed,color) or soundplayed

    x, y = gem[0], gem[1]-1
    soundplayed = breakbrick(x,y,not soundplayed,color) or soundplayed

    x, y = gem[0]+1, gem[1]
    soundplayed = breakbrick(x,y,not soundplayed,color) or soundplayed

    x, y = gem[0]-1, gem[1]
    soundplayed = breakbrick(x,y,not soundplayed,color) or soundplayed
    return soundplayed


def breakbrick(x,y,sound,color):
    if lookup(x,y) == 12:
        if 0 <= y <= 6 and 0 <= x <= 6:
            set_square(0,x,y)
            draw_animation(x,y,brickbreaking,100,c,get_pos,window)
            if sound:
                play_sound_effect(sfx_on,sounds["brick_break"])
            #next_level()
            return True
    elif lookup(x,y) == color+12:
        if 0 <= y <= 6 and 0 <= x <= 6:
            set_square(0,x,y)
            draw_animation(x,y,brickbreaking,100,c,get_pos,window)
            if sound:
                play_sound_effect(sfx_on,sounds["brick_break"])
            #next_level()
            return True
    return False
def clear_selection():
    c.itemconfig(selected,image=UI["empty"])

#RETURN HERE
def gameover_check():
    global gameover, highscore, display, tools, toolvalues
    if (0 not in grid and any(x in grid for x in [5,6,7,8,9,10,11]) == 0) or (game_state.moves <= 0 and mode == "obstacle"):  #game is over
        stop_music(window)
        if music_on or sfx_on:
            game_over_music.play()
        tools = [0]*5
        toolvalues = [0]*5
        playb.set_visible(True)
        c.itemconfig(gameovertext,text="GAME OVER")
        c.itemconfig(finalscoretext, text="Your score was "+str(game_state.score))
        for square in board: #delete the grid so we can actually see the gameover text
            c.delete(square)
        gameover = True

        if game_state.score > highscore: 
            highscore = game_state.score
        with open(f"{folder_name}/highscore.txt","w+") as hsfile:
            hsfile.write(str(highscore))
            hsfile.close()
        update_text(False)
        return True #game is over
    return False #game is not over

def draw_pit():
    global pitobjects
    #delete everything in the pit
    for object in pitobjects:
        c.delete(object)
    pitobjects.clear()
    for square in range(len(pit)):
        pitobjects.append(c.create_image(SQUAREMARGINX+(square*PITSQUARESPACING)+25,
                PITSQUAREY+25,
                image=itemid[pit[square]]))
        #works out how to draw the pit


window.bind("<Button>",click)
window.bind("<Key>",key_press)
window.bind("<Motion>",motion)
window.protocol("WM_DELETE_WINDOW", close)

window.mainloop()
