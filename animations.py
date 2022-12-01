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

def draw_animation(x,y,frames,fps,c: Canvas,get_pos:callable,window: Tk,frame=0,sprite=None,event:callable=None,direct=False):
    '''Draws an animation at a given grid position. X and Y are the grid position of the animation, frames is a list of the frames to play, fps is how fast the animation plays.
    
    For c, get_pos, and window, just pass those exact words in, for frame and sprite, leave those alone, and event is the function which will be called on animation completing.'''
    frametime = 1000//fps
    if direct:
        DrawX, DrawY = x,y
    else:
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

        window.after(frametime,draw_animation,x,y,frames,fps,c,get_pos,window,frame,sprite,event)
    else:
        if event is not None:
            event()
        c.delete(sprite)