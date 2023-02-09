import os
import time
import tkinter
from tkinter import *
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
import random
from PIL import Image, ImageTk

#window 
root = Tk()
root.title("CyberMusic")
root.geometry("485x700+290+10")
root.configure(background='#333333')
root.resizable(False, False)
mixer.init()


# Create a function to open a file
def AddMusic():
    global mp3_files
    path = filedialog.askdirectory()
    os.chdir(path)
    playlist = os.listdir(path)
    mp3_files = [files for files in playlist if files.endswith(".mp3")]
    for files in mp3_files:
        Playlist.insert(END, files)
        print(files)
        print(mp3_files)

# function to add a music in the playlist
def add_file():
    file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    if file_path:
        file_name = os.path.basename(file_path)
        Playlist.insert(END, file_name)

# function to remove a music in the playlist
def remove_file():
    file_index = Playlist.curselection()
    if file_index:
        Playlist.delete(file_index)




music_state = False
random_value = False
repeat = False

def PlayMusic():
    global current_music, duration, current_pos
    if random_value == True:
        current_music = random.choice(mp3_files)
        Playlist.activate(mp3_files.index(current_music))
        Playlist.selection_clear(0, 'end')
        Playlist.selection_set(mp3_files.index(current_music))
    else:
        current_music = Playlist.get(ACTIVE)
    mixer.music.load(current_music)
    duration = round(MP3(current_music).info.length)    
    current_pos = 0
    progress_bar.config(value=current_pos, maximum=duration)
    mixer.music.play()



def PauseMusic():
    global music_state
    if mixer.music.get_busy():
        mixer.music.pause()
    else:
        mixer.music.unpause()

def StopMusic():
    mixer.music.stop()
    progress_bar.config(value=0)
    mixer.music.unload()



def Volume_Music(event):
    mixer.music.set_volume(volume_music.get())




#button stop
def musicend():
    mixer.music.rewind()

#loop function
def loopb():
    global repeat
    if random_value == True:
        random_play()
    if repeat == False:
        repeat = True
    else:
        repeat = False

#update the frame of the gif 
def gifupdate(ind):
    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label.configure(image=frame)
    root.after(35, gifupdate, ind)
label = Label(root)
label.place(x=0, y=0)
root.after(0, gifupdate, 0)

def update():
    global current_pos
    if mixer.music.get_busy():
        progress_bar.config(value=current_pos+1)
        current_pos += 1
        print(round(current_pos), duration)
        if round(current_pos) == duration:
            song_end()
    root.after(1000, update)



def click(event, progress_bar):
    global current_pos
    new_pos = event.x * progress_bar["maximum"] / progress_bar.winfo_width()
    current_pos = new_pos
    mixer.music.set_pos(current_pos)
    progress_bar.config(value=current_pos)


def song_end():
    if repeat == True or random_value == True:
        PlayMusic()
    else:
        mixer.music.stop()
        progress_bar.config(value=0)
        mixer.music.unload()

#function,to play a random music in the playlist 
def random_play():
    global random_value
    if repeat == True:
        loopb()
    if random_value == False:
        random_value = True
    else:
        random_value = False


# icon
lower_frame = Frame(root, bg="#FFFFFF", width=485, height=180)
lower_frame.place(x=0, y=400)

image_icon = PhotoImage(file="logo png.png")
root.iconphoto(False, image_icon)

frameCnt = 30
frames = [PhotoImage(file='aa1.gif', format='gif -index %i' % (i)) for i in range(frameCnt)]




# Button
ButtonPlay = PhotoImage(file="play1.png")
Button(root, image=ButtonPlay, bg="#FFFFFF", bd=0, height=60, width=60, 
        command=PlayMusic ).place(x=200, y=487)


ButtonStop = PhotoImage(file="stop1.png")
Button(root, image=ButtonStop, bg="#FFFFFF", bd=0, height=60, width=60,
       command=StopMusic).place(x=130, y=487)

ButtonPause = PhotoImage(file="pause1.png")
Button(root, image=ButtonPause, bg="#FFFFFF", bd=0, height=60, width=60,
       command=PauseMusic).place(x=268, y=487)

Loop_base = Image.open("loop.png")
Loop_resize = Loop_base.resize((40, 40))
ButtonLoop = ImageTk.PhotoImage(Loop_resize)
Button(root, image=ButtonLoop, bg="#FFFFFF", bd=0, height=60, width=60, 
        command=loopb ).place(x=410, y=487)

Random_base = Image.open("random.png")
random_resize = Random_base.resize((40, 40))
ButtonRandom = ImageTk.PhotoImage(random_resize)
Button(root, image=ButtonRandom, bg="#FFFFFF", bd=0, height=60, width=60,
       command=random_play).place(x=335, y=487)

add_button = Button(root, text="Add File", command=add_file)
add_button.place(x=150, y=420)

remove_button = Button(root, text="Remove File", command=remove_file)
remove_button.place(x=260, y=420)

# Label
Menu_base= Image.open("menu.png")
Menu_resize= Menu_base.resize((200,50))
Menu = ImageTk.PhotoImage(Menu_resize)
Label(root, image=Menu).place(x=0, y=580, width=485, height=120)

Frame_Music = Frame(root, bd=2, relief=RIDGE)
Frame_Music.place(x=0, y=585, width=485, height=100)

# volume music slide bar
volume_music = tkinter.Scale(root, orient="horizontal", from_=0, to=1.0, resolution=0.1, command=Volume_Music)
volume_music.set(0.5)
volume_music.place(x=15, y=492, width=100, height=50)

#progress bar visual
progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=359, value=0, mode="determinate")
progress_bar.place(x=62, y=460)
progress_bar.bind("<Button-1>", lambda event: click(event, progress_bar))



Button(root, text="Browse Music", width=59, height=1, font=("calibri", 12, "bold"), fg="Black", bg="#FFFFFF",
       command=AddMusic).place(x=0, y=550)


Scroll = Scrollbar(Frame_Music)
Playlist = Listbox(Frame_Music, width=100, font=("Times new roman", 10), bg="#333333", fg="grey",
                   selectbackground="lightblue", cursor="hand2", bd=0, yscrollcommand=Scroll.set)
Scroll.config(command=Playlist.yview)
Scroll.pack(side=RIGHT, fill=Y)
Playlist.pack(side=RIGHT, fill=BOTH)

# Execute Tkinter
update()
root.mainloop()
