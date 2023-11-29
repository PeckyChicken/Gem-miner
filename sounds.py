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

bombcreated = mixer.Sound(filepath+f"{folder_name}/Sounds/Bomb/bombcreated.wav")
explosion = mixer.Sound(filepath+f"{folder_name}/Sounds/Bomb/boom.wav")
remove = mixer.Sound(filepath+f"{folder_name}/Sounds/Gameplay/break.wav")
brickbreak = mixer.Sound(filepath+f"{folder_name}/Sounds/Gameplay/brick_break.wav")
clearall = mixer.Sound(filepath+f"{folder_name}/Sounds/Diamond/clearall.wav")
diamondcreated = mixer.Sound(filepath+f"{folder_name}/Sounds/Diamond/diamondcreated.wav")
diamondused = mixer.Sound(filepath+f"{folder_name}/Sounds/Diamond/diamondused.wav")
drillcreated = mixer.Sound(filepath+f"{folder_name}/Sounds/Drill/drillcreated.wav")
drillused = mixer.Sound(filepath+f"{folder_name}/Sounds/Drill/drillused.wav")

jackhammerused = mixer.Sound(filepath+f"{folder_name}/Sounds/Tools/jackhammerused.wav")
nomatch = mixer.Sound(filepath+f"{folder_name}/Sounds/Gameplay/nomatch.wav")
pickused = mixer.Sound(filepath+f"{folder_name}/Sounds/Tools/pickaxeused.wav")
placed = mixer.Sound(filepath+f"{folder_name}/Sounds/Gameplay/place.wav")
toolselected = mixer.Sound(filepath+f"{folder_name}/Sounds/Tools/toolselected.wav")
shufflesound = mixer.Sound(filepath+f"{folder_name}/Sounds/Tools/shuffleused.wav")
axeused = mixer.Sound(filepath+f"{folder_name}/Sounds/Tools/axeused.wav")
starused = mixer.Sound(filepath+f"{folder_name}/Sounds/Tools/starused.wav")
bucketused = mixer.Sound(filepath+f"{folder_name}/Sounds/Tools/bucketused.wav")
advance = mixer.Sound(filepath+f"{folder_name}/Sounds/Gameplay/nextlevel.wav")
newhighscore = mixer.Sound(filepath+f"{folder_name}/Sounds/Gameplay/highscore.wav")
clicked = mixer.Sound(filepath+f"{folder_name}/Sounds/Gameplay/click.wav")
clocktick = mixer.Sound(filepath+f"{folder_name}/Sounds/Gameplay/clocktick.wav")
brickplaced = mixer.Sound(filepath+f"{folder_name}/Sounds/Gameplay/brick_placed.wav")
specialadvance = mixer.Sound(filepath+f"{folder_name}/Sounds/Gameplay/you_know_not_what_this_is.wav")
startsound = mixer.Sound(filepath+f"{folder_name}/Sounds/Gameplay/start.wav")
warning = mixer.Sound(filepath+f"{folder_name}/Sounds/Gameplay/warning.wav")

#Sets the volume of the music
music_vol = 0.25

for song in music.values():
    song.set_volume(music_vol)

#Sets the volume of the sound effects
sound_vol = 0.5
mixer.Sound.set_volume(bombcreated,sound_vol)
mixer.Sound.set_volume(explosion,sound_vol)
mixer.Sound.set_volume(remove,sound_vol)
mixer.Sound.set_volume(brickbreak,sound_vol)
mixer.Sound.set_volume(clearall,sound_vol)
mixer.Sound.set_volume(diamondcreated,sound_vol)
mixer.Sound.set_volume(diamondused,sound_vol)
mixer.Sound.set_volume(drillcreated,sound_vol)
mixer.Sound.set_volume(drillused,sound_vol)
mixer.Sound.set_volume(bombcreated,sound_vol)
mixer.Sound.set_volume(jackhammerused,sound_vol)
mixer.Sound.set_volume(nomatch,sound_vol)
mixer.Sound.set_volume(pickused,sound_vol)
mixer.Sound.set_volume(placed,sound_vol)
mixer.Sound.set_volume(toolselected,sound_vol)
mixer.Sound.set_volume(shufflesound,sound_vol)
mixer.Sound.set_volume(axeused,sound_vol)
mixer.Sound.set_volume(starused,sound_vol)
mixer.Sound.set_volume(advance,sound_vol)
mixer.Sound.set_volume(specialadvance,sound_vol)
mixer.Sound.set_volume(clicked,sound_vol)
mixer.Sound.set_volume(clocktick,sound_vol)
mixer.Sound.set_volume(brickplaced,sound_vol)
mixer.Sound.set_volume(startsound,sound_vol)
mixer.Sound.set_volume(warning,sound_vol)
mixer.Sound.set_volume(newhighscore,sound_vol)
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
