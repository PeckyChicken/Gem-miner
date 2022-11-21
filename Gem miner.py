from math import floor
from random import choice, randint, shuffle
from statistics import mean
from time import sleep
from tkinter import *  # doing wildcard import to make it easier to use

from animations import *
from classes import *
from constants import *
from functions import *
from images import *
from lines import *
from sounds import *

filepath = __file__+"/../"



window.title("Gem miner")
window.iconbitmap(filepath+"Gem miner/icon.ico")
window.resizable(0, 0)

gameover = False
squarey = SQUAREMARGINY

moves = 15
score = 0
level = 1
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
bg = PhotoImage(file = filepath+"Gem miner/Images/Backgrounds/bg.png")
bg_image = c.create_image(WIDTH/2,HEIGHT/2,image=bg)
highlight = [c.create_rectangle(5,7,6,8)]
c.delete(highlight[0])
highlight.clear()
try:
    with open(filepath+"Gem miner/highscore.txt","r+") as hsfile:
        highscore = hsfile.read()
        highscore = int(highscore.strip())
        hsfile.close()
except (FileNotFoundError, ValueError):
    highscore = 0

select_music = Music({mode_select:69818},window)
title_music = Music({title1:13300,title2:54850},window)
game_music = Music({main1:52377},window)
game_music2 = Music({main2:61075},window)
time_music = Music({time1:8000,time2:32000},window)
obstacle_music = Music({obstacle:56000},window)
game_over_music = Music({gameover1:643,gameover2:13714},window)
chroma_music = Music({chromablitz:57600},window)

title_music.play()

canplace = False
selcolor = 0

scoretext = c.create_text(40,20,text="Score",font=(FONT,10),state=HIDDEN,fill=TEXTCOL)
scoredisp = c.create_text(40,50,text=0,font=(FONT,31),state=HIDDEN,fill=TEXTCOL)

goaltext = c.create_text(40,100,text="Goal",font=(FONT,10),state=HIDDEN,fill=TEXTCOL)
goaldisp = c.create_text(40,130,text=500,font=(FONT,23),state=HIDDEN,fill=TEXTCOL)

leveltext = c.create_text(40,180,text="Level",font=(FONT,10),state=HIDDEN,fill=TEXTCOL)
leveldisp = c.create_text(40,210,text=1,font=(FONT,31),state=HIDDEN,fill=TEXTCOL)


frame = 0

gameovertext = c.create_text(WIDTH/2,HEIGHT/2-25,font=(FONT,50),fill=TEXTCOL)
finalscoretext = c.create_text(WIDTH/2,HEIGHT/2+25,font=(FONT,25),fill=TEXTCOL)
toasttext = c.create_text(WIDTH/2,HEIGHT/2 + 150,font=(FONT,15),text="Click again if you really want to restart.",state=HIDDEN,fill=TEXTCOL)

highscoretext = c.create_text(WIDTH-10,HEIGHT-20,font=(FONT,15),anchor="e",text=f"High score: {highscore}",fill="#916000")
clickcount = 0




titlebg = c.create_image(WIDTH/2,HEIGHT/2,image=titlebgimage)


selected = c.create_image(470,50,image=empty_block,state=HIDDEN)

tutimage = c.create_image(WIDTH/2,HEIGHT/2,image=tut1,state=HIDDEN)





powerups = [1,1,1,1,1] #sets up the powerup squares
powerupvalues = [1,1,1,1,1]

pickaxesquare = c.create_image(470,150,image=pickaxe,state=HIDDEN)
pickvalue = c.create_text(490,180,text='',font=(FONT,15),state=HIDDEN,fill=TEXTCOL)

throwingaxesquare = c.create_image(470,210,image=throwingaxe,state=HIDDEN)
axevalue = c.create_text(490,240,text='',font=(FONT,15),state=HIDDEN,fill=TEXTCOL)

jackhammersquare = c.create_image(470,270,image=jackhammer,state=HIDDEN)
jackhammervalue = c.create_text(490,300,text='',font=(FONT,15),state=HIDDEN,fill=TEXTCOL)

starsquare = c.create_image(470,330,image=star,state=HIDDEN)
starvalue = c.create_text(490,360,text='',font=(FONT,15),state=HIDDEN,fill=TEXTCOL)

shufflesquare = c.create_image(470,390,image=dice,state=HIDDEN)
shufflevalue = c.create_text(490,420,text='',font=(FONT,15),state=HIDDEN,fill=TEXTCOL)

indicator = c.create_image(0,0)

#Sets up the button squares
restartsquare = c.create_image(25,375,image=restart,state=HIDDEN)
sfxsquare = c.create_image(25,425,image=sfx)
musicsquare = c.create_image(25,475,image=music)


#Buttons
grid = [0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,
        0,0,0,0,0,0,0] #defines the game board
pit = [randint(1,4),randint(1,4),randint(1,4)] #sets up the pit
pitobjects: list[Button] = list()

loop = 0




#Makes all the title screen buttons
startb = GameButton("Start",-35,c,False)
helpb = GameButton("How to play",35,c,False)
fastb = GameButton("Fast Game",105,c,True)

fastmode = False

survivalb = GameButton("Survival",-35,c,True)
timeb = GameButton("Time Rush",35,c,True)
obstacleb = GameButton("Obstacles",105,c,True)
chromab = GameButton("Chromablitz",-105,c,True)



playb = GameButton("Play again",95,c,True)

started = False
helping = False
tutstage = 0

