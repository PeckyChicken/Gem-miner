from tkinter import PhotoImage, Canvas, NORMAL, Tk
from pathlib import Path
from time import sleep
from constants import *
def create_animation(path: str,name: str) -> list[PhotoImage]:
    '''This function creates a list of animation frames, from just giving the file path and the name of the file.
    The program will automatically determine how many frames there are, as long as they are named in the style <title>1, <title>2, <title>3, and so on
    '''
    files = Path(path).glob(f"{name}*.png")
    files = sorted(files)
    framelist: list[PhotoImage] = []
    for frame in files:
        framelist.append(PhotoImage(file=f"{frame}"))
    return framelist

def draw_animation(x,y,frames,fps,c: Canvas,get_pos: callable,window: Tk):
    frametime = 1/fps
    DrawX, DrawY = get_pos(x,y)
    DrawX += SQUARELEN/2
    DrawY += SQUARELEN/2
    sprite = c.create_image(DrawX,DrawY,image=frames[0])
    frame = 0
    while frame < len(frames):
        c.itemconfig(sprite,state=NORMAL,image=frames[frame])
        frame += 1
        sleep(frametime)
        window.update()
    c.delete(sprite)