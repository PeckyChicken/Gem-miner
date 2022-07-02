from tkinter import * #doing wildcard import to make it easier to use
from math import floor
from random import randint
from pygame import mixer, init
mixer.pre_init(44100, -16, 1, 512)
init()
mixer.init()

window = Tk() #sets up window
window.title("Gem miner")
window.iconbitmap("Gem miner/icon.ico")
WIDTH = 500
HEIGHT = 500
SQUARELEN = 50
SQUARESPACING = 50
SQUAREMARGINX = 75
SQUAREMARGINY = 25
PITSQUARESPACING = 150
gameover = False
squarey = SQUAREMARGINY
GRIDROWS = 7
PITSQUAREY = 425
STARTERMOVES = 30
score = 0
level = 1

MusicOn = True
SfxOn = True

try:
    with open("Gem miner/highscore.txt","r+") as hsfile:
        highscore = hsfile.read()
        highscore = int(highscore.strip())
        hsfile.close()
except (FileNotFoundError, ValueError):
    highscore = 0



canplace = False
selcolor = 0
c = Canvas(window,width=WIDTH,height=HEIGHT, bg="gray") #sets up canvas
c.pack(fill="both")
scoretext = c.create_text(40,20,text="Score",state=HIDDEN)
scoredisp = c.create_text(40,50,text=0,font=("Helvetica",30),state=HIDDEN)
leveltext = c.create_text(40,100,text="Level",state=HIDDEN)
leveldisp = c.create_text(40,130,text=1,font=("Helvetica",30),state=HIDDEN)

gameovertext = c.create_text(WIDTH/2,HEIGHT/2-25,font=("Helvetica",50))
playagaintext = c.create_text(WIDTH/2,HEIGHT/2+25,font=("Helvetica",30))
finalscoretext = c.create_text(WIDTH/2,HEIGHT/2+75,font=("Helvetica",15))
toasttext = c.create_text(WIDTH/2,HEIGHT/2 + 150,font=("Helvetica",15),text="Click again if you really want to restart.",state=HIDDEN)
highscoretext = c.create_text(10,20,font=("Helvetica",15),anchor="w",text=f"High score: {highscore}")
clickcount = 0

#imports the images
red_block = PhotoImage(file = "Gem miner/red_block.png")
yellow_block = PhotoImage(file = "Gem miner/yellow_block.png")
green_block = PhotoImage(file = "Gem miner/green_block.png")
blue_block = PhotoImage(file = "Gem miner/blue_block.png")
empty_block = PhotoImage(file = "Gem miner/empty.png")
vdrill = PhotoImage(file = "Gem miner/rocket_vertical.png")
hdrill = PhotoImage(file = "Gem miner/rocket_horizontal.png")
red_diamond = PhotoImage(file = "Gem miner/red_ball.png")
yellow_diamond = PhotoImage(file = "Gem miner/yellow_ball.png")
green_diamond = PhotoImage(file = "Gem miner/green_ball.png")
blue_diamond = PhotoImage(file = "Gem miner/blue_ball.png")
rainbow_diamond = PhotoImage(file = "Gem miner/rain_ball.png")
bomb = PhotoImage(file = "Gem miner/bomb.png")
bricks = PhotoImage(file = "Gem miner/bricks.png")
jackhammer = PhotoImage(file = "Gem miner/jackhammer.png")
pickaxe = PhotoImage(file = "Gem miner/pickaxe.png")
throwingaxe = PhotoImage(file = "Gem miner/throwing axe.png")
gem_bag = PhotoImage(file = "Gem miner/gem bag.png")
shuffle = PhotoImage(file = "Gem miner/shuffle.png")
restart = PhotoImage(file = "Gem miner/restartbutton.png")
brickp1 = PhotoImage(file = "Gem miner/bricks_particle_1.png")
brickp2 = PhotoImage(file = "Gem miner/bricks_particle_2.png")
brickp3 = PhotoImage(file = "Gem miner/bricks_particle_3.png")
brickp4 = PhotoImage(file = "Gem miner/bricks_particle_4.png")
button = PhotoImage(file = "Gem miner/button.png")
backgroundimg = PhotoImage(file = "Gem miner/TitleBG.png")
tut1 = PhotoImage(file = "Gem miner/Tutorial1.png")
tut2 = PhotoImage(file = "Gem miner/Tutorial2.png")
tut3 = PhotoImage(file = "Gem miner/Tutorial3.png")
tut4 = PhotoImage(file = "Gem miner/Tutorial4.png")
tut5 = PhotoImage(file = "Gem miner/Tutorial5.png")
tut6 = PhotoImage(file = "Gem miner/Tutorial6.png")
music = PhotoImage(file = "Gem miner/music_yes.png")
sfx = PhotoImage(file = "Gem miner/sfx_yes.png")
nomusic = PhotoImage(file = "Gem miner/music_no.png")
nosfx = PhotoImage(file = "Gem miner/sfx_no.png")

