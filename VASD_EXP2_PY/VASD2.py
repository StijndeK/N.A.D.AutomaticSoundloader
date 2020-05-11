import os
import simpleaudio as sa
import soundfile
import random
import sys, select
import time
import glob

names = [] # to contain all wav files
entryList = [] # all different audio files
currentTrack = []
currentTransitionOptions = [] # current options for every layer to transition to 
loopDuration = 0
currentTransitionValue = "1"

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
        for layerEntryList in entryList:
            # set the number of the current layer
            currentEntryNumber = int(layerEntryList[0][3]) - 1
            # set what variation to play if options are initialised
            if currentTransitionOptions[currentEntryNumber]: 
                currentTransitionValue = currentTransitionOptions[currentEntryNumber][random.randint(1, len(currentTransitionOptions[currentEntryNumber])) - 1]
            # find track to play
            for entry in layerEntryList:
                if int(entry[1]) == int(currentTransitionValue):
                    currentTrack = entry
                    break
            # set new transition options
            currentTransitionOptions[currentEntryNumber] = currentTrack[2]
            # play track
            playTrack(currentTrack[0])
        # wait till tracks have finished playing
        time.sleep(loopDuration)
        # check if return is pressed        
        i,o,e = select.select([sys.stdin],[],[],0.0001)
        if i == [sys.stdin]: 
            break

# LOAD AND PARSE FILES
print ("Welcome!")
print("Loaded audio loops:")
for root, dirs, files in os.walk("."):
    for filename in files:
        if filename.endswith('.wav'): 
            print(" - " + filename)
            # convert tot 16 bit to make sure audio is playable and copy the audio so the source files are safe
            data, samplerate = soundfile.read(filename)
            newName = "".join(("new_", filename))
            soundfile.write(newName, data, samplerate, subtype='PCM_16')
            names.append(newName)
            # set all entrys in list
            possibleTransitions = []
            tempName = newName[:-4] # remove wav extension
            # set possible transitions
            while True:
                possibleTransition = tempName[-1]
                if possibleTransition != "_":
                    possibleTransitions.append(possibleTransition)
                    tempName = tempName[:-1]
                else:
                    break
            # init lists
            while len(entryList) < int(newName[6]):
                entryList.append([])
                currentTransitionOptions.append([])
            # add entry
            entryList[int(newName[6]) - 1].append([newName, newName[4], possibleTransitions , newName[6]]) # layer [filename, loopnumber, [transition possibilities], vertical layer number]

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

