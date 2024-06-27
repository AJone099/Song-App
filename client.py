import socket
from threading import Thread
from tkinter import *
from tkinter import ttk, filedialog
from playsound import playsound
import pygame 
from pygame import mixer
import os
import time

PORT = 8050
IP_ADDRESS = '127.0.0.1'
SERVER = None
BUFFER_SIZE = 4096

def musicWindow():
    window = Tk()
    window.title("Music Window")
    window.geometry("300x300")
    window.configure(bg = "LightSkyBlue")

    global listbox

    selectlabel = Label(window, text = "Select Song", bg = "LightSkyBlue", font = ("Calibri", 10))
    selectlabel.place(x = 2, y = 1)

    listbox = Listbox(window, height = 10, width = 39, activestyle = "dotbox", bg = "LightSkyBlue", borderwidth = 2, font = ("Calibri", 10))
    listbox.place(x = 10, y = 10)

    scrollbar1 = Scrollbar(listbox)
    scrollbar1.place(relheight = 1, relx = 1)
    scrollbar1.config(command = listbox.yview)

    PlayButton = Button(window, text = "Play", width = 10, bd = 1, bg = "SkyBlue", borderwidth = 2, font = ("Calibri", 10), command = play)
    PlayButton.place(x = 30, y = 200)

    Stop = Button(window, text = "Stop", bd = 1, width = 10, bg = "SkyBlue", font = ("Calibri", 10), command = stop)
    Stop.place(x = 200, y = 200)

    ResumeButton = Button(window, text = "Resume", width = 10, bd = 1, bg = "SkyBlue", font = ("Calibri", 10), command = resume)
    ResumeButton.place(x = 10, y = 250)

    PauseButton = Button(window, text = "Pause", width = 10, bd =1, bg = "SkyBlue", font = ("Calibri", 10), command = pause)
    PauseButton.place(x = 200, y = 250)

    Upload = Button(window, text = "Upload", width = 10, bd = 1, bg = "SkyBlue", font = ("Calibri", 10))
    Upload.place(x = 30, y = 250)

    Download = Button(window, text = "Download", width = 10, bd = 1, bg = "SkyBlue", font = ("Calibri", 10))
    Download.place(x = 200, y = 250)

    global infoLabel
    infoLabel = Label(window, text = "", fg = "blue", font = ("Calibri", 10))
    infoLabel.place(x = 4, y = 200)

    for file in os.listdir("shared_files"):
        filename = os.fsdecode(file)
        listbox.insert(END, filename)

    window.mainloop()

def play():
    global song_selected
    song_selected = listbox.get(ANCHOR)

    pygame.init()
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.play()

    if song_selected != "":
        infoLabel.configure(text = "Now Playing: " + song_selected)
    else:
        infoLabel.configure(text = "")

def stop():
    global song_selected
    mixer.music.stop()
    infoLabel.configure(text = "")

def resume():
    global song_selected
    mixer.init()
    mixer.music.load("shared_files/"+song_selected)
    mixer.music.play()

def pause():
    global song_selected
    pygame
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.pause()

def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    musicWindow()

setup()