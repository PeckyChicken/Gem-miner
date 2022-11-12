from pathlib import Path
from time import sleep
from tkinter import NORMAL, Canvas, PhotoImage, Tk

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

#! Depricated function
def draw_old_animation(x,y,frames,fps,c: Canvas,get_pos: callable,window: Tk):
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

def draw_animation(x,y,frames,fps,c: Canvas,get_pos:callable,window: Tk,frame=0,sprite=None):
    frametime = 1000//fps
    DrawX, DrawY = get_pos(x,y)
    if sprite is None:
        sprite = c.create_image(DrawX+SQUARELEN/2,DrawY+SQUARELEN/2,image=frames[frame])
    else:
        c.itemconfig(sprite,image=frames[frame])
    c.itemconfig(sprite,state=NORMAL,image=frames[frame])
    #print(f"FPS is {fps}, frame time is {frametime/1000}, waiting {frametime} ms before next frame, current frame number is {frame}")
    frame += 1
    window.update()
    if frame < len(frames):

        window.after(frametime,draw_animation,x,y,frames,fps,c,get_pos,window,frame,sprite)
    else:
        c.delete(sprite)