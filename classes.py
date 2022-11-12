from tkinter import HIDDEN, NORMAL, Canvas

from constants import *
from functions import *
from images import *




class GameButton:
    def __init__(self,text:str,offset:float,c:Canvas,hide:bool=False):
        self.image = c.create_image(WIDTH/2,HEIGHT/2+offset,image=button,state=[NORMAL,HIDDEN][hide])
        self.text = c.create_text(WIDTH/2,HEIGHT/2+offset,text=text,font=(FONT,25),fill="white",state=[NORMAL,HIDDEN][hide])
        self.bounds = (WIDTH/2-100,
                       HEIGHT/2+offset-50/2,
                       WIDTH/2+100,
                       HEIGHT/2+offset+50/2)
        self.offset = offset
        self.visible = not hide
        self.canvas = c

    def is_clicked(self,mousex:float,mousey:float) -> bool:
        if not self.visible:
            return False
        x1,y1,x2,y2 = self.bounds
        return inside(x1,y1,x2,y2,mousex, mousey)

    def set_visible(self,visible:bool):
        self.visible = visible
        self.canvas.itemconfig(self.image,state=[HIDDEN,NORMAL][visible])
        self.canvas.itemconfig(self.text,state=[HIDDEN,NORMAL][visible])