bg = c.create_image(WIDTH/2,HEIGHT/2,image=backgroundimg)

selected = c.create_image(470,50,image=empty_block,state=HIDDEN)

tutimage = c.create_image(WIDTH/2,HEIGHT/2,image=tut1,state=HIDDEN)


#Importing the sounds
bombcreated = mixer.Sound("Gem miner/bombcreated.wav")
explosion = mixer.Sound("Gem miner/boom.wav")
remove = mixer.Sound("Gem miner/break.wav")
brickbreak = mixer.Sound("Gem miner/brick_break.wav")
clearall = mixer.Sound("Gem miner/clearall.wav")
diamondcreated = mixer.Sound("Gem miner/diamondcreated.wav")
diamondused = mixer.Sound("Gem miner/diamondused.wav")
drillcreated = mixer.Sound("Gem miner/drillcreated.wav")
drillused = mixer.Sound("Gem miner/drillused.wav")
gembagused = mixer.Sound("Gem miner/gem bag.wav")
javalinused = mixer.Sound("Gem miner/javalinused.wav")
nomatch = mixer.Sound("Gem miner/nomatch.wav")
pickused = mixer.Sound("Gem miner/pickaxeused.wav")
placed = mixer.Sound("Gem miner/place.wav")
powerupselected = mixer.Sound("Gem miner/powerupselected.wav")
shufflesound = mixer.Sound("Gem miner/shuffle.wav")
axe = mixer.Sound("Gem miner/Throwing axe.wav")
title1 = mixer.Sound("Gem miner/title1.wav")
title2 = mixer.Sound("Gem miner/title2.wav")
main1 = mixer.Sound("Gem miner/main1.wav")
main2 = mixer.Sound("Gem miner/main2.wav")
advance = mixer.Sound("Gem miner/nextlevel.wav")
gameoversound = mixer.Sound("Gem miner/endofgame.wav")
clicked = mixer.Sound("Gem miner/click.wav")


powerups = [1,1,1,1,1] #sets up the powerup squares
pickaxesquare = c.create_image(470,150,image=pickaxe,state=HIDDEN)
throwingaxesquare = c.create_image(470,210,image=throwingaxe,state=HIDDEN)
javalinsquare = c.create_image(470,270,image=jackhammer,state=HIDDEN)
gem_bagsquare = c.create_image(470,330,image=gem_bag,state=HIDDEN)
shufflesquare = c.create_image(470,390,image=shuffle,state=HIDDEN)

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

startbuttonbg = c.create_image(WIDTH/2,HEIGHT/2-35,image=button)
startbuttontext = c.create_text(WIDTH/2,HEIGHT/2-35,text="Start",font=("Helvetica",25),fill="white")

helpbuttonbg = c.create_image(WIDTH/2,HEIGHT/2+35,image=button)
helpbuttontext = c.create_text(WIDTH/2,HEIGHT/2+35,text="How to play",font=("Helvetica",25),fill="white")

startbounds = (WIDTH/2-100,HEIGHT/2-60,WIDTH/2+100,HEIGHT/2-10)
helpbounds = (WIDTH/2-100,HEIGHT/2+10,WIDTH/2+100,HEIGHT/2+60)

started = False
helping = False
tutstage = 0

#*IDS
itemid = {0:empty_block,1:red_block,2:yellow_block,3:green_block,4:blue_block,5:vdrill,6:hdrill,7:red_diamond,8:yellow_diamond,9:green_diamond,10:blue_diamond,11:bomb,12:bricks} #sets up the item ids

board = list() #sets up the board
#Music loop


repeats = 0
def titleMusic():
    global repeats, loop
    if repeats == 0:
        mixer.Sound.play(title1)
    else:
        mixer.Sound.play(title2)
    repeats += 1
    loop = window.after(16000,titleMusic)
titleMusic()

def gameMusic():
    global repeats, loop2
    if repeats == 0:
        mixer.Sound.play(main1)
        loop2 = window.after(27850,gameMusic)
    else: 
        mixer.Sound.play(main2)
        loop2 = window.after(23600,gameMusic)
    repeats += 1

def stopMusic():
    global repeats
    mixer.stop()
    try:
        window.after_cancel(loop)
    except NameError: pass
    try:
        window.after_cancel(loop2)
    except NameError: pass
    repeats = 0

