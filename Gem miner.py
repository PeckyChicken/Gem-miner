from statistics import mean
from time import sleep
from tkinter import * #doing wildcard import to make it easier to use
from math import floor
from random import choice, randint
from pygame import mixer, init
mixer.pre_init(48000, -16, 1, 512)
init()
mixer.init()

filepath = __file__+"/../"
window = Tk() #sets up window
window.title("Gem miner")
window.iconbitmap(filepath+"Gem miner/icon.ico")
window.resizable(0, 0)

WIDTH = 500
HEIGHT = 500
SQUARELEN = 50
SQUARESPACING = 50
SQUAREMARGINX = 75
SQUAREMARGINY = 25
PITSQUARESPACING = 150
TEXTCOL = "#a27100"
gameover = False
squarey = SQUAREMARGINY
GRIDROWS = 7
PITSQUAREY = 425
STARTERMOVES = 30
score = 0
level = 1
track = 0
busy = False
reqscore = 500
mode = "time"
display = False

MusicOn = True
SfxOn = True

c = Canvas(window,width=WIDTH,height=HEIGHT, bg="gray") #sets up canvas
c.pack(fill="both")
bg = PhotoImage(file = filepath+"Gem miner/bg.png")
c.create_image(WIDTH/2,HEIGHT/2,image=bg)

try:
    with open(filepath+"Gem miner/highscore.txt","r+") as hsfile:
        highscore = hsfile.read()
        highscore = int(highscore.strip())
        hsfile.close()
except (FileNotFoundError, ValueError):
    highscore = 0

font = "comic sans ms"

canplace = False
selcolor = 0

scoretext = c.create_text(40,20,text="Score",font=(font,10),state=HIDDEN,fill=TEXTCOL)
scoredisp = c.create_text(40,50,text=0,font=(font,31),state=HIDDEN,fill=TEXTCOL)

goaltext = c.create_text(40,100,text="Goal",font=(font,10),state=HIDDEN,fill=TEXTCOL)
goaldisp = c.create_text(40,130,text=500,font=(font,23),state=HIDDEN,fill=TEXTCOL)

leveltext = c.create_text(40,180,text="Level",font=(font,10),state=HIDDEN,fill=TEXTCOL)
leveldisp = c.create_text(40,210,text=1,font=(font,31),state=HIDDEN,fill=TEXTCOL)


frame = 0

gameovertext = c.create_text(WIDTH/2,HEIGHT/2-25,font=(font,50),fill=TEXTCOL)
playagaintext = c.create_text(WIDTH/2,HEIGHT/2+25,font=(font,30),fill=TEXTCOL)
finalscoretext = c.create_text(WIDTH/2,HEIGHT/2+75,font=(font,15),fill=TEXTCOL)
toasttext = c.create_text(WIDTH/2,HEIGHT/2 + 150,font=(font,15),text="Click again if you really want to restart.",state=HIDDEN,fill=TEXTCOL)

highscoretext = c.create_text(WIDTH-10,HEIGHT-20,font=(font,15),anchor="e",text=f"High score: {highscore}",fill="#916000")
clickcount = 0

#imports the images
red_block = PhotoImage(file = filepath+"Gem miner/red_block.png")
yellow_block = PhotoImage(file = filepath+"Gem miner/yellow_block.png")
green_block = PhotoImage(file = filepath+"Gem miner/green_block.png")
blue_block = PhotoImage(file = filepath+"Gem miner/blue_block.png")
empty_block = PhotoImage(file = filepath+"Gem miner/empty.png")
vdrill = PhotoImage(file = filepath+"Gem miner/rocket_vertical.png")
hdrill = PhotoImage(file = filepath+"Gem miner/rocket_horizontal.png")
red_diamond = PhotoImage(file = filepath+"Gem miner/red_ball.png")
yellow_diamond = PhotoImage(file = filepath+"Gem miner/yellow_ball.png")
green_diamond = PhotoImage(file = filepath+"Gem miner/green_ball.png")
blue_diamond = PhotoImage(file = filepath+"Gem miner/blue_ball.png")
rainbow_diamond = PhotoImage(file = filepath+"Gem miner/rain_ball.png")
bomb = PhotoImage(file = filepath+"Gem miner/bomb.png")
bricks = PhotoImage(file = filepath+"Gem miner/bricks.png")
jackhammer = PhotoImage(file = filepath+"Gem miner/jackhammer.png")
pickaxe = PhotoImage(file = filepath+"Gem miner/pickaxe.png")
throwingaxe = PhotoImage(file = filepath+"Gem miner/throwing axe.png")
star = PhotoImage(file = filepath+"Gem miner/star.png")
shuffle = PhotoImage(file = filepath+"Gem miner/shuffle.png")
restart = PhotoImage(file = filepath+"Gem miner/restartbutton.png")
brickp1 = PhotoImage(file = filepath+"Gem miner/bricks_particle_1.png")
brickp2 = PhotoImage(file = filepath+"Gem miner/bricks_particle_2.png")
brickp3 = PhotoImage(file = filepath+"Gem miner/bricks_particle_3.png")
brickp4 = PhotoImage(file = filepath+"Gem miner/bricks_particle_4.png")
button = PhotoImage(file = filepath+"Gem miner/button.png")
titlebgimage = PhotoImage(file = filepath+"Gem miner/TitleBG.png")
tut1 = PhotoImage(file = filepath+"Gem miner/Tutorial1.png")
tut2 = PhotoImage(file = filepath+"Gem miner/Tutorial2.png")
tut3 = PhotoImage(file = filepath+"Gem miner/Tutorial3.png")
tut4 = PhotoImage(file = filepath+"Gem miner/Tutorial4.png")
tut5 = PhotoImage(file = filepath+"Gem miner/Tutorial5.png")
tut6 = PhotoImage(file = filepath+"Gem miner/Tutorial6.png")
music = PhotoImage(file = filepath+"Gem miner/music_yes.png")
sfx = PhotoImage(file = filepath+"Gem miner/sfx_yes.png")
nomusic = PhotoImage(file = filepath+"Gem miner/music_no.png")
nosfx = PhotoImage(file = filepath+"Gem miner/sfx_no.png")
explosions = [PhotoImage(file = filepath+"Gem miner/explosion1.png"), 
              PhotoImage(file = filepath+"Gem miner/explosion2.png"), 
              PhotoImage(file = filepath+"Gem miner/explosion3.png"), 
              PhotoImage(file = filepath+"Gem miner/explosion4.png"), 
              PhotoImage(file = filepath+"Gem miner/explosion5.png"), 
              PhotoImage(file = filepath+"Gem miner/explosion6.png"), 
              PhotoImage(file = filepath+"Gem miner/explosion7.png"), 
              PhotoImage(file = filepath+"Gem miner/explosion8.png"), 
              PhotoImage(file = filepath+"Gem miner/explosion9.png"), 
              PhotoImage(file = filepath+"Gem miner/explosion10.png")]

