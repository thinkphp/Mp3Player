import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from pygame import mixer
import os

class MusicPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("Music Player")
        self.master.geometry("400x300")

        mixer.init()

        self.current_song_index = 0
        self.playlist = []

        self.play_button = tk.Button(master, text="Play", command=self.play_music)
        self.play_button.pack(pady=10)

        self.pause_button = tk.Button(master, text="Pause", command=self.pause_music)
        self.pause_button.pack(pady=10)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_music)
        self.stop_button.pack(pady=10)

        self.back_button = tk.Button(master, text="Back", command=self.play_previous)
        self.back_button.pack(side=tk.LEFT, padx=10)

        self.forward_button = tk.Button(master, text="Forward", command=self.play_next)
        self.forward_button.pack(side=tk.RIGHT, padx=10)

        self.choose_button = tk.Button(master, text="Choose Song", command=self.choose_file)
        self.choose_button.pack(pady=10)

        self.song_label = tk.Label(master, text="")
        self.song_label.pack(pady=10)

        # Volume Slider
        self.volume_label = tk.Label(master, text="Volume:")
        self.volume_label.pack()

        self.volume_slider = ttk.Scale(master, from_=0, to=1, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_slider.set(0.5)
        self.volume_slider.pack(pady=10)

        # Position Slider
        self.position_label = tk.Label(master, text="Position:")
        self.position_label.pack()

        self.position_slider = ttk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_position)
        self.position_slider.set(0)
        self.position_slider.pack(pady=10)

    def play_music(self):
        if self.playlist:
            mixer.music.load(self.playlist[self.current_song_index])
            mixer.music.play()
            self.song_label.config(text=f"Now Playing: {os.path.basename(self.playlist[self.current_song_index])}")

    def pause_music(self):
        mixer.music.pause()
        self.song_label.config(text="Music Paused")

    def stop_music(self):
        mixer.music.stop()
        self.song_label.config(text="Music Stopped")

    def play_previous(self):
        if self.playlist:
            self.current_song_index = (self.current_song_index - 1) % len(self.playlist)
            self.play_music()

    def play_next(self):
        if self.playlist:
            self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
            self.play_music()

    def choose_file(self):
        file = filedialog.askopenfilename(initialdir="/", title="Select File",
                                          filetypes=(("MP3 files", "*.mp3"), ("all files", "*.*")))
        if file:
            self.playlist.append(file)
            self.song_label.config(text=f"Added: {os.path.basename(file)}")

    def set_volume(self, val):
        mixer.music.set_volume(float(val))

    def set_position(self, val):
        if self.playlist:
            total_length = mixer.Sound(self.playlist[self.current_song_index]).get_length()
            position = (float(val) / 100) * total_length
            mixer.music.set_pos(position)


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
