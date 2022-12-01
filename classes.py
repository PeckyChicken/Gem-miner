from tkinter import HIDDEN, NORMAL, Canvas

from constants import *
from functions import *
from images import *
from animations import *




class GameButton:
    def __init__(self,text:str,offset:float,c:Canvas,get_pos:callable,window:Tk,hide:bool=False):
        self.image = c.create_image(WIDTH/2,HEIGHT/2+offset,image=button,state=[NORMAL,HIDDEN][hide])
        self.text = c.create_text(WIDTH/2,HEIGHT/2+offset,text=text,font=(FONT,25),fill="white",state=[NORMAL,HIDDEN][hide])
        self.bounds = (WIDTH/2-100,
                       HEIGHT/2+offset-50/2,
                       WIDTH/2+100,
                       HEIGHT/2+offset+50/2)
        self.offset = offset
        self.visible = not hide
        self.canvas = c
        self.get_pos = get_pos
        self.window = window

    def is_clicked(self,mousex:float,mousey:float) -> bool:
        if not self.visible:
            return False
        x1,y1,x2,y2 = self.bounds
        clicked = inside(x1,y1,x2,y2,mousex, mousey)
        if clicked:
            draw_animation(WIDTH/2,HEIGHT/2+self.offset,buttonclick,100,self.canvas,self.get_pos,self.window,direct=True)
        return clicked

    def set_visible(self,visible:bool):
        self.visible = visible
        self.canvas.itemconfig(self.image,state=[HIDDEN,NORMAL][visible])
        self.canvas.itemconfig(self.text,state=[HIDDEN,NORMAL][visible])