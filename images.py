from tkinter import PhotoImage, Tk

from animations import CreateAnimation

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

bricks = PhotoImage(file = filepath+"Gem miner/Images/Bricks/bricks.png")
redbricks = PhotoImage(file = filepath+"Gem miner/Images/Bricks/red_bricks.png")
yellowbricks = PhotoImage(file = filepath+"Gem miner/Images/Bricks/yellow_bricks.png")
greenbricks = PhotoImage(file = filepath+"Gem miner/Images/Bricks/green_bricks.png")
bluebricks = PhotoImage(file = filepath+"Gem miner/Images/Bricks/blue_bricks.png")

jackhammer_img = PhotoImage(file = filepath+"Gem miner/Images/Tools/jackhammer.png")
pickaxe_img = PhotoImage(file = filepath+"Gem miner/Images/Tools/pickaxe.png")
axe_img = PhotoImage(file = filepath+"Gem miner/Images/Tools/axe.png")
bucket_img = PhotoImage(file = filepath+"Gem miner/Images/Tools/bucket.png")
star_img = PhotoImage(file = filepath+"Gem miner/Images/Tools/star.png")
wand_img = PhotoImage(file = filepath+"Gem miner/Images/Tools/wand.png")
dice_img = PhotoImage(file = filepath+"Gem miner/Images/Tools/shuffle.png")

backbutton = PhotoImage(file = filepath+"Gem miner/Images/UI/backbutton.png")
button = PhotoImage(file = filepath+"Gem miner/Images/UI/button.png")
titlebgimage = PhotoImage(file = filepath+"Gem miner/Images/Backgrounds/titlebg.png")

tut1,tut2,tut3,tut4,tut5,tut6 = CreateAnimation(filepath+"Gem miner/Images/Tutorial","tutorial")



music = PhotoImage(file = filepath+"Gem miner/Images/UI/music_yes.png")
sfx = PhotoImage(file = filepath+"Gem miner/Images/UI/sfx_yes.png")
nomusic = PhotoImage(file = filepath+"Gem miner/Images/UI/music_no.png")
nosfx = PhotoImage(file = filepath+"Gem miner/Images/UI/sfx_no.png")

obstaclecard = PhotoImage(file = filepath+"Gem miner/Images/UI/obstacles_card.png")
survivalcard = PhotoImage(file = filepath+"Gem miner/Images/UI/survival_card.png")
timecard = PhotoImage(file = filepath+"Gem miner/Images/UI/time_card.png")
chromacard = PhotoImage(file = filepath+"Gem miner/Images/UI/chroma_card.png")
fade_image = PhotoImage(file = filepath+"Gem miner/Images/UI/fade.png")

tool_bg = PhotoImage(file = filepath+"Gem miner/Images/UI/tools_bg.png")

colorselection = PhotoImage(file = filepath+"Gem miner/Images/UI/colorselection.png")

explosions = CreateAnimation(filepath+"Gem miner/Images/Animations/Explosion","explosion")

smokes = []
for color in ["General","Red","Yellow","Green","Blue"]:
    smokes.append(CreateAnimation(filepath+f"Gem miner/Images/Animations/Smoke/{color}","smoke"))

transition = CreateAnimation(path="Gem miner/Images/Animations/Transitions/Enter",name="Frame",filetype="PNG")

brickplace = CreateAnimation(filepath+"Gem miner/Images/Animations/Bricks/Placing","brickplace")

brickbreaking = CreateAnimation(filepath+"Gem miner/Images/Animations/Bricks/Breaking","brickbreak")
brickin = CreateAnimation(filepath+"Gem miner/Images/Animations/Bricks/Changing/In","dice")
brickout = CreateAnimation(filepath+"Gem miner/Images/Animations/Bricks/Changing/Out","dice")

bomb_create = CreateAnimation(filepath+"Gem miner/Images/Animations/Bombs","bomb")




hgembreaks = {}
for ani in ["Red","Yellow","Green","Blue"]:
    hgembreaks[ani.lower()] = {"center":CreateAnimation(filepath+f"Gem miner/Images/Animations/Gems/Horizontal/{ani}/Center",ani.lower()),
                                "left":CreateAnimation(filepath+f"Gem miner/Images/Animations/Gems/Horizontal/{ani}/Left",ani.lower()),
                                "right":CreateAnimation(filepath+f"Gem miner/Images/Animations/Gems/Horizontal/{ani}/Right",ani.lower())}

vgembreaks = {}
for ani in ["Red","Yellow","Green","Blue"]:
    vgembreaks[ani.lower()] = {"center":CreateAnimation(filepath+f"Gem miner/Images/Animations/Gems/Vertical/{ani}/Center",ani.lower()),
                                "bottom":CreateAnimation(filepath+f"Gem miner/Images/Animations/Gems/Vertical/{ani}/Bottom",ani.lower()),
                                "top":CreateAnimation(filepath+f"Gem miner/Images/Animations/Gems/Vertical/{ani}/Top",ani.lower())}

gemvanish = CreateAnimation(filepath+f"Gem miner/Images/Animations/Gems/Vanish","vanish")

vdiamonds = {}
hdiamonds = {}
for ani in ["Red","Green","Yellow","Blue"]:
    vdiamonds[ani.lower()] = CreateAnimation(f"Gem miner/Images/Animations/Diamonds/Vertical/{ani}","frame")
    hdiamonds[ani.lower()] = CreateAnimation(f"Gem miner/Images/Animations/Diamonds/Horizontal/{ani}","frame")


hdrills = {}
for ani in ["Red","Yellow","Green","Blue"]:
    hdrills[ani.lower()] = {"left":CreateAnimation(filepath+f"Gem miner/Images/Animations/Drills/Horizontal/{ani}/Left",ani.lower()),
                            "right":CreateAnimation(filepath+f"Gem miner/Images/Animations/Drills/Horizontal/{ani}/Right",ani.lower())}

vdrills = {}
for ani in ["Red","Yellow","Green","Blue"]:
    vdrills[ani.lower()] = {"top":CreateAnimation(filepath+f"Gem miner/Images/Animations/Drills/Vertical/{ani}/Top",ani.lower()),
                            "bottom":CreateAnimation(filepath+f"Gem miner/Images/Animations/Drills/Vertical/{ani}/Bottom",ani.lower())}

obstacle_bg = PhotoImage(file = filepath+"Gem miner/Images/Backgrounds/obstacle_bg.png")
survival_bg = PhotoImage(file = filepath+"Gem miner/Images/Backgrounds/survival_bg.png")
chroma_bg = PhotoImage(file = filepath+"Gem miner/Images/Backgrounds/chroma_bg.png")
time_bg = PhotoImage(file=filepath+"Gem miner/Images/Backgrounds/time_bg.png")

diceused = CreateAnimation("Gem miner/Images/Animations/Dice","dice")

cross = PhotoImage(file = filepath+"Gem miner/Images/UI/cross.png")
careful = PhotoImage(file = filepath+"Gem miner/Images/UI/warning.png")
air = PhotoImage(file = filepath+"Gem miner/Images/UI/air.png")