breaking = [PhotoImage(file = filepath+"Gem miner/vdrill1.png"),
           PhotoImage(file = filepath+"Gem miner/vdrill2.png"),
           PhotoImage(file = filepath+"Gem miner/vdrill3.png"),
           PhotoImage(file = filepath+"Gem miner/vdrill4.png"),
           PhotoImage(file = filepath+"Gem miner/vdrill5.png"),
           PhotoImage(file = filepath+"Gem miner/vdrill6.png"),
           PhotoImage(file = filepath+"Gem miner/vdrill7.png"),
           PhotoImage(file = filepath+"Gem miner/vdrill8.png"),
           PhotoImage(file = filepath+"Gem miner/vdrill9.png"),
           PhotoImage(file = filepath+"Gem miner/vdrill10.png")]

brickplace = [PhotoImage(file = filepath+"Gem miner/brickplace1.png"),
              PhotoImage(file = filepath+"Gem miner/brickplace2.png"),
              PhotoImage(file = filepath+"Gem miner/brickplace3.png"),
              PhotoImage(file = filepath+"Gem miner/brickplace4.png"),
              PhotoImage(file = filepath+"Gem miner/brickplace5.png"),
              PhotoImage(file = filepath+"Gem miner/brickplace6.png"),
              PhotoImage(file = filepath+"Gem miner/brickplace7.png"),
              PhotoImage(file = filepath+"Gem miner/brickplace8.png")]

brickbreaking = [PhotoImage(file = filepath+"Gem miner/brickbreak1.png"),
                 PhotoImage(file = filepath+"Gem miner/brickbreak2.png"),
                 PhotoImage(file = filepath+"Gem miner/brickbreak3.png"),
                 PhotoImage(file = filepath+"Gem miner/brickbreak4.png"),
                 PhotoImage(file = filepath+"Gem miner/brickbreak5.png"),]

diceused = [PhotoImage(file = filepath+"Gem miner/dice1.png")]



titlebg = c.create_image(WIDTH/2,HEIGHT/2,image=titlebgimage)


selected = c.create_image(470,50,image=empty_block,state=HIDDEN)

tutimage = c.create_image(WIDTH/2,HEIGHT/2,image=tut1,state=HIDDEN)


#Importing the sounds
bombcreated = mixer.Sound(filepath+"Gem miner/bombcreated.wav")
explosion = mixer.Sound(filepath+"Gem miner/boom.wav")
remove = mixer.Sound(filepath+"Gem miner/break.wav")
brickbreak = mixer.Sound(filepath+"Gem miner/brick_break.wav")
clearall = mixer.Sound(filepath+"Gem miner/clearall.wav")
diamondcreated = mixer.Sound(filepath+"Gem miner/diamondcreated.wav")
diamondused = mixer.Sound(filepath+"Gem miner/diamondused.wav")
drillcreated = mixer.Sound(filepath+"Gem miner/drillcreated.wav")
drillused = mixer.Sound(filepath+"Gem miner/drillused.wav")
jackhammerused = mixer.Sound(filepath+"Gem miner/javalinused.wav")
nomatch = mixer.Sound(filepath+"Gem miner/nomatch.wav")
pickused = mixer.Sound(filepath+"Gem miner/pickaxeused.wav")
placed = mixer.Sound(filepath+"Gem miner/place.wav")
powerupselected = mixer.Sound(filepath+"Gem miner/powerupselected.wav")
shufflesound = mixer.Sound(filepath+"Gem miner/shuffle.wav")
axe = mixer.Sound(filepath+"Gem miner/Throwing axe.wav")
starnoise = mixer.Sound(filepath+"Gem miner/star.wav")
title1 = mixer.Sound(filepath+"Gem miner/title1.wav")
title2 = mixer.Sound(filepath+"Gem miner/title2.wav")
main1 = mixer.Sound(filepath+"Gem miner/main.wav")
main2 = mixer.Sound(filepath+"Gem miner/main2.wav")
advance = mixer.Sound(filepath+"Gem miner/nextlevel.wav")
gameover1 = mixer.Sound(filepath+"Gem miner/gameover1.wav")
gameover2 = mixer.Sound(filepath+"Gem miner/gameover2.wav")
clicked = mixer.Sound(filepath+"Gem miner/click.wav")

