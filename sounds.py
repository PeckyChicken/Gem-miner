import glob
import os
from tkinter import Tk

from pygame import init, mixer

mixer.pre_init(48000, -16, 1, 512)
init()
mixer.init()
mixer.set_num_channels(32)

filepath = __file__+"/../"
with open(f"{filepath}/folder_name.txt") as f:
    folder_name = f.read()


class Music:
    def __init__(self,music: dict,window:Tk):
        '''Creates a music object which you can play at any time. 
        You can pass up to 2 songs as the keys in a dictionary, with the values being how long the songs last, (In ms).'''
        if len(music) == 1:
            self.music = [(list(music.keys())[0],list(music.values())[0])]
            self.repeats = 0
            self.window = window
        elif len(music) == 2:
            self.music = [(list(music.keys())[0],list(music.values())[0]),(list(music.keys())[1],list(music.values())[1])]
            self.repeats = 0
            self.window = window
        else:
            raise TypeError(f"Expected dict with 2 values, got {len(music)}")
    def play(self):
        self.repeats = 0
        self.play_song()
    def play_song(self):
        global loop2
        self.repeats += 1
        if len(self.music) == 1:
            get_channel().play(self.music[0][0])
            loop2 = self.window.after(self.music[0][1],self.play_song)
        elif len(self.music) == 2:
            if self.repeats == 1:
                get_channel().play(self.music[0][0])
                loop2 = self.window.after(self.music[0][1],self.play_song)
            else:
                get_channel().play(self.music[1][0])
                loop2 = self.window.after(self.music[1][1],self.play_song)   

#Importing the sounds
def get_sounds(folder):
    sounds = {os.path.basename(file).split(".")[0]:mixer.Sound(file) for file in glob.glob(f'{filepath}/{folder_name}/Sounds/{folder}/**/*.wav', recursive=True)}
    return sounds

def get_music():
    music = {os.path.basename(file).split(".")[0]:mixer.Sound(file) for file in glob.glob(f'{filepath}/{folder_name}/Music/**/*.ogg', recursive=True)}
    return music

sounds = get_sounds(".")
music = get_music()


#Sets the volume of the music
music_vol = 0.25
for song in music.values():
    song.set_volume(music_vol)

#Sets the volume of the sound effects
sound_vol = 0.5
for sound in sounds.values():
    sound.set_volume(music_vol)

soundchannels: list[mixer.Channel] = []
def play_sound_effect(sfx_on,effect):
    global soundchannels
    if sfx_on:
        try:
            channel = mixer.find_channel()
            soundchannels.append(channel)
            channel.play(effect)
        except AttributeError:
            mixer.Channel(20).play(effect)

channels: set[mixer.Channel] = set()
def get_channel() -> mixer.Channel:
    global channels
    channel = mixer.find_channel(True)
    channels.add(channel)
    return channel
repeats = 0

def stop_sounds():
    global soundchannels
    for channel in soundchannels:
        try:
            channel.stop()
        except AttributeError:
            pass
    soundchannels.clear()

def stop_music(window: Tk,mute=False):
    global repeats, channels
    for channel in channels:
        if mute:
            channel.set_volume(0)
        else:
            channel.stop()
            soundchannels.clear()
            try:
                window.after_cancel(loop2)
            except Exception:
                pass
    errors = 0
