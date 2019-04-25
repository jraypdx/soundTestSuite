#some of this code from a stack overflow answer: https://stackoverflow.com/questions/8299303/generating-sine-wave-sound-in-python

import pyaudio
import numpy as np
from appJar import gui
import notes

app = gui()
p = pyaudio.PyAudio()

volume = 0.25     # range [0.0, 1.0]
fs = 44100       # sampling rate, Hz, must be integer
duration = .1   # in seconds, may be float
#f = 440.0        # sine frequency, Hz, may be float

def playSound(f, w, v):
    if (f == 0):
        f = 440
    # generate samples, note conversion to float32 array
    if w == "Sine":
        samples = (np.sin(2 * np.pi * np.arange(fs * duration * 4) * float(f) / fs)).astype(np.float32)
    elif w == "Triangle":
        samples = (np.sin(2 * np.pi * np.arange(fs * duration * 4) * float(f) / fs)).astype(np.float32)
    elif w == "Saw":
        #samples = -((2/np.pi) * np.arctan(1/(np.tan((np.arange(fs * duration * 4)*np.pi)/float(f)))).astype(np.float32))
        samples = (-1/2) * ((np.sin(2 * np.pi * np.arange(fs * duration * 4) * 2 * float(f) / fs)).astype(np.float32))
    elif w == "Square":
        samples = np.sign((np.sin(2 * np.pi * np.arange(fs * duration * 4) * float(f) / fs)).astype(np.float32))
    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)

    # play. May repeat with different volume values (if done interactively)
    #vvv = 1.5 + np.log(float(v)/100)/np.log(500)
    stream.write(v*samples)
    stream.stop_stream()
    stream.close()


def press(button):
    wave = app.getRadioButton("wave")
    #freq = app.getEntry("Frequency")
    vol = float(app.getScale("Volume") / 100)
    #print (vol)
    if button == "Cancel":
        app.stop()
    else:
        freq = notes.getFreq(app.getOptionBox("Note"), str(app.getOptionBox("Octave")))
        playSound(freq, wave, vol)

app.addLabelOptionBox("Note", ["C", "C#/Db", "D",
                        "D#/Eb", "E", "F", "F#/Gb", "G",
                        "G#/Ab", "A", "A#/Bb", "B"])
app.addLabelOptionBox("Octave", ["3", "4", "5"])
app.addRadioButton("wave", "Sine")
app.addRadioButton("wave", "Triangle")
app.addRadioButton("wave", "Saw")
app.addRadioButton("wave", "Square")
#app.addLabelEntry("Frequency")
app.addLabel("l1", "Volume:")
app.addScale("Volume")
app.showScaleValue("Volume", show=True)
app.setScale("Volume", 50, callFunction=False)
app.addButtons(["Play", "Cancel"], press)
app.go()

p.terminate()