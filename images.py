from tkinter import PhotoImage, Tk

from animations import CreateAnimation

window = Tk() #sets up window
filepath = __file__+"/../"
with open(f"{filepath}/folder_name.txt") as f:
    folder_name = f.read()

red_block = PhotoImage(file = filepath+f"{folder_name}/Images/Gems/red_gem.png")
yellow_block = PhotoImage(file = filepath+f"{folder_name}/Images/Gems/yellow_gem.png")
green_block = PhotoImage(file = filepath+f"{folder_name}/Images/Gems/green_gem.png")
blue_block = PhotoImage(file = filepath+f"{folder_name}/Images/Gems/blue_gem.png")
empty_block = PhotoImage(file = filepath+f"{folder_name}/Images/UI/empty.png")

vdrill = PhotoImage(file = filepath+f"{folder_name}/Images/Tools/rocket_vertical.png")
hdrill = PhotoImage(file = filepath+f"{folder_name}/Images/Tools/rocket_horizontal.png")
red_diamond = PhotoImage(file = filepath+f"{folder_name}/Images/Tools/Diamonds/red_diamond.png")
yellow_diamond = PhotoImage(file = filepath+f"{folder_name}/Images/Tools/Diamonds/yellow_diamond.png")
green_diamond = PhotoImage(file = filepath+f"{folder_name}/Images/Tools/Diamonds/green_diamond.png")
blue_diamond = PhotoImage(file = filepath+f"{folder_name}/Images/Tools/Diamonds/blue_diamond.png")
rainbow_diamond = PhotoImage(file = filepath+f"{folder_name}/Images/Tools/Diamonds/rainbow_diamond.png")
bomb = PhotoImage(file = filepath+f"{folder_name}/Images/Tools/bomb.png")

bricks = PhotoImage(file = filepath+f"{folder_name}/Images/Bricks/bricks.png")
redbricks = PhotoImage(file = filepath+f"{folder_name}/Images/Bricks/red_bricks.png")
yellowbricks = PhotoImage(file = filepath+f"{folder_name}/Images/Bricks/yellow_bricks.png")
greenbricks = PhotoImage(file = filepath+f"{folder_name}/Images/Bricks/green_bricks.png")
bluebricks = PhotoImage(file = filepath+f"{folder_name}/Images/Bricks/blue_bricks.png")

jackhammer_img = PhotoImage(file = filepath+f"{folder_name}/Images/Tools/jackhammer.png")
pickaxe_img = PhotoImage(file = filepath+f"{folder_name}/Images/Tools/pickaxe.png")
axe_img = PhotoImage(file = filepath+f"{folder_name}/Images/Tools/axe.png")
bucket_img = PhotoImage(file = filepath+f"{folder_name}/Images/Tools/bucket.png")
star_img = PhotoImage(file = filepath+f"{folder_name}/Images/Tools/star.png")
wand_img = PhotoImage(file = filepath+f"{folder_name}/Images/Tools/wand.png")
dice_img = PhotoImage(file = filepath+f"{folder_name}/Images/Tools/dice.png")

backbutton = PhotoImage(file = filepath+f"{folder_name}/Images/UI/backbutton.png")
button = PhotoImage(file = filepath+f"{folder_name}/Images/UI/button.png")
titlebgimage = PhotoImage(file = filepath+f"{folder_name}/Images/Backgrounds/titlebg.png")

tut1,tut2,tut3,tut4,tut5,tut6 = CreateAnimation(filepath+f"{folder_name}/Images/Tutorial","tutorial")



music = PhotoImage(file = filepath+f"{folder_name}/Images/UI/music_yes.png")
sfx = PhotoImage(file = filepath+f"{folder_name}/Images/UI/sfx_yes.png")
nomusic = PhotoImage(file = filepath+f"{folder_name}/Images/UI/music_no.png")
nosfx = PhotoImage(file = filepath+f"{folder_name}/Images/UI/sfx_no.png")

obstaclecard = PhotoImage(file = filepath+f"{folder_name}/Images/UI/obstacles_card.png")
survivalcard = PhotoImage(file = filepath+f"{folder_name}/Images/UI/survival_card.png")
timecard = PhotoImage(file = filepath+f"{folder_name}/Images/UI/time_card.png")
chromacard = PhotoImage(file = filepath+f"{folder_name}/Images/UI/chroma_card.png")
fade_image = PhotoImage(file = filepath+f"{folder_name}/Images/UI/fade.png")

tool_bg = PhotoImage(file = filepath+f"{folder_name}/Images/UI/tools_bg.png")