def DrawBoard():
    if not gameover:
        global board
        squarey = SQUAREMARGINY
        for object in board:
            c.delete(object) #deletes all current squares so we can redraw them
        board.clear()
        for square in range(len(grid)):
            board.append(c.create_image(SQUAREMARGINX+SQUARELEN*(square%GRIDROWS)+25,
                (squarey+(floor(square/GRIDROWS)*SQUARESPACING))+25,
                image=itemid[grid[square]]))
            #Draws the images via some complicated calculations. SQUARELEN is how big the images should be, and it is multiplying that by the square number to space it out. It uses modulo to stop it going to far as the board is only 7x7. For the y it works out what row its on and draws the image there. SQUAREMARGINX is how far it starts off the left of the screen
    
def DrawPowerups():
    global pickaxesquare, throwingaxesquare, javalinsquare, gem_bagsquare, shuffle, powerups
    powerups = [1,1,1,1,1]
    c.itemconfig(pickaxesquare,state=NORMAL)
    c.itemconfig(throwingaxesquare,state=NORMAL)
    c.itemconfig(javalinsquare,state=NORMAL)
    c.itemconfig(gem_bagsquare,state=NORMAL)
    c.itemconfig(shufflesquare,state=NORMAL)
    c.itemconfig(restartsquare,state=NORMAL)
def SetSquare(color,x,y):
    global board
    itemid = y*GRIDROWS + x #works out the id of the list given the x and y
    grid[itemid] = color #replaces the current color with the new one
    DrawBoard()

