from tkinter import PhotoImage, Tk

from animations import create_animation

window = Tk() #sets up window
filepath = __file__+"/../"

red_block = PhotoImage(file = filepath+"Gem miner/Images/Gems/red_gem.png")
yellow_block = PhotoImage(file = filepath+"Gem miner/Images/Gems/yellow_gem.png")
green_block = PhotoImage(file = filepath+"Gem miner/Images/Gems/green_gem.png")
blue_block = PhotoImage(file = filepath+"Gem miner/Images/Gems/blue_gem.png")
empty_block = PhotoImage(file = filepath+"Gem miner/Images/UI/empty.png")

vdrill = PhotoImage(file = filepath+"Gem miner/Images/Tools/rocket_vertical.png")
hdrill = PhotoImage(file = filepath+"Gem miner/Images/Tools/rocket_horizontal.png")
red_diamond = PhotoImage(file = filepath+"Gem miner/Images/Tools/Diamonds/red_diamond.png")
yellow_diamond = PhotoImage(file = filepath+"Gem miner/Images/Tools/Diamonds/yellow_diamond.png")
green_diamond = PhotoImage(file = filepath+"Gem miner/Images/Tools/Diamonds/green_diamond.png")
blue_diamond = PhotoImage(file = filepath+"Gem miner/Images/Tools/Diamonds/blue_diamond.png")
rainbow_diamond = PhotoImage(file = filepath+"Gem miner/Images/Tools/Diamonds/rainbow_diamond.png")
bomb = PhotoImage(file = filepath+"Gem miner/Images/Tools/bomb.png")

bricks = PhotoImage(file = filepath+"Gem miner/Images/Animations/Bricks/bricks.png")
jackhammer = PhotoImage(file = filepath+"Gem miner/Images/Tools/jackhammer.png")
pickaxe = PhotoImage(file = filepath+"Gem miner/Images/Tools/pickaxe.png")
throwingaxe = PhotoImage(file = filepath+"Gem miner/Images/Tools/axe.png")
star = PhotoImage(file = filepath+"Gem miner/Images/Tools/star.png")
dice = PhotoImage(file = filepath+"Gem miner/Images/Tools/shuffle.png")

restart = PhotoImage(file = filepath+"Gem miner/Images/UI/restartbutton.png")
button = PhotoImage(file = filepath+"Gem miner/Images/UI/button.png")
titlebgimage = PhotoImage(file = filepath+"Gem miner/Images/Backgrounds/titlebg.png")

tut1,tut2,tut3,tut4,tut5,tut6 = create_animation(filepath+"Gem miner/Images/Tutorial","tutorial")



music = PhotoImage(file = filepath+"Gem miner/Images/UI/music_yes.png")
sfx = PhotoImage(file = filepath+"Gem miner/Images/UI/sfx_yes.png")
nomusic = PhotoImage(file = filepath+"Gem miner/Images/UI/music_no.png")
nosfx = PhotoImage(file = filepath+"Gem miner/Images/UI/sfx_no.png")

obstaclecard = PhotoImage(file = filepath+"Gem miner/Images/UI/obstacles_card.png")
survivalcard = PhotoImage(file = filepath+"Gem miner/Images/UI/survival_card.png")
timecard = PhotoImage(file = filepath+"Gem miner/Images/UI/time_card.png")
chromacard = PhotoImage(file = filepath+"Gem miner/Images/UI/chroma_card.png")
fade_image = PhotoImage(file = filepath+"Gem miner/Images/UI/fade.png")


explosions = create_animation(filepath+"Gem miner/Images/Animations/Explosion","explosion")

breaking = create_animation(filepath+"Gem miner/Images/Animations/Smoke","smoke")

brickplace = create_animation(filepath+"Gem miner/Images/Animations/Bricks/Placing","brickplace")

brickbreaking = create_animation(filepath+"Gem miner/Images/Animations/Bricks/Breaking","brickbreak")

time_bgs = create_animation(filepath+"Gem miner/Images/Backgrounds/Time","time_bg")

bomb_create = create_animation(filepath+"Gem miner/Images/Animations/Bombs","bomb")

hgembreaks = {}
for ani in ["Red","Yellow"]:
    hgembreaks[ani.lower()] = {"center":create_animation(filepath+f"Gem miner/Images/Animations/Gems/Horizontal/{ani}/Center",ani.lower()),
                                "left":create_animation(filepath+f"Gem miner/Images/Animations/Gems/Horizontal/{ani}/Left",ani.lower()),
                                "right":create_animation(filepath+f"Gem miner/Images/Animations/Gems/Horizontal/{ani}/Right",ani.lower())}

vgembreaks = {}
for ani in ["Red","Yellow"]:
    vgembreaks[ani.lower()] = {"center":create_animation(filepath+f"Gem miner/Images/Animations/Gems/Vertical/{ani}/Center",ani.lower()),
                                "bottom":create_animation(filepath+f"Gem miner/Images/Animations/Gems/Vertical/{ani}/Bottom",ani.lower()),
                                "top":create_animation(filepath+f"Gem miner/Images/Animations/Gems/Vertical/{ani}/Top",ani.lower())}

gemvanish = create_animation(filepath+f"Gem miner/Images/Animations/Gems/Vanish","vanish")

vdiamonds = {}
hdiamonds = {}
for ani in ["Red","Green","Yellow","Blue"]:
    vdiamonds[ani.lower()] = [PhotoImage(file = filepath+f"Gem miner/Images/Animations/Diamonds/Vertical/{ani}/frame{i}.png") for i in range(1,10)]
    hdiamonds[ani.lower()] = [PhotoImage(file = filepath+f"Gem miner/Images/Animations/Diamonds/Horizontal/{ani}/frame{i}.png") for i in range(1,10)]

obstacle_bg = PhotoImage(file = filepath+"Gem miner/Images/Backgrounds/obstacle_bg.png")
survival_bg = PhotoImage(file = filepath+"Gem miner/Images/Backgrounds/survival_bg.png")
chroma_bg = PhotoImage(file = filepath+"Gem miner/Images/Backgrounds/chroma_bg.png")
diceused = [PhotoImage(file = filepath+"Gem miner/Images/Animations/Dice/dice1.png")]

cross = PhotoImage(file = filepath+"Gem miner/Images/UI/cross.png")