#Sets the volume of the music
music_vol = 0.25
mixer.Sound.set_volume(title1,music_vol)
mixer.Sound.set_volume(title2,music_vol)
mixer.Sound.set_volume(main1,music_vol)
mixer.Sound.set_volume(main2,music_vol)
mixer.Sound.set_volume(gameover1,music_vol)
mixer.Sound.set_volume(gameover2,music_vol)

#Sets the volume of the sound effects
sound_vol = 0.5
mixer.Sound.set_volume(bombcreated,sound_vol)
mixer.Sound.set_volume(explosion,sound_vol)
mixer.Sound.set_volume(remove,sound_vol)
mixer.Sound.set_volume(brickbreak,sound_vol)
mixer.Sound.set_volume(clearall,sound_vol)
mixer.Sound.set_volume(diamondcreated,sound_vol)
mixer.Sound.set_volume(diamondused,sound_vol)
mixer.Sound.set_volume(drillcreated,sound_vol)
mixer.Sound.set_volume(drillused,sound_vol)
mixer.Sound.set_volume(bombcreated,sound_vol)
mixer.Sound.set_volume(jackhammerused,sound_vol)
mixer.Sound.set_volume(nomatch,sound_vol)
mixer.Sound.set_volume(pickused,sound_vol)
mixer.Sound.set_volume(placed,sound_vol)
mixer.Sound.set_volume(powerupselected,sound_vol)
mixer.Sound.set_volume(shufflesound,sound_vol)
mixer.Sound.set_volume(axe,sound_vol)
mixer.Sound.set_volume(advance,sound_vol)
mixer.Sound.set_volume(clicked,sound_vol)

powerups = [1,1,1,1,1] #sets up the powerup squares
powerupvalues = [1,1,1,1,1]

pickaxesquare = c.create_image(470,150,image=pickaxe,state=HIDDEN)
pickvalue = c.create_text(498,180,text='',font=(font,15),state=HIDDEN,fill=TEXTCOL)

throwingaxesquare = c.create_image(470,210,image=throwingaxe,state=HIDDEN)
axevalue = c.create_text(498,240,text='',font=(font,15),state=HIDDEN,fill=TEXTCOL)

jackhammersquare = c.create_image(470,270,image=jackhammer,state=HIDDEN)
jackhammervalue = c.create_text(498,300,text='',font=(font,15),state=HIDDEN,fill=TEXTCOL)

starsquare = c.create_image(470,330,image=star,state=HIDDEN)
starvalue = c.create_text(498,360,text='',font=(font,15),state=HIDDEN,fill=TEXTCOL)

shufflesquare = c.create_image(470,390,image=shuffle,state=HIDDEN)
shufflevalue = c.create_text(498,420,text='',font=(font,15),state=HIDDEN,fill=TEXTCOL)


#Sets up the button squares
restartsquare = c.create_image(470,450,image=restart,state=HIDDEN)
musicsquare = c.create_image(25,475,image=music)
sfxsquare = c.create_image(25,425,image=sfx)


#* GRID
grid = [0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,
        0,0,0,0,0,0,0] #defines the game board
pit = [randint(1,4),randint(1,4),randint(1,4)] #sets up the pit
pitobjects = list()
defaulttextsize = 35
loop = 0


#Makes all the title screen buttons
startbuttonbg = c.create_image(WIDTH/2,HEIGHT/2-35,image=button)
startbuttontext = c.create_text(WIDTH/2,HEIGHT/2-35,text="Start",font=(font,25),fill="white")

helpbuttonbg = c.create_image(WIDTH/2,HEIGHT/2+35,image=button)
helpbuttontext = c.create_text(WIDTH/2,HEIGHT/2+35,text="How to play",font=(font,25),fill="white")

startbounds = (WIDTH/2-100,HEIGHT/2-60,WIDTH/2+100,HEIGHT/2-10)
helpbounds = (WIDTH/2-100,HEIGHT/2+10,WIDTH/2+100,HEIGHT/2+60)

normalbuttonbg = c.create_image(WIDTH/2,HEIGHT/2-35,image=button,state=HIDDEN)
normalbuttontext = c.create_text(WIDTH/2,HEIGHT/2-35,text="Normal",font=(font,25),fill="white",state=HIDDEN)

timebuttonbg = c.create_image(WIDTH/2,HEIGHT/2+35,image=button,state=HIDDEN)
timebuttontext = c.create_text(WIDTH/2,HEIGHT/2+35,text="Time rush",font=(font,25),fill="white",state=HIDDEN)

started = False
helping = False
tutstage = 0

#*IDS
itemid = {0:empty_block,1:red_block,2:yellow_block,3:green_block,4:blue_block,5:vdrill,6:hdrill,7:red_diamond,8:yellow_diamond,9:green_diamond,10:blue_diamond,11:bomb,12:bricks} #sets up the item ids

board = list() #sets up the board
#Music loop


repeats = 0
def title_music():
    global repeats, loop
    if repeats == 0:
        mixer.Sound.play(title1)
        loop = window.after(13300,title_music)
    else:
        mixer.Sound.play(title2)
        loop = window.after(54850,title_music)
    repeats += 1
title_music()

def game_music():
    global loop2
    mixer.Sound.play(main1)
    loop2 = window.after(52377,game_music)

def game_music2():
    global loop2
    mixer.Sound.play(main2)
    loop2 = window.after(61075,game_music2)

def game_over_music():
    global repeats, loop2
    if repeats == 0:
        mixer.Sound.play(gameover1)
        loop2 = window.after(643,game_over_music)
    else: 
        mixer.Sound.play(gameover2)
        loop2 = window.after(13714,game_over_music)
    repeats += 1