colorselection = PhotoImage(file = filepath+f"{folder_name}/Images/UI/colorselection.png")

explosions = CreateAnimation(filepath+f"{folder_name}/Images/Animations/Explosion","explosion")

smokes = []
for color in ["General","Red","Yellow","Green","Blue"]:
    smokes.append(CreateAnimation(filepath+f"{folder_name}/Images/Animations/Smoke/{color}","smoke"))

transition = CreateAnimation(path=f"{folder_name}/Images/Animations/Transitions/Enter",name="Frame",filetype="PNG")

brickplace = CreateAnimation(filepath+f"{folder_name}/Images/Animations/Bricks/Placing","brickplace")

brickbreaking = CreateAnimation(filepath+f"{folder_name}/Images/Animations/Bricks/Breaking","brickbreak")
brickin = CreateAnimation(filepath+f"{folder_name}/Images/Animations/Bricks/Changing/In","dice")
brickout = CreateAnimation(filepath+f"{folder_name}/Images/Animations/Bricks/Changing/Out","dice")

bomb_create = CreateAnimation(filepath+f"{folder_name}/Images/Animations/Bombs","bomb")




hgembreaks = {}
for ani in ["Red","Yellow","Green","Blue"]:
    hgembreaks[ani.lower()] = {"center":CreateAnimation(filepath+f"{folder_name}/Images/Animations/Gems/Horizontal/{ani}/Center",ani.lower()),
                                "left":CreateAnimation(filepath+f"{folder_name}/Images/Animations/Gems/Horizontal/{ani}/Left",ani.lower()),
                                "right":CreateAnimation(filepath+f"{folder_name}/Images/Animations/Gems/Horizontal/{ani}/Right",ani.lower())}

vgembreaks = {}
for ani in ["Red","Yellow","Green","Blue"]:
    vgembreaks[ani.lower()] = {"center":CreateAnimation(filepath+f"{folder_name}/Images/Animations/Gems/Vertical/{ani}/Center",ani.lower()),
                                "bottom":CreateAnimation(filepath+f"{folder_name}/Images/Animations/Gems/Vertical/{ani}/Bottom",ani.lower()),
                                "top":CreateAnimation(filepath+f"{folder_name}/Images/Animations/Gems/Vertical/{ani}/Top",ani.lower())}

gemvanish = CreateAnimation(filepath+f"{folder_name}/Images/Animations/Gems/Vanish","vanish")

vdiamonds = {}
hdiamonds = {}
for ani in ["Red","Green","Yellow","Blue"]:
    vdiamonds[ani.lower()] = CreateAnimation(f"{folder_name}/Images/Animations/Diamonds/Vertical/{ani}","frame")
    hdiamonds[ani.lower()] = CreateAnimation(f"{folder_name}/Images/Animations/Diamonds/Horizontal/{ani}","frame")


hdrills = {}
for ani in ["Red","Yellow","Green","Blue"]:
    hdrills[ani.lower()] = {"left":CreateAnimation(filepath+f"{folder_name}/Images/Animations/Drills/Horizontal/{ani}/Left",ani.lower()),
                            "right":CreateAnimation(filepath+f"{folder_name}/Images/Animations/Drills/Horizontal/{ani}/Right",ani.lower())}

vdrills = {}
for ani in ["Red","Yellow","Green","Blue"]:
    vdrills[ani.lower()] = {"top":CreateAnimation(filepath+f"{folder_name}/Images/Animations/Drills/Vertical/{ani}/Top",ani.lower()),
                            "bottom":CreateAnimation(filepath+f"{folder_name}/Images/Animations/Drills/Vertical/{ani}/Bottom",ani.lower())}

obstacle_bg = PhotoImage(file = filepath+f"{folder_name}/Images/Backgrounds/obstacle_bg.png")
survival_bg = PhotoImage(file = filepath+f"{folder_name}/Images/Backgrounds/survival_bg.png")
chroma_bg = PhotoImage(file = filepath+f"{folder_name}/Images/Backgrounds/chroma_bg.png")
time_bg = PhotoImage(file=filepath+f"{folder_name}/Images/Backgrounds/time_bg.png")

diceused = CreateAnimation(f"{folder_name}/Images/Animations/Dice","dice")

cross = PhotoImage(file = filepath+f"{folder_name}/Images/UI/cross.png")
careful = PhotoImage(file = filepath+f"{folder_name}/Images/UI/warning.png")
air = PhotoImage(file = filepath+f"{folder_name}/Images/UI/air.png")