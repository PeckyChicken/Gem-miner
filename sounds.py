from pygame import init, mixer
from tkinter import Tk

mixer.pre_init(48000, -16, 1, 512)
init()
mixer.init()
mixer.set_num_channels(32)

filepath = __file__+"/../"

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
bombcreated = mixer.Sound(filepath+"Gem miner/Sounds/Bomb/bombcreated.wav")
explosion = mixer.Sound(filepath+"Gem miner/Sounds/Bomb/boom.wav")
remove = mixer.Sound(filepath+"Gem miner/Sounds/Gameplay/break.wav")
brickbreak = mixer.Sound(filepath+"Gem miner/Sounds/Gameplay/brick_break.wav")
clearall = mixer.Sound(filepath+"Gem miner/Sounds/Diamond/clearall.wav")
diamondcreated = mixer.Sound(filepath+"Gem miner/Sounds/Diamond/diamondcreated.wav")
diamondused = mixer.Sound(filepath+"Gem miner/Sounds/Diamond/diamondused.wav")
drillcreated = mixer.Sound(filepath+"Gem miner/Sounds/Drill/drillcreated.wav")
drillused = mixer.Sound(filepath+"Gem miner/Sounds/Drill/drillused.wav")

jackhammerused = mixer.Sound(filepath+"Gem miner/Sounds/Tools/jackhammerused.wav")
nomatch = mixer.Sound(filepath+"Gem miner/Sounds/Gameplay/nomatch.wav")
pickused = mixer.Sound(filepath+"Gem miner/Sounds/Tools/pickaxeused.wav")
placed = mixer.Sound(filepath+"Gem miner/Sounds/Gameplay/place.wav")
toolselected = mixer.Sound(filepath+"Gem miner/Sounds/Tools/toolselected.wav")
shufflesound = mixer.Sound(filepath+"Gem miner/Sounds/Tools/shuffleused.wav")
axeused = mixer.Sound(filepath+"Gem miner/Sounds/Tools/axeused.wav")
starused = mixer.Sound(filepath+"Gem miner/Sounds/Tools/starused.wav")
bucketused = mixer.Sound(filepath+"Gem miner/Sounds/Tools/bucketused.wav")
title1 = mixer.Sound(filepath+"Gem miner/Music/title1.ogg")
title2 = mixer.Sound(filepath+"Gem miner/Music/title2.ogg")
title3 = mixer.Sound(filepath+"Gem miner/Music/title3.ogg")
mode_select = mixer.Sound(filepath+"Gem miner/Music/mode_select.ogg")
main1 = mixer.Sound(filepath+"Gem miner/Music/main.ogg")
main2 = mixer.Sound(filepath+"Gem miner/Music/main2.ogg")
time1 = mixer.Sound(filepath+"Gem miner/Music/time1.ogg")
time2 = mixer.Sound(filepath+"Gem miner/Music/time2.ogg")
time3 = mixer.Sound(filepath+"Gem miner/Music/time3.ogg")
time4 = mixer.Sound(filepath+"Gem miner/Music/time4.ogg")
advance = mixer.Sound(filepath+"Gem miner/Sounds/Gameplay/nextlevel.wav")
newhighscore = mixer.Sound(filepath+"Gem miner/Sounds/Gameplay/highscore.wav")
gameover1 = mixer.Sound(filepath+"Gem miner/Music/gameover1.ogg")
gameover2 = mixer.Sound(filepath+"Gem miner/Music/gameover2.ogg")
obstacle = mixer.Sound(filepath+"Gem miner/Music/obstacle.ogg")
chromablitz = mixer.Sound(filepath+"Gem miner/Music/chromablitz.ogg")
clicked = mixer.Sound(filepath+"Gem miner/Sounds/Gameplay/click.wav")
clocktick = mixer.Sound(filepath+"Gem miner/Sounds/Gameplay/clocktick.wav")
brickplaced = mixer.Sound(filepath+"Gem miner/Sounds/Gameplay/brick_placed.wav")
specialadvance = mixer.Sound(filepath+"Gem miner/Sounds/Gameplay/you_know_not_what_this_is.wav")
startsound = mixer.Sound(filepath+"Gem miner/Sounds/Gameplay/start.wav")
warning = mixer.Sound(filepath+"Gem miner/Sounds/Gameplay/warning.wav")

#Sets the volume of the music
music_vol = 0.25
mixer.Sound.set_volume(title1,music_vol)
mixer.Sound.set_volume(title2,music_vol)
mixer.Sound.set_volume(title3,music_vol)
mixer.Sound.set_volume(main1,music_vol)
mixer.Sound.set_volume(main2,music_vol)
mixer.Sound.set_volume(time1,music_vol)
mixer.Sound.set_volume(time2,music_vol)
mixer.Sound.set_volume(time3,music_vol)
mixer.Sound.set_volume(time4,music_vol)
mixer.Sound.set_volume(obstacle,music_vol*1.5)
mixer.Sound.set_volume(gameover1,music_vol)
mixer.Sound.set_volume(gameover2,music_vol)
mixer.Sound.set_volume(mode_select,music_vol)
mixer.Sound.set_volume(chromablitz,music_vol)

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

def stop_music(window):
    global repeats, channels
    for channel in channels:
        channel.stop()
    channels.clear()
    errors = 0
    try:
        window.after_cancel(loop2)
    except NameError: 
        errors += 1
    #if errors != 1:
        #print(f"LOG: Error found in function stop_music(), the number of errors were:\n{errors}.\nExpected:\n0.")
    repeats = 0
