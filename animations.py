from pathlib import Path
from typing import List, Callable
from tkinter import NORMAL, Canvas, PhotoImage, Tk

from constants import SQUARELEN

class CreateAnimation:
    def __init__(self, path: str, name: str, filetype: str = "png"):
        self.index = 0
        """
        This function creates a list of animation frames, from just giving the file path and the name of the file.
        The program will automatically determine how many frames there are, as long as they are named in the style <title>1, <title>2, <title>3, and so on
        """
        # Get a list of all the files in the given path that match the given name and filetype
        files = Path(path).glob(f"{name}*.{filetype}")
        
        # Sort the list of files in alphabetical order
        files = sorted(files)
        
        # Initialize a list to store the animation frames
        frames: List[PhotoImage] = []
        
        # Loop through the list of files and add each file as a PhotoImage to the list of frames
        for frame in files:
            frames.append(PhotoImage(file=f"{frame}"))
        
        # Put the values in
        self.values = frames
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index >= len(self.values):
            raise StopIteration
        result = self.values[self.index]
        self.index += 1
        return result


def draw_animation(x, y, frames: CreateAnimation, fps, c: Canvas, get_pos: Callable, window: Tk, frame=0, sprite=None, event: Callable = None, direct=False):
    """
    Draws an animation at a given grid position. X and Y are the grid position of the animation, frames is a list of the frames to play, fps is how fast the animation plays.

    For c, get_pos, and window, just pass those exact words in, for frame and sprite, leave those alone, and event is the function which will be called on animation completing.
    """
    frame_time = 1000 // fps
    if direct:
        draw_x, draw_y = x - SQUARELEN / 2, y - SQUARELEN / 2
    else:
        draw_x, draw_y = get_pos(x, y)
    if sprite is None:
        sprite = c.create_image(draw_x + SQUARELEN / 2, draw_y + SQUARELEN / 2, image=frames.values[frame])
    else:
        c.itemconfig(sprite, image=frames.values[frame])
    c.itemconfig(sprite, state=NORMAL, image=frames.values[frame])
    frame += 1
    if frame < len(frames.values):
        window.after(frame_time, draw_animation, x, y, frames, fps, c, get_pos, window, frame, sprite, event, direct)
    else:
        if event is not None:
            event()
        c.delete(sprite)
