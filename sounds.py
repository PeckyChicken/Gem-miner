from pygame import mixer, init

mixer.pre_init(48000, -16, 1, 512)
init()
mixer.init()
mixer.set_num_channels(16)

filepath = __file__+"/../"

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
powerupselected = mixer.Sound(filepath+"Gem miner/Sounds/Tools/powerupselected.wav")
shufflesound = mixer.Sound(filepath+"Gem miner/Sounds/Tools/shuffleused.wav")
axeused = mixer.Sound(filepath+"Gem miner/Sounds/Tools/axeused.wav")
starused = mixer.Sound(filepath+"Gem miner/Sounds/Tools/starused.wav")
title1 = mixer.Sound(filepath+"Gem miner/Music/title1.ogg")
title2 = mixer.Sound(filepath+"Gem miner/Music/title2.ogg")
mode_select = mixer.Sound(filepath+"Gem miner/Music/mode_select.ogg")
main1 = mixer.Sound(filepath+"Gem miner/Music/main.ogg")
main2 = mixer.Sound(filepath+"Gem miner/Music/main2.ogg")
time1 = mixer.Sound(filepath+"Gem miner/Music/time1.ogg")
time2 = mixer.Sound(filepath+"Gem miner/Music/time2.ogg")
advance = mixer.Sound(filepath+"Gem miner/Sounds/Gameplay/nextlevel.wav")
gameover1 = mixer.Sound(filepath+"Gem miner/Music/gameover1.ogg")
gameover2 = mixer.Sound(filepath+"Gem miner/Music/gameover2.ogg")
obstacle = mixer.Sound(filepath+"Gem miner/Music/obstacle.ogg")
chromablitz = mixer.Sound(filepath+"Gem miner/Music/chromablitz.ogg")
clicked = mixer.Sound(filepath+"Gem miner/Sounds/Gameplay/click.wav")
clocktick = mixer.Sound(filepath+"Gem miner/Sounds/Gameplay/clocktick.wav")
brickplaced = mixer.Sound(filepath+"Gem miner/Sounds/Gameplay/brick_placed.wav")
specialadvance = mixer.Sound(filepath+"Gem miner/Sounds/Gameplay/you_know_not_what_this_is.wav")
startsound = mixer.Sound(filepath+"Gem miner/Sounds/Gameplay/start.wav")

#Sets the volume of the music
music_vol = 0.25
mixer.Sound.set_volume(title1,music_vol)
mixer.Sound.set_volume(title2,music_vol)
mixer.Sound.set_volume(main1,music_vol)
mixer.Sound.set_volume(main2,music_vol)
mixer.Sound.set_volume(time1,music_vol)
mixer.Sound.set_volume(time2,music_vol)
mixer.Sound.set_volume(obstacle,music_vol)
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
mixer.Sound.set_volume(powerupselected,sound_vol)
mixer.Sound.set_volume(shufflesound,sound_vol)
mixer.Sound.set_volume(axeused,sound_vol)
mixer.Sound.set_volume(starused,sound_vol)
mixer.Sound.set_volume(advance,sound_vol)
mixer.Sound.set_volume(specialadvance,sound_vol)
mixer.Sound.set_volume(clicked,sound_vol)
mixer.Sound.set_volume(clocktick,sound_vol)
mixer.Sound.set_volume(brickplaced,sound_vol)
mixer.Sound.set_volume(startsound,sound_vol)

def play_sound_effect(sfx_on,effect):
    if sfx_on:
        try:
            mixer.find_channel().play(effect)
        except AttributeError:
            mixer.Channel(20).play(effect)

channels: set[mixer.Channel] = set()
def get_channel() -> mixer.Channel:
    global channels
    channel = mixer.find_channel(True)
    channels.add(channel)
    return channel

repeats = 0
def title_music(window):
    global repeats, loop
    if repeats == 0:
        get_channel().play(title1)
        loop = window.after(13300,title_music,window)
    else:
        get_channel().play(title2)
        loop = window.after(54850,title_music,window)
    repeats += 1

def select_music(window):
    global repeats,loop2
    get_channel().play(mode_select)
    loop2 = window.after(69818,select_music,window)
    repeats += 1

def game_music(window):
    global repeats,loop2
    get_channel().play(main1)
    loop2 = window.after(52377,game_music,window)
    repeats += 1

def game_music2(window):
    global repeats,loop2
    get_channel().play(main2)
    loop2 = window.after(61075,game_music2,window)
    repeats += 1

def time_music(window):
    global repeats, loop
    if repeats == 0:
        get_channel().play(time1)
        loop = window.after(8000,time_music,window)
    else:
        get_channel().play(time2)
        loop = window.after(32000,time_music,window)
    repeats += 1


def obstacle_music(window):
    global repeats,loop2
    get_channel().play(obstacle)
    loop2 = window.after(56000,obstacle_music,window)
    repeats += 1
    
def game_over_music(window):
    global repeats, loop2
    if repeats == 0:
        get_channel().play(gameover1)
        loop2 = window.after(643,game_over_music,window)
    else: 
        get_channel().play(gameover2)
        loop2 = window.after(13714,game_over_music,window)
    repeats += 1

def chroma_music(window):
    global repeats,loop2
    get_channel().play(chromablitz)
    loop2 = window.after(57600,chroma_music,window)
    repeats += 1

def stop_music(window):
    global repeats, channels
    for channel in channels:
        channel.stop()
    channels.clear()
    errors = 0 #Should just be one of these
    try:
        window.after_cancel(loop)
    except NameError: 
        errors += 1
    try:
        window.after_cancel(loop2)
    except NameError: 
        errors += 1
    if errors != 1:
        #print(f"LOG: Error found in function stop_music(), the number of errors were:\n{errors}.\nExpected:\n1.")
        pass
    repeats = 0