def stop_music():
    global repeats
    mixer.stop()
    try:
        window.after_cancel(loop)
    except NameError: pass
    try:
        window.after_cancel(loop2)
    except NameError: pass
    repeats = 0

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
    global pickaxesquare, throwingaxesquare, jackhammersquare, starsquare, shuffle, powerups
    powerups = [1,1,1,1,1]
    c.itemconfig(pickaxesquare,state=NORMAL)
    c.itemconfig(throwingaxesquare,state=NORMAL)
    c.itemconfig(jackhammersquare,state=NORMAL)
    c.itemconfig(starsquare,state=NORMAL)
    c.itemconfig(shufflesquare,state=NORMAL)
    c.itemconfig(restartsquare,state=NORMAL)


def draw_animation(x,y,frames,fps):
    frametime = 1/fps
    DrawX, DrawY = get_pos(x,y)
    sprite = c.create_image(DrawX,DrawY,image=frames[0])
    frame = 0
    while frame < len(frames):
        c.itemconfig(sprite,state=NORMAL,image=frames[frame])
        frame += 1
        window.update()
        sleep(1/fps)
    c.delete(sprite)

def draw_instant_animation(x,y,frames,fps,frame=0):
    DrawX, DrawY = get_pos(x,y)
    sprite = c.create_image(DrawX,DrawY,image=frames[0])
    c.itemconfig(sprite,state=NORMAL,image=frames[frame])
    frame += 1
    window.update()
    if frame < len(frames) -1:
        frametime = 1/fps
        window.after(int(frametime),draw_instant_animation,x,y,frames,fps,frame)
    c.delete(sprite)

def set_square(color,x,y):
    global board
    itemid = y*GRIDROWS + x #works out the id of the list given the x and y
    grid[itemid] = color #replaces the current color with the new one
    draw_board()

