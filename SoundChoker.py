import pyaudio
import pyautogui
import numpy
import tkinter as tk
from tkinter import messagebox as mbox	
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000

waitseconds = 5.0#待ち時間

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
    channels = CHANNELS,
    rate = RATE, #サンプリングレート
    input = True,
    frames_per_buffer = chunk
)

cnt = 0

def soundchoker():
    volumesetted  = 0.4

    currentVolumeDb = volume.GetMasterVolumeLevel()

    while True:
        data = stream.read(chunk)
        x = numpy.frombuffer(data, dtype="int16") / 32768.0
        print(x.max())
        if x.max() > volumesetted:
            volume.SetMasterVolumeLevel(-65, None)
        else:
            volume.SetMasterVolumeLevel(currentVolumeDb, None)
        

def closesoundchoker():
    stream.close()
    p.terminate()


#size
win = tk.Tk()
win.title("SoundChoker")
win.geometry("400x300")

soundchoker()

#make label
label = tk.Label(win, text = "set volume")
label.pack()

text = tk.Entry(win)
text.pack()
text.insert(tk.END, '50')

def ok_click():
    s = text.get()
    mbox.showinfo('inform','soundvolume is set to '+s+'.')

okButton = tk.Button(win, text = 'OK', command = ok_click)
okButton.pack()

#move window

closesoundchoker()
win.mainloop()