#*IDS
itemid = {0:empty_block,1:red_block,2:yellow_block,3:green_block,4:blue_block,5:vdrill,6:hdrill,7:red_diamond,8:yellow_diamond,9:green_diamond,10:blue_diamond,11:bomb,12:bricks} #sets up the item ids
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

def draw_powerups():
    global pickaxesquare, throwingaxesquare, jackhammersquare, starsquare, shufflesquare, powerups
    tools = [pickaxesquare,throwingaxesquare,jackhammersquare,starsquare,shufflesquare]
    toolvalues = [pickvalue,axevalue,jackhammervalue,starvalue,shufflevalue]
    for tool, value in zip(tools,powerups):
        c.itemconfig(tool,state=[HIDDEN,NORMAL][value])

    for tool, value in zip(toolvalues,powerupvalues):
        c.itemconfig(tool,text=str(value))
        if value > 1:
            c.itemconfig(tool,state=NORMAL)
        else:
            c.itemconfig(tool,state=HIDDEN)
    c.itemconfig(restartsquare,state=NORMAL)
    
reserved = set()

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

def next_level():
    global level, powerups, reqscore, powerupvalues, moves, grid
    if mode == "obstacle" and started: #Different level system in obstacle mode
        level_complete = 12 not in grid
    else:
        #This complicated setup means that the player will advance a level when they get to 500, 1000, 5000, etc.
        reqscore = (((level+1)%2)+1) * 500 * 10 ** (1+(level - 3) // 2)
        level_complete = score >= reqscore
    if level_complete:
        level += 1
        if mode == "survival" and level%10 == 0:
            play_sound_effect(sfx_on,specialadvance)
        else:
            play_sound_effect(sfx_on,advance)
        if mode == "obstacle":
            powerupvalues[randint(0,len(powerupvalues)-1)] += 1
            powerups[:] = [1 if i else 0 for i in powerupvalues]
        elif mode == "chroma":
            indices = set()
            for index,item in enumerate(grid):
                if item == 12:
                    indices.add(index)
            for _ in range(level):
                index = choice(list(indices))
                indices.remove(index)
                tempx, tempy = index//7, index%7
                breakbrick(tempx,tempy,True)
        else:
            powerups = [1]*5
            powerupvalues = [1]*5
        draw_powerups()
        if mode == "obstacle":
            moves += level
            update_text(False)
            for _ in range(level):
                set_brick()
        update_text(False)
        return True
    return False
            
def lookup(x,y):
    try:
        color = grid[y*GRIDROWS+x] #find the color of the grid square
        return color
    except IndexError:
        return 0

def Get_ID(x,y):
    return board[y*GRIDROWS+x]

def get_pos(gridx,gridy):
    x = gridx*SQUARELEN+SQUAREMARGINX
    y = gridy*SQUARELEN+SQUAREMARGINY
    #Both of these are very similar, so I will talk about both together.
    #The gridx/y * squarelen works out the relative position of the square, then the distance from the wall is added on.
    #The distance from the wall is multiplied by the value so that the predicted position is in the center of the square.

    return x,y

def set_pit(color,pos):
    pit[pos] = color #changes color of the pit objects



def reset_color(): #sets a random square to a color
    set_square(randint(1,4),randint(0,6),randint(0,6))

def set_brick(): #sets a random square to a brick
    if 0 not in grid: return 1
    x, y = randint(0,6),randint(0,6)
    while lookup(x,y) != 0 and lookup not in reserved:
        x, y = randint(0,6),randint(0,6)
    set_square(12,x,y,reserve=True)
    draw_animation(x,y,brickplace,100,c,get_pos,window,event=lambda: set_square(12,x,y))

    return 1

def play_place_sound(): #only putting it in a function by itself so i can call it from a window.after
    play_sound_effect(sfx_on,placed)

def time_rush():
    base_time = 1000
    loop3 = window.after(floor(base_time),time_rush)
    if gameover_check():
        c.itemconfig(bg_image,image=bg)
        window.after_cancel(loop3)
        return
    if 0 in grid:
        play_sound_effect(sfx_on,brickplaced)
    for _ in range(level):
        set_brick()

def time_bg(index = 0):
    #if not music_on:
        #play_sound_effect(sfx_on,clocktick)
    if gameover:
        return
    else:
        c.itemconfig(bg_image,image=time_bgs[index])
        window.after(500,time_bg,(index+1)%4) 

def start_part_2(card, fade):
    global started, repeats, cutscene
    started = True
    cutscene = False
    if mode == "time":
        time_bg()
        time_rush()
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
    c.delete(card[0])
    c.delete(fade[0])
    if mode != "obstacle":
        for _ in range(4):
            set_brick()
    set_brick()

def start():
    global repeats,track,powerups,powerupvalues, level, cutscene, beathighscore
    reset_color()
    reset_color()
    draw_powerups()
    draw_board()
    draw_pit()
    cutscene = True
    beathighscore = False

    powerups = powerupvalues = [1]*5
    draw_powerups()

    c.itemconfig(scoredisp,state=NORMAL)
    c.itemconfig(scoretext,state=NORMAL)

    c.itemconfig(leveldisp,state=NORMAL)
    c.itemconfig(leveltext,state=NORMAL)
    c.itemconfig(goaldisp,state=NORMAL)
    c.itemconfig(goaltext,state=NORMAL)

    if mode == "obstacle":
        c.itemconfig(goaltext,text="Moves")
        c.itemconfig(goaldisp,text=str(moves))
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

    fade = [c.create_image(WIDTH/2,HEIGHT/2,image=fade_image)]
    if mode == "obstacle":
        c.itemconfig(bg_image,image=obstacle_bg)
        card = [c.create_image(WIDTH/2,HEIGHT/2,image=obstaclecard)]
    elif mode == "time":
        c.itemconfig(bg_image,image=time_bgs[0])
        card = [c.create_image(WIDTH/2,HEIGHT/2,image=timecard)]
    elif mode == "survival":
        c.itemconfig(bg_image,image=survival_bg)
        card = [c.create_image(WIDTH/2,HEIGHT/2,image=survivalcard)]
    elif mode == "chroma":
        c.itemconfig(bg_image,image=chroma_bg)
        card = [c.create_image(WIDTH/2,HEIGHT/2,image=chromacard)]


    
    c.itemconfig(highscoretext,state=HIDDEN)

    stop_music(window)
    if sfx_on:
        play_sound_effect(sfx_on,startsound)
    track = randint(0,1)
    window.after(3600,start_part_2,card,fade)
    update_text(nextlevel=False)


def clear_board():
    global score, grid, busy
    busy = False
    toast("Board cleared!", 1)
    grid =  [0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,
            0,0,0,0,0,0,0]
    score += 500*level
    update_text()
    c.itemconfig(scoredisp,text=score)
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

def ask_close():
    global grid, clickcount, score, level, highscore, selcolor, gameover, powerups, powerupvalues
    
    play_sound_effect(sfx_on,clicked)
    clickcount += 1
    toast("Click again if you really want to restart.",2)
    if clickcount == 2:
        if score > highscore:
            highscore = score
        with open("Gem miner/highscore.txt","w+") as hsfile:
            hsfile.write(str(highscore))
            hsfile.close()
        grid = [0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,
            0,0,0,0,0,0,0]
        reset_color()
        reset_color()
        powerups = [1]*5
        powerupvalues = powerups
        draw_powerups()
        selcolor = 0
        c.itemconfig(selected,image=empty_block)
        score = 0
        level = 1
        update_text()
        gameover = False
        draw_board()
        c.itemconfig(scoredisp,text=score)
        c.itemconfig(gameovertext,text="")
        c.itemconfig(finalscoretext,text="")
        c.itemconfig(toasttext, state=HIDDEN)
        clickcount = 0
        return
    else:
        window.after(2000, reset_count)

def calc_font_size(text):
    return DEFAULTTEXTSIZE-len(text)*4

beathighscore = False

def update_text(nextlevel=True): #Updates the font size depending on how many points the player has.
    global highscore, beathighscore
    c.itemconfig(scoredisp,font=(FONT,calc_font_size(str(score))))
    c.itemconfig(scoredisp,text=str(score))
    if nextlevel:
        next_level()
    if score >= highscore and not beathighscore and started:
        beathighscore = True
        play_sound_effect(sfx_on,newhighscore)
        c.itemconfig(scoredisp,font=(FONT,calc_font_size(str(score))+5))
        window.after(250,lambda: c.itemconfig(scoredisp,font=(FONT,calc_font_size(str(score)))))
        highscore = score
        with open("Gem miner/highscore.txt","w+") as hsfile:
            hsfile.write(str(highscore))
            hsfile.close()
    c.itemconfig(leveldisp,text=str(level))
    c.itemconfig(leveldisp,font=(FONT,calc_font_size(str(level))))
    
    if mode == "obstacle":
        c.itemconfig(goaldisp,text=str(moves))
        c.itemconfig(goaldisp,font=(FONT,calc_font_size(str(moves))))
    else:
        c.itemconfig(goaldisp,text=str(reqscore))
        c.itemconfig(goaldisp,font=(FONT,calc_font_size(str(reqscore))))

    for idx, value in enumerate(powerupvalues):
        text = ''
        if value > 1: #Only write the value if it is greater than 1
            text = value
        #The list index is so python knows which value to modify
        c.itemconfig([pickvalue,axevalue,jackhammervalue,starvalue,shufflevalue][idx],text=text)
        
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
    global score, sfx_on
    
    play_sound_effect(sfx_on,drillused)
    
    #Clear all the vertical rows.
    clear_line("V",row-1,column,False)
    clear_line("V",row,column,False)
    clear_line("V",row+1,column,False)

    #Clear all the horizontal rows.
    clear_line("H",row,column-1,False)
    clear_line("H",row,column,False)
    clear_line("H",row,column+1,False)

def convert_colors(item,row,column,samesquare):
    global score, busy
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

    
    play_sound_effect(sfx_on,diamondused)
    
    for i in range(len(grid)):
        if grid[i] == lookup(diamondx,diamondy)-6: #sets all colors of the same to the item
            x = i%7
            y = i//7
            draw_animation(x,y,smokes[lookup(x,y)],100,c,get_pos,window)
            set_square(11 if item == "bomb" else randint(5,6),x,y)
            score += 10*level
            update_text()
    busy = False
    draw_animation(diamondx,diamondy,smokes[lookup(diamondx,diamondy)-6],100,c,get_pos,window)
    set_square(11 if item == "bomb" else randint(5,6),diamondx,diamondy)

def clear_2_lines(row,column):
    global score
    play_sound_effect(sfx_on,drillused)
    clear_line("V",row,column,False)
    clear_line("H",row,column,False)

def big_bang(row,column):
    global score
    score += 50*level
    explode(row,column,3)
    set_square(0,row,column)

def handle_items(item,row,column):
    global score, busy
    leftid = lookup(row-1,column)
    rightid = lookup(row+1,column)
    upid = lookup(row,column-1)
    downid = lookup(row,column+1)
    #Checks if there is a diamond next to it
    if 6 < leftid < 11 or 6 < rightid < 11\
        or 6 < upid < 11 or 6 < downid < 11:
        if item == 'diamond':
            
            play_sound_effect(sfx_on,clearall)
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


    update_text()
    return False


def clear_colors(row,column):
    global score, busy, powerups, powerupvalues
    play_sound_effect(sfx_on,diamondused)
    busy = False
    square = lookup(row,column)-6
    play_sound_effect(sfx_on,remove)
    for i in range(len(grid)):
        if grid[i] == lookup(row,column)-6: #sets all colors of the same to gray
            currow, curcolumn = i%7,floor(i/7)
            draw_animation(currow,curcolumn,smokes[lookup(currow,curcolumn)],75,c,get_pos,window)
            
            set_square(0,currow,curcolumn)
            score += 10*level
            c.itemconfig(scoredisp,text=score)
            update_text()
    if mode == "chroma":
        if square == 1:
            play_sound_effect(sfx_on,axeused)
            clear_line("V",row,column,False)
            clear_line("H",row,column,False)
        elif square == 2:
            play_sound_effect(sfx_on,axeused)
            clear_line(choice(["V","R"]),row,column,sound=False)
        elif square == 3:
            play_sound_effect(sfx_on,powerupselected)
            for _ in range(3):
                powerups = [0]*5
                powerupvalues = powerups
                draw_powerups()
                window.update()
                sleep(0.05)
                powerups = [1]*5
                powerupvalues = powerups
                draw_powerups()
                window.update()               
                sleep(0.05)
        elif square == 4:
            explode(row,column,1)
    score += 100*level
    
    update_text()
    c.itemconfig(scoredisp,text=score)
    draw_animation(row,column,smokes[lookup(row,column)-6],100,c,get_pos,window)
    set_square(0,row,column) #removes the current diamond
    if all(0==x for x in grid):
        score += 50*level
        update_text()
        c.itemconfig(scoredisp,text=score)
        window.after(1000,reset_color)
        window.after(1000,play_place_sound)
    update_text()

def clear_line(direction,row,column,sound=True):
    global score

    if sound:
        play_sound_effect(sfx_on,drillused)
    queue: callable = []
    for square in range(GRIDROWS):
        delete = True
        curx, cury = square if direction == "H" else row, square if direction == "V" else column
        cursquare = lookup(curx,cury)
        draw_animation(curx,cury,smokes[0],100,c,get_pos,window)
        if cursquare != 0:
            score += 10*level
            
            if cursquare == 12:
                next_level()
                play_sound_effect(sfx_on,brickbreak)
            else:
                play_sound_effect(sfx_on,remove)
            update_text()
            c.itemconfig(scoredisp,text=score)

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
    for item in queue:
        item()
    if all(0==x for x in grid):
        score += 50*level
        update_text()
        c.itemconfig(scoredisp,text=score)
        window.after(1000,reset_color)
        window.after(1000,play_place_sound)

def close():
    global highscore
    if score > highscore:
        highscore = score
        with open("Gem miner/highscore.txt","w+") as hsfile:
            hsfile.write(str(highscore))
            hsfile.close()
    window.destroy()

def pick_color(row):
    global canplace, powerups, selcolor
    if row not in [0,3,6]: return
    clear_toast()
    clear_dice_prev()
    powerups = [1 if elem==2 else elem for elem in powerups]
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

def motion(event,outside=False):
    global indicator,mousex,mousey,highlight
    for item in highlight:
        c.delete(item)
    highlight.clear()
    if not outside:
        mousex = event.x
        mousey = event.y #get mouse x and y

    row = floor((mousex-SQUAREMARGINY)//49-1)
    column = floor((mousey-SQUAREMARGINX)//49+1) #work out row and column of hovered space
    pos = get_pos(row,column)
    c.moveto(indicator,pos[0]+SQUARELEN*outside/2,pos[1]+SQUARELEN*outside/2)
    
    if all([GRIDROWS > row >= 0, GRIDROWS > column >= 0, started]):
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
                c.itemconfig(indicator,image=cross,state=NORMAL)
                return

            lines, direction, _ = detect_line(row,column,lookup,True,selcolor)

            if direction == "HV":
                icon = bomb
            elif direction == '0' or len(lines) <= 3:
                icon = itemid[selcolor]
            elif len(lines) == 5:
                icon = itemid[selcolor+6]
            elif len(lines) == 4:
                icon = itemid[5 + (direction == "V")]
            for square in lines:
                #print(f"Row/Column, {(row,column)}. Square, {(square)}")
                if square != [row,column]:
                    highlight.append(c.create_image(get_pos(*square)[0]+SQUARELEN/2,get_pos(*square)[1]+SQUARELEN/2,image=empty_block))
            c.itemconfig(indicator,image=icon,state=NORMAL)
        elif 2 in powerups:
            if powerups[0] == 2:
                if lookup(row,column) == 0:
                    highlight.append(c.create_image(get_pos(row,column)[0]+SQUARELEN/2,get_pos(row,column)[1]+SQUARELEN/2,image=cross))
                else:
                    highlight.append(c.create_image(get_pos(row,column)[0]+SQUARELEN/2,get_pos(row,column)[1]+SQUARELEN/2,image=empty_block))
            elif powerups[1] == 2:
                for square in [(i,column) for i in range(7)]:
                    #if square != [row,column]:
                    highlight.append(c.create_image(get_pos(*square)[0]+SQUARELEN/2,get_pos(*square)[1]+SQUARELEN/2,image=empty_block))
            elif powerups[2] == 2:
                for square in [(row,i) for i in range(7)]:
                    #if square != [row,column]:
                    highlight.append(c.create_image(get_pos(*square)[0]+SQUARELEN/2,get_pos(*square)[1]+SQUARELEN/2,image=empty_block))
            elif powerups[3] == 2:
                for square in [(row,i) for i in range(7)]+[(i,column) for i in range(7)]+clear_diagonal_lines(row,column,False):
                    #if square != [row,column]:
                    highlight.append(c.create_image(get_pos(*square)[0]+SQUARELEN/2,get_pos(*square)[1]+SQUARELEN/2,image=empty_block))
        else: c.itemconfig(indicator,state=HIDDEN)
    else:
        c.itemconfig(indicator,state=HIDDEN)

diceprev = []
#Main event
def click(event):
    global selcolor,diceprev, pit, canplace, pitobjects, grid, score, gameover, powerups, started, helping, tutstage, level, highscore, music_on, sfx_on, repeats, busy, track, mode, moves, selecting, powerupvalues

    next_level()
    mouseb = event.num
    # print(mousex,mousey)
    if helping:
        tutstage += 1
        
        play_sound_effect(sfx_on,clicked)
        disp_help()
        return

    if inside(0,450,50,500,mousex,mousey): #Is music clicked?
        if music_on:
            music_on = False
            
            play_sound_effect(sfx_on,clicked)
            if not gameover or (gameover and not sfx_on):
                stop_music(window)
            
            c.itemconfig(musicsquare, image = nomusic)
        else:
            music_on = True
            repeats = 0
            
            play_sound_effect(sfx_on,clicked)
            if started:
                if gameover:
                    if not sfx_on:
                        game_over_music.play()
                elif mode == "survival":
                    [game_music,game_music2][track].play()
                elif mode == "time":
                    repeats = 0
                    time_music.play()
                elif mode == "obstacle":
                    obstacle_music.play()
                elif mode == "chroma":
                    chroma_music.play()
            else:
                if selecting:
                    select_music.play()
                else:
                    title_music.play()
            c.itemconfig(musicsquare, image = music)

    if inside(0,400,50,450,mousex,mousey): #Is sfx clicked?
        if sfx_on:
            sfx_on = False
            if gameover and not music_on:
                stop_music(window)
            c.itemconfig(sfxsquare, image = nosfx)
        else:
            sfx_on = True
            if gameover and not music_on:
                game_over_music.play()
            play_sound_effect(sfx_on,clicked)
            c.itemconfig(sfxsquare, image = sfx)
    
    if started:
        if gameover and playb.is_clicked(mousex,mousey): #if the game is over run it again
            stop_music(window)
            playb.set_visible(False)
            #Anything in these lists gets deleted or vanished
            for x in board+pitobjects:
                c.delete(x)
            for x in [scoredisp,scoretext,goaldisp,goaltext,leveldisp,leveltext,selected,pickaxesquare,throwingaxesquare,jackhammersquare,starsquare,shufflesquare,restartsquare]:
                c.itemconfig(x,state=HIDDEN)
            selecting = True
            display_modes(True)
            play_sound_effect(sfx_on,clicked)
            grid = [0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0]
            selcolor = 0
            c.itemconfig(selected,image=empty_block)
            score = 0
            level = 1
            gameover = False
            c.itemconfig(scoredisp,text=score)
            c.itemconfig(gameovertext,text="")
            c.itemconfig(finalscoretext,text="")
            track = randint(0,1)
            moves = 15
            return


        #TODO: TURN THIS INTO A FUNCTION
        if inside(445,125,495,175,mousex,mousey) and powerups[0] != 0: #is pickaxe clicked?
            clear_dice_prev()
            if powerups[0] == 2:
                powerups[0] = 1
                clear_toast()
                clear_selection()
                return
            
            play_sound_effect(sfx_on,powerupselected)
            if selcolor != 0:
                pit = [selcolor if elem==0 else elem for elem in pit]
                selcolor = 0
                canplace = False
                draw_pit()
            c.itemconfig(selected,image=pickaxe)
            powerups = [1 if elem==2 else elem for elem in powerups]
            powerups[0] = 2
            toast("The Pickaxe clears the square you click on.")
            return
        if inside(445,185,495,235,mousex,mousey) and powerups[1] != 0: #is throwing axe clicked?
            clear_dice_prev()
            if powerups[1] == 2:
                powerups[1] = 1
                clear_toast()
                clear_selection()
                return
            
            play_sound_effect(sfx_on,powerupselected)
            if selcolor != 0:
                pit = [selcolor if elem==0 else elem for elem in pit]
                selcolor = 0
                canplace = False
                draw_pit()
            powerups = [1 if elem==2 else elem for elem in powerups]
            powerups[1] = 2
            c.itemconfig(selected,image=throwingaxe)
            toast("Click on any square to clear a row with the Axe.")
            return
        if inside(445,245,495,295,mousex,mousey) and powerups[2] != 0: #is jackhammer clicked?
            clear_dice_prev()
            if powerups[2] == 2:
                powerups[2] = 1
                clear_toast()
                clear_selection()
                return
            
            play_sound_effect(sfx_on,powerupselected)
            if selcolor != 0:
                pit = [selcolor if elem==0 else elem for elem in pit]
                selcolor = 0
                canplace = False
                draw_pit()
            powerups = [1 if elem==2 else elem for elem in powerups]
            powerups[2] = 2
            c.itemconfig(selected,image=jackhammer)
            toast("Clear a whole column with the Jackhammer.")
            return
        if inside(445,305,495,355,mousex,mousey) and powerups[3] != 0: #is star clicked?
            clear_dice_prev()
            if powerups[3] == 2:
                powerups[3] = 1
                clear_toast()
                clear_selection()
                return
            play_sound_effect(sfx_on,powerupselected)
            if selcolor != 0:
                pit = [selcolor if elem==0 else elem for elem in pit]
                selcolor = 0
                canplace = False
                draw_pit()
            powerups = [1 if elem==2 else elem for elem in powerups]
            powerups[3] = 2
            c.itemconfig(selected,image=star)
            toast("Clear a line in every direction from the Star.")
            return
        if inside(445,365,495,415,mousex,mousey) and powerups[4] != 0: #is shuffle clicked?
            if powerups[4] == 1:
                powerups = [1 if elem==2 else elem for elem in powerups]
                if selcolor != 0:
                    pit = [selcolor if elem==0 else elem for elem in pit]
                    selcolor = 0
                    canplace = False
                    draw_pit()
                update_text()
                powerups[4] = 2
                toast("Use the Dice to replenish your pit.")
                play_sound_effect(sfx_on,powerupselected)
                c.itemconfig(selected,image=dice)
                for square in [(0,8),(3,8),(6,8)]:
                    #if square != [row,column]:
                    diceprev.append(c.create_image(get_pos(*square)[0]+SQUARELEN/2,get_pos(*square)[1]+SQUARELEN/2,image=empty_block))
                return
            clear_toast()
            powerups = [1 if elem==2 else elem for elem in powerups]
            clear_dice_prev()
            play_sound_effect(sfx_on,shufflesound)
            c.itemconfig(scoredisp,text=score)
            

            powerupvalues[4] -= 1
            if powerupvalues[4] == 0:
                powerups[4] = 0
                c.itemconfig(shufflesquare,state=HIDDEN)
            else:
                powerups[4] = 1
            c.itemconfig(selected,image=empty_block)
            #sets the pit to random colors
            for item in pitobjects:
                c.delete(item)
            def finish(i):
                set_pit(choice([j for j in range(1,4) if j != pit[i]]),i)
                draw_pit()
            for i in range(2,-1,-1):
                draw_animation(i*3,8,diceused,70,c,get_pos,window,event=lambda i=i: finish(i))

            gameover_check()

        #* BUTTONS
        if inside(0,350,50,400,mousex,mousey): #Is restart clicked?
            ask_close()

        row = floor((mousex-SQUAREMARGINY)//49-1) 
        column = floor((mousey-SQUAREMARGINX)//49+1) #work out row and column of clicked space
        if powerups[0] == 2: #Removes the square for the pickaxe
            clear_toast()
            if row < 0 or row > 6 or column < 0 or column > 6:
                pass
            elif lookup (row,column) == 0:
                
                play_sound_effect(sfx_on,nomatch)
            else:
                powerupvalues[0] -= 1
                if powerupvalues[0] == 0:
                    powerups[0] = 0
                    c.itemconfig(pickaxesquare,state=HIDDEN)
                else:
                    powerups[0] = 1
                    c.itemconfig(pickaxesquare,state=HIDDEN)
                c.itemconfig(selected,image=empty_block)    
                
                play_sound_effect(sfx_on,pickused)
                draw_animation(row,column,smokes[0], 100,c,get_pos,window)
                if lookup(row,column) == 12:
                    next_level()
                    play_sound_effect(sfx_on,brickbreak)
                else:
                    play_sound_effect(sfx_on,remove)
                score += 60*level
                update_text()
                c.itemconfig(scoredisp,text=score)
                set_square(0,row,column)
                next_level()
                return
        if powerups[1] == 2 and 0 <= column <= 6 and 0 <= row <= 6: #Removes the line for the throwing axe after checking that it is within bounds
            clear_toast()
            powerupvalues[1] -= 1
            if powerupvalues[1] == 0:
                powerups[1] = 0
                c.itemconfig(throwingaxesquare,state=HIDDEN)
            else:
                powerups[1] = 1
            c.itemconfig(selected,image=empty_block)
            
            play_sound_effect(sfx_on,axeused)
            score += 120*level
            update_text()
            c.itemconfig(scoredisp,text=score)
            clear_line("H",row,column,False)
            next_level()
            return
        if powerups[2] == 2 and 0 <= column <= 6 and 0 <= row <= 6: #Removes the column for the jackhammer after checking that it is within bounds
            clear_toast()
            powerupvalues[2] -= 1
            if powerupvalues[2] == 0:
                powerups[2] = 0
                c.itemconfig(jackhammersquare,state=HIDDEN)
            else:
                powerups[2] = 1
            c.itemconfig(selected,image=empty_block)
            
            play_sound_effect(sfx_on,jackhammerused)
            score += 120*level
            update_text()
            c.itemconfig(scoredisp,text=score)
            clear_line("V",row,column,False)
            next_level()
            return
        if powerups[3] == 2 and 0 <= column <= 6 and 0 <= row <= 6: #Clears the starline
            clear_toast()
            powerupvalues[3] -= 1
            if powerupvalues[3] == 0:
                powerups[3] = 0
                c.itemconfig(starsquare,state=HIDDEN)
            else:
                powerups[3] = 1
            c.itemconfig(selected,image=empty_block)
            
            play_sound_effect(sfx_on,starused)
            score += 300*level
            update_text()
            c.itemconfig(scoredisp,text=score)
            clear_line("V",row,column,False)
            clear_line("H",row,column,False)
            clear_diagonal_lines(row,column)
            next_level()
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
                    score += 10*level
                    explode(row, column, 1)
                    busy = False
                    return
        except IndexError:
            pass
        #works out if the clicked area was inside the grid, that the player can place a color there, that it is empty, and that there is a square next to it
        if row >= 0 and row < GRIDROWS and column >= 0 and column < GRIDROWS and selcolor != 0:
            # print(f'Row: {row}, Column: {column}, Row+1: {row+1}, Column+1: {column+1}, Row-1: {row-1}, Column-1: {column-1}')
            if (lookup(row,column) == 0 and
                    (
                    (row > 0 and lookup(row-1,column)) or
                    (row < 6 and lookup(row+1,column)) or
                    (column < 6 and lookup(row,column+1)) or
                    (column > 0 and lookup(row,column-1))
                    )):
                pit = [randint(1,4) if elem==0 else elem for elem in pit]
                draw_pit()
                set_square(selcolor,row,column)
                colorsel = selcolor
                selcolor = 0
                canplace = False
                c.itemconfig(selected,image=empty_block)
                lines, direction, num = detect_line(row,column,lookup) #detects any lines
                if mode == "obstacle":
                    moves -= 1
                tempx, tempy = row,column
                square = lookup(tempx,tempy)

                for line in lines: #if there are any lines
                    #* HANDLING LINES
                    set_square(0,line[0],line[1]) #clears all of the squares part of the line
                    score += 10*level
                    update_text()
                if len (lines) >= 3:
                    if len(lines) == 3:
                        handle_gem_break(square, direction, num, tempx, tempy)
                    play_sound_effect(sfx_on,remove)
                    for item in highlight:
                        c.delete(item)
                    highlight.clear()
                    c.itemconfig(indicator, state=HIDDEN)
                    if mode == "chroma":
                        if square == 1:
                            play_sound_effect(sfx_on,axeused)
                            clear_line("V",tempx,tempy,False)
                            clear_line("H",tempx,tempy,False)
                        elif square == 2:
                            play_sound_effect(sfx_on,axeused)
                            clear_line(direction,tempx,tempy,sound=False)
                        elif square == 3:
                            play_sound_effect(sfx_on,powerupselected)
                            for _ in range(3):
                                powerups = [0]*5
                                powerupvalues = powerups
                                draw_powerups()
                                window.update()
                                sleep(0.05)
                                powerups = [1]*5
                                powerupvalues = powerups
                                draw_powerups()
                                window.update()               
                                sleep(0.05)
                        elif square == 4:
                            explode(tempx,tempy,1)
                if len(lines) == 4: #Finds the lines with 4 gems and changes them into a drill with the opposite direction as the line.
                    handle_drill_create(square, row, column,num, direction, tempx, tempy)
                    
                    play_sound_effect(sfx_on,drillcreated)
                elif len(lines) == 5:
                    #finds the lines with 5 gems and changes them into a diamond
                    play_sound_effect(sfx_on,diamondcreated)
                    diamonds = vdiamonds if direction == 'V' else hdiamonds
                    if colorsel == 1: #Red
                        draw_animation(row,column,diamonds["red"],100,c,get_pos,window,event=lambda:set_square(colorsel+6,row,column))
                    elif colorsel == 2: #Yellow
                        draw_animation(row,column,diamonds["yellow"],100,c,get_pos,window,event=lambda:set_square(colorsel+6,row,column))
                    elif colorsel == 3: #Green
                        draw_animation(row,column,diamonds["green"],100,c,get_pos,window,event=lambda:set_square(colorsel+6,row,column))
                    elif colorsel == 4: #Blue
                        draw_animation(row,column,diamonds["blue"],100,c,get_pos,window,event=lambda:set_square(colorsel+6,row,column))
                    
                elif len(lines) >= 6: #finds the lines with 6 or more gems and changes them into a bomb. gems used in 2 lines count twice
                    draw_animation(row,column,explosions,100,c,get_pos,window,event=lambda: set_square(11,row,column))
                    
                    play_sound_effect(sfx_on,bombcreated)
                soundplayed = False
                #Need to go through all the lines again to remove all the bricks
                for line in lines:

                    soundplayed = clear_bricks(line,soundplayed)

                c.itemconfig(scoredisp,text=score)
                if all(0==x for x in grid):
                    score += 50*level
                    update_text()
                    c.itemconfig(scoredisp,text=score)
                    window.after(1000,reset_color)
                    window.after(1000,play_place_sound)
                if len(lines) == 0:
                    play_place_sound()
                    score += level
                    update_text()
                    if mode in ("survival","chroma"):
                        for _ in range(level): #Puts more bricks on the board
                            set_brick()
                next_level()
                if gameover_check():
                        return
            else:
                
                play_sound_effect(sfx_on,nomatch)

            if gameover_check(): return
            draw_board()
        elif column == 8: #if not check if row is where the colors are and that they can choose a color
            pick_color(row)
            if selcolor == 0:
                canplace = False
    else:
        if display:
            if survivalb.is_clicked(mousex,mousey):
                play_sound_effect(sfx_on,clicked)
                mode = "survival"
                start()

            if timeb.is_clicked(mousex,mousey):
                play_sound_effect(sfx_on,clicked)
                mode = "time"
                start()

            if obstacleb.is_clicked(mousex,mousey):
                play_sound_effect(sfx_on,clicked)
                mode = "obstacle"
                start()
            
            if chromab.is_clicked(mousex,mousey):
                play_sound_effect(sfx_on,clicked)
                mode = "chroma"
                start()
        else:
            if startb.is_clicked(mousex,mousey):
                display_modes()
                play_sound_effect(sfx_on,clicked)
            if helpb.is_clicked(mousex,mousey) and not helping:
                play_sound_effect(sfx_on,clicked)
                helping = True
                tutstage = 1
                disp_help() 

def handle_drill_create(square, row, column, num, direction, tempx, tempy):
    color = [None,"red","yellow","green","blue"][square]
    if direction == "H":
        if square in (1,2):
            pos = ["left","right"][num-1]
            draw_animation(tempx,tempy,hdrills[color][pos],100,c,get_pos,window,event=lambda: set_square(5 if direction == "H" else 6,row,column))
        else:
            set_square(5 if direction == "H" else 6,row,column)

    elif direction == "V":
        if square in ():
            pos = ["top","bottom"][num-1]
            draw_animation(tempx,tempy,vgembreaks[color][pos],100,c,get_pos,window,event=lambda x=tempx,y=tempy: draw_animation(x,y,gemvanish,100,c,get_pos,window))
        else: 
            set_square(5 if direction == "H" else 6,row,column)

def handle_gem_break(square, direction, num, tempx, tempy):
    color = [None,"red","yellow","green","blue"][square]
    if direction == "H":
        pos = ["left","center","right"][num]
        draw_animation(tempx,tempy,hgembreaks[color][pos],100,c,get_pos,window,event=lambda x=tempx,y=tempy: draw_animation(x,y,gemvanish,100,c,get_pos,window))

    elif direction == "V":
        pos = ["top","center","bottom"][num]
        draw_animation(tempx,tempy,vgembreaks[color][pos],100,c,get_pos,window,event=lambda x=tempx,y=tempy: draw_animation(x,y,gemvanish,100,c,get_pos,window))

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

    for item in [survivalb,timeb,obstacleb]:
        item.set_visible(True)

def clear_diagonal_lines(row,column,clear=True):
    currow = row
    curcolumn = column
    if not clear:
        squares = []
    while currow > 0 and curcolumn > 0:
        currow -= 1
        curcolumn -= 1
    while currow < 7 and curcolumn < 7:

        if clear:
            if lookup(currow,curcolumn) == 12:
                next_level()
                play_sound_effect(sfx_on,brickbreak)
            elif lookup(currow,curcolumn) != 0:
                play_sound_effect(sfx_on,remove)
            play_sound_effect(sfx_on,remove)
            set_square(0,currow,curcolumn)
            draw_animation(currow,curcolumn,smokes[0],100,c,get_pos,window)
        else:
            squares.append((currow,curcolumn))

        currow += 1
        curcolumn += 1

    
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
                next_level()
                play_sound_effect(sfx_on,brickbreak)
            elif lookup(currow,curcolumn) != 0:
                play_sound_effect(sfx_on,remove)
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
    global score
    queue = []
    play_sound_effect(sfx_on,explosion)
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
                score += level
    set_square(0,row,column)
    draw_animation(row,column,explosions,75,c,get_pos,window)
    for item in queue:
        item()
    if all(0==x for x in grid):
        toast("Board cleared!", 1)
        score += 50*level
        update_text()
        c.itemconfig(scoredisp,text=score)
        window.after(1000,reset_color)
        window.after(1000,play_place_sound)
    update_text()

def clear_bricks(line,soundplayed=False):
    #This next part checks all the blocks around where the line was.
    #If any bricks were there it breaks them

    x, y = line[0], line[1]+1
    soundplayed = breakbrick(x,y,not soundplayed) or soundplayed

    x, y = line[0], line[1]-1
    soundplayed = breakbrick(x,y,not soundplayed) or soundplayed

    x, y = line[0]+1, line[1]
    soundplayed = breakbrick(x,y,not soundplayed) or soundplayed

    x, y = line[0]-1, line[1]
    soundplayed = breakbrick(x,y,not soundplayed) or soundplayed
    return soundplayed


def breakbrick(x,y,sound):
    if lookup(x,y) == 12:
        if 0 <= y <= 6 and 0 <= x <= 6:
            set_square(0,x,y)
            draw_animation(x,y,brickbreaking,100,c,get_pos,window)
            if sound:
                play_sound_effect(sfx_on,brickbreak)
            next_level()
            return True
    return False
def clear_selection():
    c.itemconfig(selected,image=empty_block)

#RETURN HERE
def gameover_check():
    global gameover, highscore, display, score, powerups, powerupvalues
    if (0 not in grid and any(x in grid for x in [5,6,7,8,9,10,11]) == 0) or (moves <= 0 and mode == "obstacle"):  #game is over
        stop_music(window)
        if music_on or sfx_on:
            game_over_music.play()
        powerups = [0]*5
        powerupvalues = [0]*5
        playb.set_visible(True)
        c.itemconfig(gameovertext,text="GAME OVER")
        c.itemconfig(finalscoretext, text="Your score was "+str(score))
        for square in board: #delete the grid so we can actually see the gameover text
            c.delete(square)
        gameover = True

        if score > highscore: 
            highscore = score
        with open("Gem miner/highscore.txt","w+") as hsfile:
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