def next_level():
    global level, powerups, reqscore, powerupvalues
    #This complicated setup means that the player will advance a level when they get to 500, 1000, 5000, etc.
    reqscore = (((level+1)%2)+1) * 500 * 10 ** (1+(level - 3) // 2)
    if score >= reqscore:
        level += 1
        powerups = [1]*5
        powerupvalues = [1]*5
        update_text()
        draw_powerups()
        if SfxOn:
            mixer.Sound.play(advance)
            
def lookup(x,y):
    try:
        color = grid[y*GRIDROWS+x] #find the color of the grid square
        return color
    except IndexError:
        return 0

def Get_ID(x,y):
    return board[y*GRIDROWS+x]

def get_pos(gridx,gridy):
    x = gridx*SQUARELEN+SQUAREMARGINX*1.35
    y = gridy*SQUARELEN+SQUAREMARGINY*2
    #Both of these are very similar, so I will talk about both together.
    #The gridx/y * squarelen works out the relative position of the square, then the distance from the wall is added on.
    #The distance from the wall is multiplied by the value so that the predicted position is in the center of the square.

    return x,y

def set_pit(color,pos):
    pit[pos] = color #changes color of the pit objects

def detect_line(x,y):
    count = 0
    usedsquares = list()
    curx = x
    cury = y
    #Moves down as far as there are matches
    while lookup(curx,cury) == lookup(x,y):
        count += 1
        usedsquares.append([curx,cury]) #add the current match to the list
        cury += 1 #move it down one
        if cury >= 7: break #stop it from overflowing
    if count != 0:
        curx = x
        cury = y-1 #subtracts one so it doesnt double count the first one
        #Once it has finished if it found anything it goes back up to look for other matches
        while lookup(curx,cury) == lookup(x,y):
            if cury < 0: break
            count += 1 
            usedsquares.append([curx,cury]) #add the current match to the list
            cury -= 1 #move it up one row
    
    #Does it again for the up direction, doesnt need to check for down because it just did that
    while lookup(curx,cury) == lookup(x,y):
        if cury < 0: break
        count += 1 
        usedsquares.append([curx,cury]) #add the current match to the list
        cury -= 1 #move it up one row
    if count == 5: #Return if already a diamond
        return usedsquares, "V"
    if count < 3: #If there were no lines that way they do not count
        count == 0
        usedsquares.clear()
    #now for the horizontal lines
    xcount = 0 #resetting things for the horizontal check
    xusedsquares = list()
    curx = x
    cury = y
    #checking for anything to the right
    while lookup(curx,cury) == lookup(x,y):
        xcount += 1
        xusedsquares.append([curx,cury]) #add the current match to the list
        curx += 1 #move it right one column
        if curx >= 7: break
    if xcount != 0:
        curx = x-1 #subtracts one to avoid double counting
        cury = y
        #Go back to the left to look for more matches
        while lookup(curx,cury) == lookup(x,y):
            if curx < 0: break
            xcount += 1
            xusedsquares.append([curx,cury]) #add the current match to the list
            curx -= 1 #move it back left
    if xcount < 3: #If there were no lines that way they do not count
        xcount == 0
        xusedsquares.clear()
    if xcount == 5: #Return if already a diamond
        return xusedsquares, "V"
    if len(xusedsquares)+len(usedsquares) >= 6:
        return xusedsquares+usedsquares,"HV"
    elif len(xusedsquares) >= 3:
        return xusedsquares,"H"
    elif len(usedsquares) >= 3:
        return usedsquares,"V"
    #Now to check for left on its own
    while lookup(curx,cury) == lookup(x,y):
        if curx < 0: break
        xcount += 1
        xusedsquares.append([curx,cury]) #add the current match to the list
        curx -= 1 #move it left one column
    if xcount == 5:
        return xusedsquares, "V"
    if len(xusedsquares)+len(usedsquares) >= 6:
        return xusedsquares+usedsquares,"HV"
    elif len(xusedsquares) >= 3:
        return xusedsquares,"H"
    elif len(usedsquares) >= 3:
        return usedsquares,"V"
    return [],"0"

def reset_color(): #sets a random square to a color
    set_square(randint(1,4),randint(0,6),randint(0,6))

def set_brick(): #sets a random square to a brick
    if 0 not in grid: return 1
    x, y = randint(0,6),randint(0,6)
    while lookup(x,y) != 0:
        x, y = randint(0,6),randint(0,6)
    draw_animation(x,y,brickplace,100)
    set_square(12,x,y)
    return 0

def play_place_sound(): #only putting it in a function by itself so i can call it from a window.after
    if SfxOn:
        mixer.Sound.play(placed)

def time_rush():
    set_brick()
    if gameover_check():
        return
    base_time = 1500
    window.after(mean([base_time//level,base_time]),time_rush)

def start():
    global repeats,track
    reset_color()
    reset_color()
    draw_powerups()
    draw_board()
    draw_pit()
    if mode == "time":
        time_rush()

    c.itemconfig(pickvalue,state=NORMAL)
    c.itemconfig(axevalue,state=NORMAL)
    c.itemconfig(jackhammervalue,state=NORMAL)
    c.itemconfig(starvalue,state=NORMAL)
    c.itemconfig(shufflevalue,state=NORMAL)

    c.itemconfig(scoredisp,state=NORMAL)
    c.itemconfig(scoretext,state=NORMAL)

    c.itemconfig(leveldisp,state=NORMAL)
    c.itemconfig(leveltext,state=NORMAL)

    c.itemconfig(goaldisp,state=NORMAL)
    c.itemconfig(goaltext,state=NORMAL)

    c.itemconfig(selected,state=NORMAL)
    c.itemconfig(titlebg,state=HIDDEN)

    c.itemconfig(startbuttonbg,state=HIDDEN)
    c.itemconfig(startbuttontext,state=HIDDEN)

    c.itemconfig(helpbuttonbg,state=HIDDEN)
    c.itemconfig(helpbuttontext,state=HIDDEN)

    c.itemconfig(normalbuttonbg,state=HIDDEN)
    c.itemconfig(normalbuttontext,state=HIDDEN)

    c.itemconfig(timebuttonbg,state=HIDDEN)
    c.itemconfig(timebuttontext,state=HIDDEN)

    c.itemconfig(highscoretext,state=HIDDEN)

    stop_music()
    track = randint(0,1)
    if MusicOn:
        [game_music,game_music2][track]()
    if mode == "normal":
        for _ in range(5):
            set_brick()

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
    global grid, clickcount, score, level, highscore
    if SfxOn:
        mixer.Sound.play(clicked)
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
        c.itemconfig(playagaintext,text="")
        c.itemconfig(finalscoretext,text="")
        c.itemconfig(toasttext, state=HIDDEN)
        clickcount = 0
        if mode == "normal":
            for _ in range(5):
                set_brick()
        return
    else:
        window.after(2000, reset_count)

def calc_font_size(text):
    return defaulttextsize-len(text)*4

def update_text(): #Updates the font size depending on how many points the player has.
    c.itemconfig(scoredisp,font=(font,calc_font_size(str(score))))
    c.itemconfig(scoredisp,text=str(score))
    next_level()
    c.itemconfig(leveldisp,text=str(level))
    c.itemconfig(leveldisp,font=(font,calc_font_size(str(level))))

    c.itemconfig(goaldisp,text=str(reqscore))
    c.itemconfig(goaldisp,font=(font,calc_font_size(str(reqscore))))

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
    c.itemconfig(startbuttonbg,state=HIDDEN)
    c.itemconfig(startbuttontext,state=HIDDEN)
    c.itemconfig(helpbuttonbg,state=HIDDEN)
    c.itemconfig(helpbuttontext,state=HIDDEN)
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
        c.itemconfig(startbuttonbg,state=NORMAL)
        c.itemconfig(startbuttontext,state=NORMAL)
        c.itemconfig(helpbuttonbg,state=NORMAL)
        c.itemconfig(helpbuttontext,state=NORMAL)
#* HANDLING

def clear3x3(row,column):
    global score, SfxOn
    if SfxOn:
        mixer.Sound.play(drillused)
    
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

    if SfxOn:
        mixer.Sound.play(diamondused)
    
    for i in range(len(grid)):
        if grid[i] == lookup(diamondx,diamondy)-6: #sets all colors of the same to the item
            x = i%7
            y = i//7
            draw_animation(x,y,breaking,100)
            set_square(11 if item == "bomb" else randint(5,6),x,y)
            score += 10*level
            update_text()
    busy = False
    draw_animation(diamondx,diamondy,breaking,100)
    set_square(11 if item == "bomb" else randint(5,6),diamondx,diamondy)

def clear_2_lines(row,column):
    global score
    if SfxOn:
        mixer.Sound.play(drillused)
    
    clear_line("V",row,column,False)
    clear_line("H",row,column,False)

def big_bang(row,column):
    global score
    score += 50*level
    explode(row,column,4)
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
            if SfxOn:
                mixer.Sound.play(clearall)
            window.after(2250,clear_board)
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

def clear_line(direction,row,column,sound=True):
    global score
    # #Reusing code from the SetSquare() function, because the SetSquare function runs some unwanted code
    # itemid = column*GRIDROWS + row 
    # grid[itemid] = 0 #replaces the current color with the new one

    if sound and SfxOn:
        mixer.Sound.play(drillused)
    for square in range(GRIDROWS):
        curx, cury = square if direction == "H" else row, square if direction == "V" else column
        cursquare = lookup(curx,cury)
        draw_animation(curx,cury,breaking,100)
        if cursquare != 0:
            score += 10*level
            if SfxOn:
                if cursquare == 12:
                    mixer.Sound.play(brickbreak)
                else:
                    mixer.Sound.play(remove)
            update_text()
            c.itemconfig(scoredisp,text=score)
            #     #This bit here makes sure that it does not set off any drills directly next to it, 
            #     #as they would have been combined to clear 2 lines. It also makes sure that it doesnt set itself off
            # if cursquare == 5:
            #     clearline("V",curx,cury)
            # if cursquare == 6:
            #     clearline("H",curx,cury)
        set_square(0,curx,cury) #sets all squares in the column to blank
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
    powerups = [1 if elem==2 else elem for elem in powerups]
    canplace = True #make sure that the player can place a color
    c.itemconfig(pitobjects[row//3],image=itemid[selcolor]) #sets the color to gray temporarily
    selcolor, pit[row//3] = pit[row//3], selcolor #swaps the selected color with the one in the pit
    c.itemconfig(selected,image=itemid[selcolor]) #fills the selected box with whatever color was chosen

def key_press(event):
    key = event.keysym
    if key in ['1','2','3']:
        keyvalue = int(key)-1
        pick_color(keyvalue*3)

#Main event
def click(event):
    global selcolor, pit, canplace, pitobjects, grid, score, gameover, powerups, started, helping, tutstage, level, highscore, MusicOn, SfxOn, repeats, busy, track, mode

    next_level()
    mousex = event.x
    mousey = event.y #get mouse x and y
    if helping:
        tutstage += 1
        if SfxOn:
            mixer.Sound.play(clicked)
        disp_help()
        return

    if inside(0,450,50,500,mousex,mousey): #Is music clicked?
        if MusicOn:
            MusicOn = False
            if SfxOn:
                mixer.Sound.play(clicked)
            stop_music()
            c.itemconfig(musicsquare, image = nomusic)
        else:
            MusicOn = True
            repeats = 0
            if SfxOn:
                mixer.Sound.play(clicked)
            if started:
                [game_music,game_music2][track]()
            else:
                title_music()
            c.itemconfig(musicsquare, image = music)

    if inside(0,400,50,450,mousex,mousey): #Is sfx clicked?
        if SfxOn:
            SfxOn = False
            c.itemconfig(sfxsquare, image = nosfx)
        else:
            SfxOn = True
            if SfxOn:
                mixer.Sound.play(clicked)
            c.itemconfig(sfxsquare, image = sfx)
    
    if started:
        if gameover: #if the game is over run it again
            stop_music()
            if SfxOn:
                mixer.Sound.play(clicked)
            grid = [0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0]
            reset_color()
            reset_color()
            draw_powerups()
            selcolor = 0
            c.itemconfig(selected,image=empty_block)
            score = 0
            level = 1
            gameover = False
            draw_board()
            c.itemconfig(scoredisp,text=score)
            c.itemconfig(gameovertext,text="")
            c.itemconfig(playagaintext,text="")
            c.itemconfig(finalscoretext,text="")
            track = randint(0,1)
            if MusicOn:
                [game_music,game_music2][track]()
            update_text()
            if mode == "normal":
                for _ in range(5):
                    set_brick()
            return


        #TODO: TURN THIS INTO A FUNCTION
        if inside(445,125,495,175,mousex,mousey) and powerups[0] != 0: #is pickaxe clicked?
            if powerups[0] == 2:
                powerups[0] = 1
                clear_toast()
                clear_selection()
                return
            if SfxOn:
                mixer.Sound.play(powerupselected)
            if canplace:
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
            if powerups[1] == 2:
                powerups[1] = 1
                clear_toast()
                clear_selection()
                return
            if SfxOn:
                mixer.Sound.play(powerupselected)
            if canplace:
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
            if powerups[2] == 2:
                powerups[2] = 1
                clear_toast()
                clear_selection()
                return
            if SfxOn:
                mixer.Sound.play(powerupselected)
            if canplace:
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
            if powerups[3] == 2:
                powerups[3] = 1
                clear_toast()
                clear_selection()
                return
            if SfxOn:
                mixer.Sound.play(powerupselected)
            if canplace:
                pit = [selcolor if elem==0 else elem for elem in pit]
                selcolor = 0
                canplace = False
                draw_pit()
            powerups = [1 if elem==2 else elem for elem in powerups]
            powerups[3] = 2
            c.itemconfig(selected,image=star)
            toast("Clear a line in every direction from the Star.")
            return
        if inside(445,365,495,415,mousex,mousey) and powerups[4] != 0: #is shuffle clicked?.
            if powerups[4] == 1:
                powerups = [1 if elem==2 else elem for elem in powerups]
                if canplace:
                    pit = [selcolor if elem==0 else elem for elem in pit]
                    selcolor = 0
                    canplace = False
                    draw_pit()
                update_text()
                powerups[4] = 2
                toast("Use the Dice to replenish your pit.")
                mixer.Sound.play(powerupselected)
                c.itemconfig(selected,image=shuffle)
                return
            clear_toast()
            powerups = [1 if elem==2 else elem for elem in powerups]
            if SfxOn:
                mixer.Sound.play(shufflesound)
            c.itemconfig(scoredisp,text=score)
            powerupvalues[4] -= 1
            if powerupvalues[4] == 0:
                powerups[4] = 0
                c.itemconfig(shufflesquare,state=HIDDEN)
            c.itemconfig(selected,image=empty_block)
            #sets the pit to random colors
            for i in range(2,-1,-1):
                set_pit(randint(1,4),i)
                draw_animation(i*3,8,diceused,20)
                draw_pit()
            gameover_check()

        #* BUTTONS
        if inside(445,425,495,475,mousex,mousey): #Is restart clicked?
            ask_close()

        row = floor((mousex-SQUAREMARGINY)//49-1) 
        column = floor((mousey-SQUAREMARGINX)//49+1) #work out row and column of clicked space
        if powerups[0] == 2: #Removes the square for the pickaxe
            clear_toast()
            if row < 0 or row > 6 or column < 0 or column > 6:
                pass
            elif lookup (row,column) == 0:
                if SfxOn:
                    mixer.Sound.play(nomatch)
            else:
                powerupvalues[0] -= 1
                if powerupvalues[0] == 0:
                    powerups[0] = 0
                    c.itemconfig(pickaxesquare,state=HIDDEN)
                c.itemconfig(selected,image=empty_block)    
                if SfxOn:
                    mixer.Sound.play(pickused)
                draw_animation(row,column,breaking, 100)
                if SfxOn:
                    if lookup(row,column) == 12:
                        mixer.Sound.play(brickbreak)
                    else:
                        mixer.Sound.play(remove)
                score += 60*level
                update_text()
                c.itemconfig(scoredisp,text=score)
                set_square(0,row,column)
                return
        if powerups[1] == 2 and 0 <= column <= 6 and 0 <= row <= 6: #Removes the line for the throwing axe after checking that it is within bounds
            clear_toast()
            powerupvalues[1] -= 1
            if powerupvalues[1] == 0:
                powerups[1] = 0
                c.itemconfig(throwingaxesquare,state=HIDDEN)
            c.itemconfig(selected,image=empty_block)
            if SfxOn:
                mixer.Sound.play(axe)
            score += 120*level
            update_text()
            c.itemconfig(scoredisp,text=score)
            clear_line("H",row,column,False)
            return
        if powerups[2] == 2 and 0 <= column <= 6 and 0 <= row <= 6: #Removes the column for the jackhammer after checking that it is within bounds
            clear_toast()
            powerupvalues[2] -= 1
            if powerupvalues[2] == 0:
                powerups[2] = 0
                c.itemconfig(jackhammersquare,state=HIDDEN)
            c.itemconfig(selected,image=empty_block)
            if SfxOn:
                mixer.Sound.play(jackhammerused)
            score += 120*level
            update_text()
            c.itemconfig(scoredisp,text=score)
            clear_line("V",row,column,False)
            return
        if powerups[3] == 2 and 0 <= column <= 6 and 0 <= row <= 6: #Clears the starline
            clear_toast()
            powerupvalues[3] -= 1
            if powerupvalues[3] == 0:
                powerups[3] = 0
                c.itemconfig(starsquare,state=HIDDEN)
            c.itemconfig(selected,image=empty_block)
            if SfxOn:
                mixer.Sound.play(starnoise)
            score += 300*level
            update_text()
            c.itemconfig(scoredisp,text=score)
            clear_line("V",row,column,False)
            clear_line("H",row,column,False)
            clear_diagonal_lines(row,column)
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
                    if SfxOn:
                        mixer.Sound.play(diamondused)
                    busy = False
                    for i in range(len(grid)):
                        if grid[i] == lookup(row,column)-6: #sets all colors of the same to gray
                            currow, curcolumn = i%7,floor(i/7)
                            draw_animation(currow,curcolumn,breaking,75)
                            if SfxOn:
                                mixer.Sound.play(remove)
                            set_square(0,currow,curcolumn)
                            score += 10*level
                            c.itemconfig(scoredisp,text=score)
                            update_text()
                    score += 100*level
                    update_text()
                    c.itemconfig(scoredisp,text=score)
                    draw_animation(row,column,breaking,100)
                    set_square(0,row,column) #removes the current diamond
                    if all(0==x for x in grid):
                        score += 50*level
                        update_text()
                        c.itemconfig(scoredisp,text=score)
                        window.after(1000,reset_color)
                        window.after(1000,play_place_sound)
                    update_text()
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
        #works out if the clicked area was inside the grid, that the player can put a color there, that it is empty, and that there is a square next to it
        if row >= 0 and row < GRIDROWS and column >= 0 and column < GRIDROWS and canplace:
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
                canplace = False
                c.itemconfig(selected,image=empty_block)
                lines,direction = detect_line(row,column) #detects any lines

                for line in lines: #if there are any lines
                    set_square(0,line[0],line[1]) #clears all of the squares part of the line
                    score += 10*level
                    update_text()

                if len (lines) >= 3: 
                    if SfxOn:
                        mixer.Sound.play(remove)
                
                if len(lines) == 4: #Finds the lines with 4 gems and changes them into a drill with the opposite direction as the line.
                    set_square(5 if direction == "H" else 6,row,column)
                    if SfxOn:
                        mixer.Sound.play(drillcreated)
                elif len(lines) == 5:
                    set_square(selcolor+6,row,column) #finds the lines with 5 gems and changes them into a diamond
                    if SfxOn:
                        mixer.Sound.play(diamondcreated)
                elif len(lines) >= 6: #finds the lines with 6 or more gems and changes them into a bomb. gems used in 2 lines count twice
                    set_square(11,row,column)
                    if SfxOn:
                        mixer.Sound.play(bombcreated)
                
                #Need to go through all the lines again to remove all the bricks
                for line in lines:
                    clear_bricks(line)

                c.itemconfig(scoredisp,text=score)
                if all(0==x for x in grid):
                    score += 50*level
                    update_text()
                    c.itemconfig(scoredisp,text=score)
                    window.after(1000,reset_color)
                    window.after(1000,play_place_sound)
                selcolor = 0
                if len(lines) == 0:
                    play_place_sound()
                    score += level
                    update_text()
                    if mode == "normal":
                        for _ in range(level): #Puts more bricks on the board
                            set_brick()
            else:
                if SfxOn:
                    mixer.Sound.play(nomatch)

            if gameover_check(): return
            draw_board()
        elif column == 8: #if not check if row is where the colors are and that they can choose a color
            pick_color(row)
            if selcolor == 0:
                canplace = False
    else:
        if display:
            x1, y1, x2, y2 = startbounds
            if inside(x1,y1,x2,y2,mousex, mousey):
                if SfxOn:
                    mixer.Sound.play(clicked)
                mode = "normal"
                started = True
                start()
            x1, y1, x2, y2 = helpbounds
            if inside(x1,y1,x2,y2,mousex, mousey):
                if SfxOn:
                    mixer.Sound.play(clicked)
                mode = "time"
                started = True
                start()
        else:
            x1, y1, x2, y2 = startbounds
            if inside(x1,y1,x2,y2,mousex, mousey):
                display_modes()
                if SfxOn:
                    mixer.Sound.play(clicked)
            x1, y1, x2, y2 = helpbounds
            if inside(x1,y1,x2,y2,mousex, mousey) and not helping:
                if SfxOn:
                    mixer.Sound.play(clicked)
                helping = True
                tutstage = 1
                disp_help() 

def display_modes():
    global display
    display = True
    for item in [startbuttonbg,startbuttontext,helpbuttonbg,helpbuttontext]:
        c.itemconfig(item,state=HIDDEN)
    for item in [normalbuttonbg,normalbuttontext,timebuttonbg,timebuttontext]:
        c.itemconfig(item,state=NORMAL)

def clear_diagonal_lines(row,column):
    currow = row
    curcolumn = column
    while currow > 0 and curcolumn > 0:
        currow -= 1
        curcolumn -= 1
    while currow < 7 and curcolumn < 7:
        if lookup(currow,curcolumn) == 12:
            mixer.Sound.play(brickbreak)
        elif lookup(currow,curcolumn) != 0:
            mixer.Sound.play(remove)
        set_square(0,currow,curcolumn)
        draw_animation(currow,curcolumn,breaking,100)
        currow += 1
        curcolumn += 1
    
    currow = row
    curcolumn = column

    while currow < 6 and curcolumn > 0:
        currow += 1
        curcolumn -= 1
    while currow >= 0 and curcolumn < 7:
        if lookup(currow,curcolumn) == 12:
            mixer.Sound.play(brickbreak)
        elif lookup(currow,curcolumn) != 0:
            mixer.Sound.play(remove)
        set_square(0,currow,curcolumn)
        draw_animation(currow,curcolumn,breaking,100)
        currow -= 1
        curcolumn += 1

def explode(row, column, radius):
    global score
    if SfxOn:
        mixer.Sound.play(explosion)
    for i in range(row-radius,row+radius+1):
        for j in range(column-radius,column+radius+1):
            if not(i < 0 or i > 6 or j < 0 or j > 6):
                set_square(0,i,j)
                score += level
    set_square(0,row,column)
    draw_animation(row,column,explosions,75)
    if all(0==x for x in grid):
        toast("Board cleared!", 1)
        score += 50*level
        update_text()
        c.itemconfig(scoredisp,text=score)
        window.after(1000,reset_color)
        window.after(1000,play_place_sound)
    update_text()

def clear_bricks(line):
    #This next part checks all the blocks around where the line was.
    #If any bricks were there it breaks them
    if lookup(line[0]-1,line[1]) == 12:
        if not line[0]-1 < 0:
            set_square(0,line[0]-1,line[1])
            draw_animation(line[0]-1,line[1],brickbreaking,100)
            if SfxOn:
                mixer.Sound.play(brickbreak)

    if lookup(line[0],line[1]+1) == 12:
        if not line[1]+1 > 6:
            set_square(0,line[0],line[1]+1)
            draw_animation(line[0],line[1]+1,brickbreaking,100)
            if SfxOn:
                mixer.Sound.play(brickbreak)
    if lookup(line[0]+1,line[1]) == 12:
        if not line[0]+1 > 6:
            set_square(0,line[0]+1,line[1])
            draw_animation(line[0]+1,line[1],brickbreaking,100)
            if SfxOn:
                mixer.Sound.play(brickbreak)

    if lookup(line[0],line[1]-1) == 12:
        if not line[1]-1 < 0:
            set_square(0,line[0],line[1]-1)
            draw_animation(line[0],line[1]-1,brickbreaking,100)
            if SfxOn:
                mixer.Sound.play(brickbreak)

def clear_selection():
    c.itemconfig(selected,image=empty_block)

def gameover_check():
    global gameover, highscore
    if 0 not in grid and sum(x for x in grid if 10 >= x >=5) == 0: #game is over
        stop_music()
        if MusicOn:
            game_over_music()
        c.itemconfig(gameovertext,text="GAME OVER")
        c.itemconfig(playagaintext,text="Click anywhere to play again")
        c.itemconfig(finalscoretext, text="Your score was "+str(score))
        for square in board: #delete the grid so we can actually see the gameover text
            c.delete(square)
        gameover = True
        update_text()

        if score > highscore: 
            highscore = score
        with open("Gem miner/highscore.txt","w+") as hsfile:
            hsfile.write(str(highscore))
            hsfile.close()
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


def inside(x1,y1,x2,y2,testx, testy):
    return (testx > x1 and testx < x2) and (testy > y1 and testy < y2) #works out if a point is inside another

window.bind("<Button>",click)
window.bind("<Key>",key_press)
window.protocol("WM_DELETE_WINDOW", close)

window.mainloop()