import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pygame
from mutagen.mp3 import MP3
from PIL import ImageTk, Image

# Initialize pygame
pygame.mixer.init()

# Create the main window
root = tk.Tk()
root.title("Anus mp3 player")
root.geometry("800x500")
root.configure(background="#303030")

# Load custom fonts
title_font = ("Montserrat", 18, "bold")
label_font = ("Montserrat", 12)
button_font = ("Montserrat", 12, "bold")

# Load custom icons
play_icon = ImageTk.PhotoImage(Image.open("C:\\Users\\Anurag\\OneDrive\\Desktop\\error\\play2.png").resize((40, 40)))
pause_icon = ImageTk.PhotoImage(Image.open("C:\\Users\\Anurag\\OneDrive\\Desktop\\error\\download.png").resize((40, 40)))
skip_forward_icon = ImageTk.PhotoImage(Image.open("C:\\Users\\Anurag\\OneDrive\\Desktop\\error\\skip forward.png").resize((30, 30)))
skip_back_icon = ImageTk.PhotoImage(Image.open("C:\\Users\\Anurag\\OneDrive\\Desktop\\error\\skip backward.png").resize((30, 30)))
add_icon = ImageTk.PhotoImage(Image.open("C:\\Users\\Anurag\\OneDrive\\Desktop\\error\\Add.png").resize((30, 30)))
remove_icon = ImageTk.PhotoImage(Image.open("C:\\Users\\Anurag\\OneDrive\\Desktop\\error\\remove.png").resize((30, 30)))

# Create a list to store the audio files
playlist = []
current_song = 0

# Function to browse and add audio files to the playlist
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    if file_path:
        playlist.append(file_path)
        song_title = os.path.basename(file_path)
        song_length = get_song_length(file_path)
        playlist_box.insert(tk.END, f"{song_title} - {song_length}")

# Function to remove selected audio file from the playlist
def remove_file():
    global current_song
    current_selection = playlist_box.curselection()
    if current_selection:
        if current_selection[0] == current_song:
            stop_music()
            current_song = 0
        playlist.pop(current_selection[0])
        playlist_box.delete(current_selection[0])

# Function to get the length of an audio file in minutes and seconds
def get_song_length(file_path):
    audio = MP3(file_path)
    song_length = audio.info.length
    minutes, seconds = divmod(song_length, 60)
    return f"{int(minutes):02d}:{int(seconds):02d}"

# Function to play selected audio file
def play_music():
    global current_song
    if not pygame.mixer.music.get_busy():
        if playlist:
            current_song = 0
            play_button.config(image=pause_icon)
            current_song_title.config(text=os.path.basename(playlist[current_song]))
            current_song_length.config(text=get_song_length(playlist[current_song]))
            pygame.mixer.music.load(playlist[current_song])
            pygame.mixer.music.play()
            update_song_time()
    else:
        pygame.mixer.music.unpause()
        play_button.config(image=pause_icon)

# Function to pause playing music
def pause_music():
    pygame.mixer.music.pause()
    play_button.config(image=play_icon)

# Function to stop playing music
def stop_music():
    global current_song
    pygame.mixer.music.stop()
    play_button.config(image=play_icon)
    current_song = 0
    current_song_title.config(text="")
    current_song_length.config(text="")

# Function to skip forward to the next song
def skip_forward():
    global current_song
    if current_song < len(playlist) - 1:
        current_song += 1
    else:
        current_song = 0
    pygame.mixer.music.load(playlist)
    
    
    pygame.mixer.music.load(playlist[current_song])
    pygame.mixer.music.play()
    current_song_title.config(text=os.path.basename(playlist[current_song]))
    current_song_length.config(text=get_song_length(playlist[current_song]))
    update_song_time()

# Function to skip back to the previous song
def skip_back():
    global current_song
    if current_song > 0:
        current_song -= 1
    else:
        current_song = len(playlist) - 1
    pygame.mixer.music.load(playlist[current_song])
    pygame.mixer.music.play()
    current_song_title.config(text=os.path.basename(playlist[current_song]))
    current_song_length.config(text=get_song_length(playlist[current_song]))
    update_song_time()

# Function to update the song time label every second
def update_song_time():
    if pygame.mixer.music.get_busy():
        current_time = pygame.mixer.music.get_pos() / 1000
        minutes, seconds = divmod(current_time, 60)
        current_song_time.config(text=f"{int(minutes):02d}:{int(seconds):02d}")
        root.after(1000, update_song_time)

# Create browse button
add_button = ttk.Button(root, image=add_icon, command=browse_file)
add_button.place(x=50, y=50)

# Create remove button
remove_button = ttk.Button(root, image=remove_icon, command=remove_file)
remove_button.place(x=100, y=50)

# Create playlist box
playlist_box = tk.Listbox(root, font=label_font, bg="#484848", fg="#ffffff", selectbackground="#0059b3", selectforeground="#ffffff", highlightthickness=0)
playlist_box.place(x=50, y=100, width=700, height=250)

# Create play button
play_button = ttk.Button(root, image=play_icon, command=play_music)
play_button.place(x=350, y=375)

# Create pause button
pause_button = ttk.Button(root, image=pause_icon, command=pause_music)
pause_button.place(x=420, y=375)

# Create stop button
stop_button = ttk.Button(root, text="Stop", style="Custom.TButton", command=stop_music)
stop_button.place(x=500, y=375)

# Create skip back button
skip_back_button = ttk.Button(root, image=skip_back_icon, command=skip_back)
skip_back_button.place(x=300, y=375)

# Create skip forward button
skip_forward_button = ttk.Button(root, image=skip_forward_icon, command=skip_forward)
skip_forward_button.place(x=470, y=375)

# Create current song label
current_song_title = ttk.Label(root, font=title_font, foreground="#ffffff", background="#303030")
current_song_title.place(x=50, y=450)

# Create current song length label
current_song_length = ttk.Label(root, font=label_font, foreground="#ffffff", background="#303030")
current_song_length.place(x=650, y=450)

# Create current song time label
current_song_time = ttk.Label(root, font=label_font, foreground="#ffffff", background="#303030")
current_song_time.place(x=600, y=450)

# Start the main event loop
root.mainloop()

# Quit pygame
pygame.quit()

