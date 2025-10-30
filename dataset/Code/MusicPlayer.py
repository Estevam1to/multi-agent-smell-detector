#Create a tkinter gui to play music

from tkinter import *
from tkinter import filedialog
import pygame

root = Tk()
root.title("Music Player")
root.geometry("500x400")

#initialize pygame mixer
pygame.mixer.init()

#add song function
def add_song():
    song = filedialog.askopenfilename(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
    #strip out the directory info and .mp3 from the song name
    song = song.replace("C:/Users/Owner/Desktop/Python/audio/", "")
    song = song.replace(".mp3", "")
    #add song to listbox
    song_box.insert(END, song)

#add many songs to playlist
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
    #loop through song list and replace directory info and mp3
    for song in songs:
        song = song.replace("C:/Users/Owner/Desktop/Python/audio/", "")
        song = song.replace(".mp3", "")
        #insert into playlist
        song_box.insert(END, song)
    
#play selected song
def play():
    #set stopped to false since a song is now playing
    global stopped
    stopped = False
    song = song_box.get(ACTIVE)
    song = f'C:/Users/Owner/Desktop/Python/audio/{song}.mp3'
    
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

#stop playing current song
global stopped
stopped = False
def stop():
    #stop song
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    
    #clear status bar
    status_bar.config(text='')
    
    #set stop variable to true
    global stopped
    stopped = True

#play next song in playlist
def next_song():
    #reset stopped variable
    global stopped
    stopped = False
    #get the current song number
    next_one = song_box.curselection()
    #add one to the current song number
    next_one = next_one[0]+1
    #grab the song title from the playlist
    song = song_box.get(next_one)
    #add directory structure and mp3 to the song title
    song = f'C:/Users/Owner/Desktop/Python/audio/{song}.mp3'
    
    #load song with pygame mixer
    pygame.mixer.music.load(song)
    #play song with pygame mixer
    pygame.mixer.music.play(loops=0)
    
    #clear active bar in playlist
    song_box.selection_clear(0, END)
    
    #move active bar to next song
    song_box.activate(next_one)
    
    #set active bar to next song
    song_box.selection_set(next_one, last=None)

#play previous song in playlist
def previous_song():
    #reset stopped variable
    global stopped
    stopped = False
    #get the current song number
    next_one = song_box.curselection()
    #add one to the current song number
    next_one = next_one[0]-1
    #grab the song title from the playlist
    song = song_box.get(next_one)
    #add directory structure and mp3 to the song title
    song = f'C:/Users/Owner/Desktop/Python/audio/{song}.mp3'
    
    #load song with pygame mixer
    pygame.mixer.music.load(song)
    #play song with pygame mixer
    pygame.mixer.music.play(loops=0)
    
    #clear active bar in playlist
    song_box.selection_clear(0, END)
    
    #move active bar to next song
    song_box.activate(next_one)
    
    #set active bar to next song
    song_box.selection_set(next_one, last=None)

#delete a song
def delete_song():
    #stop song from playing
    pygame.mixer.music.stop()
    #delete highlighted song from playlist
    song_box.delete(ANCHOR)
    #clear status bar
    status_bar.config(text='')

#delete all songs
def delete_all_songs():
    #stop song from playing
    pygame.mixer.music.stop()
    #delete all songs from playlist
    song_box.delete(0, END)
    #clear status bar
    status_bar.config(text='')

#create global pause variable
global paused
paused = False

#pause and unpause the song
def pause(is_paused):
    global paused
    paused = is_paused
    
    if paused:
        #unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        #pause
        pygame.mixer.music.pause()
        paused = True

#create volume function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

#create slider function
def slide(x):
    #slider_label.config(text=f'{int(my_slider.get())} of {int(length)}')
    song = song_box.get(ACTIVE)
    song = f'C:/Users/Owner/Desktop/Python/audio/{song}.mp3'
    
    #load song with pygame mixer
    pygame.mixer.music.load(song)
    #play song with pygame mixer
    pygame.mixer.music.play(loops=0, start=my_slider.get())

#create main frame
main_frame = Frame(root)
main_frame.pack(pady=20)

#create song box
song_box = Listbox(main_frame, bg="black", fg="green", width=60, selectbackground="green", selectforeground="black")
song_box.grid(row=0, column=0)

#create player control frame
controls_frame = Frame(main_frame)
controls_frame.grid(row=1, column=0, pady=20)

#create volume frame
volume_frame = LabelFrame(main_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=20)

#create playlist box
playlist_box = Listbox(main_frame, bg="black", fg="green", width=60)
playlist_box.grid(row=0, column=2)

#create player control buttons
back_btn_img = PhotoImage(file='MusicPlayer\Assets\previousSongButton.png')
forward_btn_img = PhotoImage(file='MusicPlayer\Assets\(n)extSongButton.png')
play_btn_img = PhotoImage(file='MusicPlayer\Assets\playButton.png')
pause_btn_img = PhotoImage(file='MusicPlayer\Assets\pauseButton.png')
stop_btn_img = PhotoImage(file='MusicPlayer\Assets\stopButton.png')

back_button = Button(controls_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(controls_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

#create menu
my_menu = Menu(root)
root.config(menu=my_menu)

#create add song menu dropdown
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
#add one song to playlist
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)
#add many songs to playlist
add_song_menu.add_command(label="Add Many Songs To Playlist", command=add_many_songs)

#create delete song menu dropdown
remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
#remove one song from playlist
remove_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
#remove all songs from playlist
remove_song_menu.add_command(label="Delete All Songs From Playlist", command=delete_all_songs)

#create status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

#create volume slider
volume_slider = Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, length=125, command=volume)
volume_slider.pack(pady=10)

#create song slider
my_slider = Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, value=0, length=360, command=slide)
my_slider.grid(row=2, column=0, pady=10)

#temp label
#slider_label = Label(main_frame, text='0')
#slider_label.grid(row=2, column=0)

root.mainloop()



###CREDITS###
#Main code chunk credit to GithubCopilot
#Icons credit to gibustudio on Vecteezy.com