def nextLevel():
    global level
    #This complicated setup means that the player will advance a level when they get to 500, 1000, 5000, etc.
    reqscore = (((level+1)%2)+1) * 500 * 10 ** (1+(level - 3) // 2)
    # print(f"Required score: {reqscore}")
    if score >= reqscore:
        level += 1
        if SfxOn:
            mixer.Sound.play(advance)
def Lookup(x,y):
    try:
        color = grid[y*GRIDROWS+x] #find the color of the grid square
        return color
    except IndexError:
        return 0

def GetID(x,y):
    return board[y*GRIDROWS+x]

def SetPit(color,pos):
    pit[pos] = color #changes color of the pit objects

def DetectLine(x,y):
    count = 0
    usedsquares = list()
    curx = x
    cury = y
    #Moves down as far as there are matches
    while Lookup(curx,cury) == Lookup(x,y):
        count += 1
        usedsquares.append([curx,cury]) #add the current match to the list
        cury += 1 #move it down one
        if cury >= 7: break #stop it from overflowing
    if count != 0:
        curx = x
        cury = y-1 #subtracts one so it doesnt double count the first one
        #Once it has finished if it found anything it goes back up to look for other matches
        while Lookup(curx,cury) == Lookup(x,y):
            if cury < 0: break
            count += 1 
            usedsquares.append([curx,cury]) #add the current match to the list
            cury -= 1 #move it up one row
    
    #Does it again for the up direction, doesnt need to check for down because it just did that
    while Lookup(curx,cury) == Lookup(x,y):
        if cury < 0: break
        count += 1 
        usedsquares.append([curx,cury]) #add the current match to the list
        cury -= 1 #move it up one row
    if count == 5: #Return if already a diamond
        return usedsquares
    if count < 3: #If there were no lines that way they do not count
        count == 0
        usedsquares.clear()
    #now for the horizontal lines
    xcount = 0 #resetting things for the horizontal check
    xusedsquares = list()
    curx = x
    cury = y
    #checking for anything to the right
    while Lookup(curx,cury) == Lookup(x,y):
        xcount += 1
        xusedsquares.append([curx,cury]) #add the current match to the list
        curx += 1 #move it right one column
        if curx >= 7: break
    if xcount != 0:
        curx = x-1 #subtracts one to avoid double counting
        cury = y
        #Go back to the left to look for more matches
        while Lookup(curx,cury) == Lookup(x,y):
            if curx < 0: break
            xcount += 1
            xusedsquares.append([curx,cury]) #add the current match to the list
            curx -= 1 #move it back left
    if xcount < 3: #If there were no lines that way they do not count
        xcount == 0
        xusedsquares.clear()
    if xcount == 5: #Return if already a diamond
        return xusedsquares
    if len(xusedsquares)+len(usedsquares) >= 6:
        return xusedsquares+usedsquares
    elif len(xusedsquares) >= 3:
        return xusedsquares
    elif len(usedsquares) >= 3:
        return usedsquares
    #Now to check for left on its own
    while Lookup(curx,cury) == Lookup(x,y):
        if curx < 0: break
        xcount += 1
        xusedsquares.append([curx,cury]) #add the current match to the list
        curx -= 1 #move it left one column
    if xcount == 5:
        return xusedsquares
    if len(xusedsquares)+len(usedsquares) >= 6:
        return xusedsquares+usedsquares
    elif len(xusedsquares) >= 3:
        return xusedsquares
    elif len(usedsquares) >= 3:
        return usedsquares
    return []

def ResetColor(): #sets a random square to a color
    SetSquare(randint(1,4),randint(0,6),randint(0,6))

def ResetBrick(): #sets a random square to a brick
    SetSquare(12,randint(0,6),randint(0,6))

def PlayPlaceSound(): #only putting it in a function by itself so i can call it from a window.after
    if SfxOn:
        mixer.Sound.play(placed)

def start():
    global repeats
    ResetColor()
    ResetColor()
    ResetBrick()
    ResetBrick()
    ResetBrick()
    ResetBrick()
    ResetBrick()
    DrawPowerups()
    DrawBoard()
    DrawPit()
    c.itemconfig(scoredisp,state=NORMAL)
    c.itemconfig(scoretext,state=NORMAL)
    c.itemconfig(leveldisp,state=NORMAL)
    c.itemconfig(leveltext,state=NORMAL)
    c.itemconfig(selected,state=NORMAL)
    c.itemconfig(bg,state=HIDDEN)
    c.itemconfig(startbuttonbg,state=HIDDEN)
    c.itemconfig(startbuttontext,state=HIDDEN)
    c.itemconfig(helpbuttonbg,state=HIDDEN)
    c.itemconfig(helpbuttontext,state=HIDDEN)
    c.itemconfig(highscoretext,state=HIDDEN)
    stopMusic()
    gameMusic()

def clearboard():
    global score, grid
    toast("Board cleared!", 1)
    grid =  [0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,
            0,0,0,0,0,0,0]
    score += 500*level
    updatetext()
    c.itemconfig(scoredisp,text=score)
    window.after(1000,ResetColor)
    window.after(1000,ResetColor)
    DrawBoard()
 
def resetcount():
    global clickcount
    clickcount = 0

def cleartoast():
    c.itemconfig(toasttext,state=HIDDEN)

def toast(msg,time=-1):
    c.itemconfig(toasttext,state=NORMAL,text=msg)
    if time >= 0:
        window.after(time*1000,cleartoast)

def askclose():
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
        ResetColor()
        ResetColor()
        ResetBrick()
        ResetBrick()
        ResetBrick()
        ResetBrick()
        ResetBrick()
        DrawPowerups()
        selcolor = 0
        c.itemconfig(selected,image=empty_block)
        score = 0
        level = 1
        updatetext()
        gameover = False
        DrawBoard()
        c.itemconfig(scoredisp,text=score)
        c.itemconfig(gameovertext,text="")
        c.itemconfig(playagaintext,text="")
        c.itemconfig(finalscoretext,text="")
        c.itemconfig(toasttext, state=HIDDEN)
        clickcount = 0
        return
    else:
        window.after(2000, resetcount)
    
def updatetext(): #Updates the font size depending on how many points the player has.
    c.itemconfig(scoredisp,font=("Helvetica",defaulttextsize-len(str(score))*3))
    nextLevel()
    c.itemconfig(leveldisp,text=str(level))
    c.itemconfig(leveldisp,font=("Helvetica",defaulttextsize-len(str(level))*3))
updatetext()


def disphelp():
    global helping
    c.itemconfig(bg,state=HIDDEN)
    c.itemconfig(startbuttonbg,state=HIDDEN)
    c.itemconfig(startbuttontext,state=HIDDEN)
    c.itemconfig(helpbuttonbg,state=HIDDEN)
    c.itemconfig(helpbuttontext,state=HIDDEN)
    match tutstage:
        case 1:
            c.itemconfig(tutimage,image=tut1,state=NORMAL)
        case 2:
            c.itemconfig(tutimage,image=tut2,state=NORMAL)
        case 3:
            c.itemconfig(tutimage,image=tut3,state=NORMAL)
        case 4:
            c.itemconfig(tutimage,image=tut4,state=NORMAL)
        case 5:
            c.itemconfig(tutimage,image=tut5,state=NORMAL)
        case 6:
            c.itemconfig(tutimage,image=tut6,state=NORMAL)
        case _: 
            c.itemconfig(tutimage,state=HIDDEN)
            helping = False
            c.itemconfig(bg,state=NORMAL)
            c.itemconfig(startbuttonbg,state=NORMAL)
            c.itemconfig(startbuttontext,state=NORMAL)
            c.itemconfig(helpbuttonbg,state=NORMAL)
            c.itemconfig(helpbuttontext,state=NORMAL)
#* HANDLING

def clear3x3(row,column):
    global score
    if SfxOn:
        mixer.Sound.play(drillused)
    for square in range(GRIDROWS):
        if Lookup(row,square) != 0:
            score += 10*level
            updatetext()
            c.itemconfig(scoredisp,text=score)
        SetSquare(0,row,square) #sets all squares in the column to grey

        if Lookup(row-1,square) != 0:
            score += 10*level
            updatetext()
            c.itemconfig(scoredisp,text=score)
        SetSquare(0,row-1,square) #sets all squares in the column to grey

        
        if Lookup(row+1,square) != 0:
            score += 10*level
            updatetext()
            c.itemconfig(scoredisp,text=score)
        SetSquare(0,row+1,square) #sets all squares in the column to grey

        if Lookup(square,column) != 0:
            score += 10*level
            updatetext()
            c.itemconfig(scoredisp,text=score)
        SetSquare(0,square,column) #sets all squares in the row to grey

        
        if Lookup(square,column-1) != 0:
            score += 10*level
            updatetext()
            c.itemconfig(scoredisp,text=score)
        SetSquare(0,square,column-1) #sets all squares in the row to grey

        
        if Lookup(square,column+1) != 0:
            score += 10*level
            updatetext()
            c.itemconfig(scoredisp,text=score)
        SetSquare(0,square,column+1) #sets all squares in the row to grey

def convertcolors(item,row,column,samesquare):
    global score
    leftid = Lookup(row-1,column)
    rightid = Lookup(row+1,column)
    upid = Lookup(row,column-1)
    downid = Lookup(row,column+1)
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
        if grid[i] == Lookup(diamondx,diamondy)-6: #sets all colors of the same to the item
            SetSquare(11 if item == "bomb" else randint(5,6),i%7,floor(i/7))
            score += 10*level
            updatetext()
    SetSquare(11 if item == "bomb" else randint(5,6),diamondx,diamondy)

def clear2lines(row,column):
    global score
    if SfxOn:
        mixer.Sound.play(drillused)
    for square in range(GRIDROWS):
        if Lookup(row,square) != 0:
            score += 10*level
            updatetext()
            c.itemconfig(scoredisp,text=score)
        SetSquare(0,row,square) #sets all squares in the column to grey
        if Lookup(square,column) != 0:
            score += 10*level
            updatetext()
            c.itemconfig(scoredisp,text=score)
        SetSquare(0,square,column) #sets all squares in the row to grey

def bigbang(row,column):
    global score
    score += 50*level
    if SfxOn:
        mixer.Sound.play(explosion)
    for i in range(row-3,row+4):
        for j in range(column-3,column+4):
            if not(i < 0 or i > 6 or j < 0 or j > 6):
                score += level
                SetSquare(0,i,j)
    SetSquare(0,row,column)

def handleitems(item,row,column):
    global score
    leftid = Lookup(row-1,column)
    rightid = Lookup(row+1,column)
    upid = Lookup(row,column-1)
    downid = Lookup(row,column+1)
    #Checks if there is a diamond next to it
    if 6 < leftid < 11 or 6 < rightid < 11\
        or 6 < upid < 11 or 6 < downid < 11:
        if item == 'diamond':
            if SfxOn:
                mixer.Sound.play(clearall)
            window.after(2250,clearboard)
            return True
        convertcolors(item,row,column,False)
        return True
    
    #Checks if there is a drill next to it

    elif leftid in (5,6) or rightid in (5,6)\
        or downid in (5,6) or upid in (5,6):
        if item == "bomb":
            clear3x3(row,column)
            return True
        if item == "diamond":
            convertcolors("hdrill",row,column,True)
            return True
        clear2lines(row,column)
        return True


    #Checks if there is a bomb next to it
    elif 11 in (leftid,rightid,upid,downid):
        if item in ("hdrill","vdrill"):
            clear3x3(row,column)
            return True
        if item == "bomb":
            bigbang(row,column)
            return True
        convertcolors("bomb",row,column,True)
        return True

    updatetext()
    return False


def clearline(direction,row,column):
    global score
    if SfxOn:
        mixer.Sound.play(drillused)
    for square in range(GRIDROWS):
        curx, cury = square if direction == "H" else row, square if direction == "V" else column
        cursquare = Lookup(curx,cury)
        if cursquare != 0:
            score += 10*level
            updatetext()
            c.itemconfig(scoredisp,text=score)
            if (curx, cury) != (row,column):
                if cursquare == 5:
                    clearline("V",curx,cury)
                if cursquare == 6:
                    clearline("H",curx,cury)
        SetSquare(0,curx,cury) #sets all squares in the column to blank
    if all(0==x for x in grid):
        score += 50*level
        updatetext()
        c.itemconfig(scoredisp,text=score)
        window.after(1000,ResetColor)
        window.after(1000,PlayPlaceSound)

def close():
    global highscore
    if score > highscore:
        highscore = score
        with open("Gem miner/highscore.txt","w+") as hsfile:
            hsfile.write(str(highscore))
            hsfile.close()
    window.destroy()

#Main event
def click(event):
    global selcolor, pit, canplace, pitobjects, grid, score, gameover, powerups, started, helping, tutstage, level, highscore, MusicOn, SfxOn, repeats
    nextLevel()
    mousex = event.x
    mousey = event.y #get mouse x and y
    # print(f"X: {mousex}, Y: {mousey}")
    if helping:
        tutstage += 1
        disphelp()
        return

    if inside(0,450,50,500,mousex,mousey): #Is music clicked?
        if MusicOn:
            MusicOn = False
            stopMusic()
            c.itemconfig(musicsquare, image = nomusic)
        else:
            MusicOn = True
            repeats = 0
            if started:
                gameMusic()
            else:
                titleMusic()
            c.itemconfig(musicsquare, image = music)

    if inside(0,400,50,450,mousex,mousey): #Is sfx clicked?
        if SfxOn:
            SfxOn = False
            c.itemconfig(sfxsquare, image = nosfx)
        else:
            SfxOn = True
            c.itemconfig(sfxsquare, image = sfx)
    
    if started:
        if gameover: #if the game is over run it again

            if SfxOn:
                mixer.Sound.play(clicked)
            grid = [0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0,
                    0,0,0,0,0,0,0]
            ResetColor()
            ResetColor()
            ResetBrick()
            ResetBrick()
            ResetBrick()
            ResetBrick()
            ResetBrick()
            DrawPowerups()
            selcolor = 0
            c.itemconfig(selected,image=empty_block)
            score = 0
            level = 1
            gameover = False
            DrawBoard()
            c.itemconfig(scoredisp,text=score)
            c.itemconfig(gameovertext,text="")
            c.itemconfig(playagaintext,text="")
            c.itemconfig(finalscoretext,text="")
            gameMusic()
            updatetext()
            return
        if not canplace:
            if inside(445,125,495,175,mousex,mousey) and powerups[0] == 1: #is pickaxe clicked?
                if SfxOn:
                    mixer.Sound.play(powerupselected)
                c.itemconfig(selected,image=pickaxe)
                powerups = [1 if elem==2 else elem for elem in powerups]
                powerups[0] = 2
                toast("The Pickaxe clears the square you click on.")
                return
            if inside(445,185,495,235,mousex,mousey) and powerups[1] == 1: #is throwing axe clicked?
                if SfxOn:
                    mixer.Sound.play(powerupselected)
                powerups = [1 if elem==2 else elem for elem in powerups]
                powerups[1] = 2
                c.itemconfig(selected,image=throwingaxe)
                toast("Click on any square to clear a row with the Axe.")
                return
            if inside(445,245,495,295,mousex,mousey) and powerups[2] == 1: #is jackhammer clicked?
                if SfxOn:
                    mixer.Sound.play(powerupselected)
                powerups = [1 if elem==2 else elem for elem in powerups]
                powerups[2] = 2
                c.itemconfig(selected,image=jackhammer)
                toast("Clear a whole column with the Jackhammer.")
                return
            if inside(445,305,495,355,mousex,mousey) and powerups[3] == 1: #is gem bag clicked?
                if SfxOn:
                    mixer.Sound.play(gembagused)
                    mixer.Sound.play(clicked)
                score += 30*level
                updatetext()
                c.itemconfig(scoredisp,text=score)
                powerups = [1 if elem==2 else elem for elem in powerups]
                powerups[3] = 0
                c.itemconfig(selected,image=empty_block)
                for _ in [0,1,2]: #sets 3 random squares to random colors
                    pickeditem = -1
                    while (not grid[pickeditem] == 0) and 0 in grid:
                        pickeditem = randint(0,len(grid)-1)
                    grid[pickeditem] = randint(1,4)
                DrawBoard()
                c.itemconfig(gem_bagsquare,state=HIDDEN)
                gameovercheck()
                return
            if inside(445,365,495,415,mousex,mousey) and powerups[4] == 1: #is shuffle clicked?.
                if SfxOn:
                    mixer.Sound.play(shufflesound)
                    mixer.Sound.play(clicked)
                c.itemconfig(scoredisp,text=score)
                powerups = [1 if elem==2 else elem for elem in powerups]
                powerups[4] = 0
                c.itemconfig(selected,image=empty_block)
                #sets the pit to random colors
                SetPit(randint(1,4),0)
                SetPit(randint(1,4),1)
                SetPit(randint(1,4),2)
                DrawPit()
                c.itemconfig(shufflesquare,state=HIDDEN)
                gameovercheck()
                return
            #* BUTTONS
            if inside(445,425,495,475,mousex,mousey): #Is restart clicked?
                askclose()

        row = floor((mousex-SQUAREMARGINY)/49-1) 
        column = floor((mousey-SQUAREMARGINX)/49+1) #work out row and column of clicked space
        if powerups[0] == 2: #Removes the square for the pickaxe
            cleartoast()
            if row < 0 or row > 6 or column < 0 or column > 6:
                pass
            elif Lookup (row,column) == 0:
                if SfxOn:
                    mixer.Sound.play(nomatch)
            else:
                if SfxOn:
                    mixer.Sound.play(pickused)
                score += 60*level
                updatetext()
                c.itemconfig(scoredisp,text=score)
                SetSquare(0,row,column)
                powerups[0] = 0
                c.itemconfig(pickaxesquare,state=HIDDEN)
                c.itemconfig(selected,image=empty_block)
        if powerups[1] == 2 and 0 <= column <= 6 and 0 <= row <= 6: #Removes the line for the throwing axe after checking that it is within bounds
            cleartoast()
            if SfxOn:
                mixer.Sound.play(axe)
            score += 120*level
            updatetext()
            c.itemconfig(scoredisp,text=score)
            for i in range(7):
                SetSquare(0,i,column)
            powerups[1] = 0
            c.itemconfig(throwingaxesquare,state=HIDDEN)
            c.itemconfig(selected,image=empty_block)
        if powerups[2] == 2 and 0 <= column <= 6 and 0 <= row <= 6: #Removes the column for the jackhammer after checking that it is within bounds
            cleartoast()
            if SfxOn:
                mixer.Sound.play(javalinused)
            score += 120*level
            updatetext()
            c.itemconfig(scoredisp,text=score)
            for i in range(7):
                SetSquare(0,row,i)
            powerups[2] = 0
            c.itemconfig(javalinsquare,state=HIDDEN)
            c.itemconfig(selected,image=empty_block)
        try:
            # *ITEM
            leftid = Lookup(row-1,column)
            rightid = Lookup(row+1,column)
            upid = Lookup(row,column-1)
            downid = Lookup(row,column+1)

            if Lookup(row,column) == 5: #its a vdrill
                if handleitems("hdrill",row,column): return

                clearline("V",row,column)
            if Lookup(row,column) == 6: #its an hdrill
                if handleitems("hdrill",row,column): return

                clearline("H",row,column)

            if Lookup(row,column) > 6 and Lookup(row,column) < 11: #its a diamond
                if handleitems("diamond",row,column): return

                if SfxOn:
                    mixer.Sound.play(diamondused)
                for i in range(len(grid)):
                    if grid[i] == Lookup(row,column)-6: #sets all colors of the same to gray
                        SetSquare(0,i%7,floor(i/7))
                        score += 10*level
                        updatetext()
                score += 100*level
                updatetext()
                c.itemconfig(scoredisp,text=score)
                SetSquare(0,row,column) #removes the current diamond
                if all(0==x for x in grid):
                    score += 50*level
                    updatetext()
                    c.itemconfig(scoredisp,text=score)
                    window.after(1000,ResetColor)
                    window.after(1000,PlayPlaceSound)
                updatetext()
                return
            if Lookup(row,column) == 11: #its a bomb
                if handleitems("bomb",row,column): return
                
                if SfxOn:
                    mixer.Sound.play(explosion)
                score += 10*level
                for i in range(row-1,row+2):
                    for j in range(column-1,column+2):
                        if not(i < 0 or i > 6 or j < 0 or j > 6):
                            SetSquare(0,i,j)
                            score += level
                SetSquare(0,row,column)
                if all(0==x for x in grid):
                    toast("Board cleared!", 1)
                    score += 50*level
                    updatetext()
                    c.itemconfig(scoredisp,text=score)
                    window.after(1000,ResetColor)
                    window.after(1000,PlayPlaceSound)
                updatetext()
                return
        except IndexError:
            pass
        #works out if the clicked area was inside the grid, that the player can put a color there, that it is empty, and that there is a square next to it
        if row >= 0 and row < GRIDROWS and column >= 0 and column < GRIDROWS and canplace:
            # print(f'Row: {row}, Column: {column}, Row+1: {row+1}, Column+1: {column+1}, Row-1: {row-1}, Column-1: {column-1}')
            if (Lookup(row,column) == 0 and
                    (
                    (row > 0 and Lookup(row-1,column)) or
                    (row < 6 and Lookup(row+1,column)) or
                    (column < 6 and Lookup(row,column+1)) or
                    (column > 0 and Lookup(row,column-1))
                    )):
                pit = [randint(1,4) if elem==0 else elem for elem in pit]
                DrawPit()
                SetSquare(selcolor,row,column)
                canplace = False
                c.itemconfig(selected,image=empty_block)
                lines = DetectLine(row,column) #detects any lines
                if len (lines) >= 3: 
                    if SfxOn:
                        mixer.Sound.play(remove)
                for line in lines: #if there are any lines
                    #This next part checks all the blocks around where the line was.
                    #If any bricks were there it breaks them
                    if Lookup(line[0]-1,line[1]) == 12:
                        if not line[0]-1 < 0:
                            SetSquare(0,line[0]-1,line[1])
                            if SfxOn:
                                mixer.Sound.play(brickbreak)
                    if Lookup(line[0]+1,line[1]) == 12:
                        if not line[0]+1 > 6:
                            SetSquare(0,line[0]+1,line[1])
                            if SfxOn:
                                mixer.Sound.play(brickbreak)
                    if Lookup(line[0],line[1]-1) == 12:
                        if not line[1]-1 < 0:
                            SetSquare(0,line[0],line[1]-1)
                            if SfxOn:
                                mixer.Sound.play(brickbreak)
                    if Lookup(line[0],line[1]+1) == 12:
                        if not line[1]+1 > 6:
                            SetSquare(0,line[0],line[1]+1)
                            if SfxOn:
                                mixer.Sound.play(brickbreak)
                    SetSquare(0,line[0],line[1]) #clears all of the squares part of the line
                    score += 10*level
                    updatetext()
                
                if len(lines) == 0:
                    if SfxOn:
                        mixer.Sound.play(placed)
                    score += 1*level
                    updatetext()
                    for _ in range(level): #Puts more bricks on the board
                        pickeditem = -1
                        while (not grid[pickeditem] == 0) and 0 in grid:
                            pickeditem = randint(0,len(grid)-1)
                        grid[pickeditem] = 12

                if len(lines) == 4: #finds the lines with 4 colors and changes them into a drill
                    SetSquare(randint(5,6),row,column)
                    if SfxOn:
                        mixer.Sound.play(drillcreated)
                elif len(lines) == 5:
                    SetSquare(selcolor+6,row,column) #finds the lines with 5 colors and changes them into a diamond
                    if SfxOn:
                        mixer.Sound.play(diamondcreated)
                elif len(lines) >= 6: #finds the lines with 6 or more colors and changes them into a bomb. Colors used in 2 lines count twice
                    SetSquare(11,row,column)
                    if SfxOn:
                        mixer.Sound.play(bombcreated)

                c.itemconfig(scoredisp,text=score)
                if all(0==x for x in grid):
                    score += 50*level
                    updatetext()
                    c.itemconfig(scoredisp,text=score)
                    window.after(1000,ResetColor)
                    window.after(1000,PlayPlaceSound)
                selcolor = 0
            else:
                if SfxOn:
                    mixer.Sound.play(nomatch)

            if gameovercheck(): return
            DrawBoard()
        elif column == 8: #if not check if row is where the colors are and that they can choose a color
            if row == 0:
                cleartoast()
                powerups = [1 if elem==2 else elem for elem in powerups]
                canplace = True #make sure that the player can place a color
                c.itemconfig(pitobjects[0],image=itemid[selcolor]) #sets the color to gray temporarily
                selcolor, pit[0] = pit[0], selcolor #swaps the selected color with the one in the pit
                c.itemconfig(selected,image=itemid[selcolor]) #fills the selected box with whatever color was chosen
            elif row == 3: #same as above
                cleartoast()
                powerups = [1 if elem==2 else elem for elem in powerups]
                canplace = True
                c.itemconfig(pitobjects[1],image=itemid[selcolor])
                selcolor, pit[1] = pit[1], selcolor
                c.itemconfig(selected,image=itemid[selcolor])
            elif row == 6: #same as above
                cleartoast()
                powerups = [1 if elem==2 else elem for elem in powerups]
                canplace = True
                c.itemconfig(pitobjects[2],image=itemid[selcolor])
                selcolor, pit[2] = pit[2], selcolor
                c.itemconfig(selected,image=itemid[selcolor])
            if selcolor == 0:
                canplace = False
    else:
        x1, y1, x2, y2 = startbounds
        if inside(x1,y1,x2,y2,mousex, mousey):
            started = True
            start()
        x1, y1, x2, y2 = helpbounds
        if inside(x1,y1,x2,y2,mousex, mousey) and not helping:
            helping = True
            tutstage = 1
            disphelp()

def gameovercheck():
    global gameover, highscore
    if 0 not in grid: #game is over
        stopMusic()
        if SfxOn:
            mixer.Sound.play(gameoversound)
        c.itemconfig(gameovertext,text="GAME OVER")
        c.itemconfig(playagaintext,text="Click anywhere to play again")
        c.itemconfig(finalscoretext, text="Your score was "+str(score))
        for square in board: #delete the grid so we can actually see the gameover text
            c.delete(square)
        gameover = True
        updatetext()

        if score > highscore: 
            highscore = score
        with open("Gem miner/highscore.txt","w+") as hsfile:
            hsfile.write(str(highscore))
            hsfile.close()
        return True #game is over
    return False #game is not over
def DrawPit():
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
window.protocol("WM_DELETE_WINDOW", close)

window.mainloop()