from pathlib import Path
from typing import List, Callable
from tkinter import NORMAL, Canvas, PhotoImage, Tk

from constants import SQUARELEN


def create_animation(path: str, name: str, filetype: str = "png") -> List[PhotoImage]:
    """
    This function creates a list of animation frames, from just giving the file path and the name of the file.
    The program will automatically determine how many frames there are, as long as they are named in the style <title>1, <title>2, <title>3, and so on
    """
    files = Path(path).glob(f"{name}*.{filetype}")
    files = sorted(files)
    frames: List[PhotoImage] = []
    for frame in files:
        frames.append(PhotoImage(file=f"{frame}"))
    return frames

def draw_animation(x, y, frames, fps, c: Canvas, get_pos: Callable, window: Tk, frame=0, sprite=None, event: Callable = None, direct=False):
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
        sprite = c.create_image(draw_x + SQUARELEN / 2, draw_y + SQUARELEN / 2, image=frames[frame])
    else:
        c.itemconfig(sprite, image=frames[frame])
    c.itemconfig(sprite, state=NORMAL, image=frames[frame])
    frame += 1
    if frame < len(frames):
        window.after(frame_time, draw_animation, x, y, frames, fps, c, get_pos, window, frame, sprite, event, direct)
    else:
        if event is not None:
            event()
        c.delete(sprite)
