from tkinter import PhotoImage, Tk
import os
import glob
from animations import CreateAnimation

window = Tk() #sets up window
filepath = __file__+"/../"
with open(os.path.join(filepath,"folder_name.txt")) as f:
    folder_name = f.read()

def get_images(folder):
    images = {os.path.basename(file).split(".")[0]:PhotoImage(file=file) for file in glob.glob(f'{filepath}/{folder_name}/Images/{folder}/**/*.png', recursive=True)}
    return images


gems = get_images("Gems")
bricks = get_images("Bricks")
tool_images = get_images("Tools")
UI = get_images("UI")
backgrounds = get_images("Backgrounds")



tut1,tut2,tut3,tut4,tut5,tut6 = CreateAnimation(filepath+f"{folder_name}/Images/Tutorial","tutorial")


explosions = CreateAnimation(filepath+f"{folder_name}/Images/Animations/Explosion","explosion")

smokes = []
for color in ["General","Red","Yellow","Green","Blue"]:
    smokes.append(CreateAnimation(filepath+f"{folder_name}/Images/Animations/Smoke/{color}","smoke"))

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

diceused = CreateAnimation(f"{folder_name}/Images/Animations/Dice","dice")
