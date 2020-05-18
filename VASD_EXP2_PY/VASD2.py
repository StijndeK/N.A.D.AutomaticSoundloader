import os
import simpleaudio as sa
import soundfile
import random
import sys, select
import time
import glob

names = []
currentTrack = []
currentTransitionOptions = []
loopDuration = 0
currentTransitionValue = "1"
layers = []

# CLASSES
class LayerVariation():
    def __init__(self, filename, loopnumber, possibleTransitions):
        self.filename = filename
        self.loopnumber = loopnumber
        self.possibleTransitions = possibleTransitions
class Layer():
    def __init__(self, layer, layerVariations):
        self.layer = layer
        self.layerVariations = layerVariations

# FUNCTIONS
def playTrack(name):
    wave_obj = sa.WaveObject.from_wave_file(name)
    print("playing: " + name)
    play_obj = wave_obj.play()

def calculateTime():
    while True:
        bpm = float(input("set bpm: "))
        if bpm > 0 and bpm < 300:
            break
    while True:
        beats = float(input("set loop length in beats: "))
        if beats > 0:
            break
    return (60/bpm) * beats

def play():
    print ("Now playing")
    print ("Press return to stop audio")
    while True:
        global currentTransitionValue
        for layer in layers:
            # current layer
            currentEntryNumber = layer.layer

            # set what variation to play if options are initialised
            if currentTransitionOptions[currentEntryNumber]: 
                currentTransitionValue = currentTransitionOptions[currentEntryNumber][random.randint(1, len(currentTransitionOptions[currentEntryNumber])) - 1]

            # find track to play
            for layerVar in layer.layerVariations:
                if int(layerVar.loopnumber) == int(currentTransitionValue):
                    currentTrack = layerVar
                    break

            # set new transition options
            currentTransitionOptions[currentEntryNumber] = currentTrack.possibleTransitions

            playTrack(currentTrack.filename)

        time.sleep(loopDuration)

        # check if return is pressed        
        i,o,e = select.select([sys.stdin],[],[],0.0001)
        if i == [sys.stdin]: 
            break

# LOAD AND PARSE FILES
print ("Welcome!")
currentLayerNumber = -1
for root, dirs, files in os.walk("./Bounces/"):
    if root != "./Bounces/":
        layers.append(Layer(int(root[-1]) - 1, []))
        currentLayerNumber = currentLayerNumber + 1
        currentTransitionOptions.append([])
    for filename in files:
        if filename.endswith('.wav'): 
            # set possible transitions
            possibleTransitions = []
            tempName = filename[:-4] # remove wav extension
            while True:
                possibleTransition = tempName[-1]
                if possibleTransition != "_":
                    possibleTransitions.append(int(possibleTransition))
                    tempName = tempName[:-1]
                else:
                    break

            # convert tot 16 bit to make sure audio is playable and copy the audio so the source files are safe
            data, samplerate = soundfile.read(root + "/" + filename)
            newName = root + "/" + "new_" + filename
            names.append(newName)
            soundfile.write(newName, data, samplerate, subtype='PCM_16')

            # set layer data
            layers[currentLayerNumber].layerVariations.append(LayerVariation(newName, filename[0], possibleTransitions))



print("Audio loaded: ")
for layer in layers:
    for layerVar in layer.layerVariations:
        print(layerVar.filename)

# LOOP
loopDuration = calculateTime()

# main game loop
while True:
    while True:
        i = input("Type 'p' to play or 'q' to quit: ")
        if i == "p" or i == "q":
            break
    if i == "p":
        "Playing"
        play()
    else: 
        print("bye!")
        break

# EXIT
for name in names:
    os.remove(name)