from tkinter import PhotoImage
from pathlib import Path
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