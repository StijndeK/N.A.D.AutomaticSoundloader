import os
import simpleaudio as sa
import soundfile
import random
import sys, select
import time
import glob

print ("Welcome!")
print ("Press return to stop audio playing")

# initialise 
nameList = [] # to contain all wav files
newNameList = [] # to contain all new wav files
entryList = [] # all different audio files
currentTrack = []
loopDuration = 0
layerAmount = 0
newEntryList = []
currentTransitionOptions = []

# on start remove created files incase they didnt get removed on destroy
for filename in glob.glob("./new_*"):
    os.remove(filename) 

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
    newDuration = (60/bpm) * beats
    return newDuration

def play():
    print ("Now playing")
    first = [True, True, True, True, True, True, True, True, True, True] #TODO: create a dynamic checking system
    while True:
        for layerEntryList in newEntryList:
            # set the number of the current layer
            currentEntryNumber = int(layerEntryList[0][3]) - 1
            # choose what track to play
            if first[currentEntryNumber]:
                transitionValue = 1
                first[currentEntryNumber] = 0
            else:
                transitionValue = currentTransitionOptions[currentEntryNumber][random.randint(1, len(currentTransitionOptions[currentEntryNumber])) - 1]
            # find track
            for entry in layerEntryList:
                if int(entry[1]) == int(transitionValue):
                    currentTrack = entry
                    break
            # play track
            playTrack(currentTrack[0])
            # set new transition options
            currentTransitionOptions[currentEntryNumber] = currentTrack[2]
        # wait till tracks have finished playing
        time.sleep(loopDuration)
        # check if return is pressed        
        i,o,e = select.select([sys.stdin],[],[],0.0001)
        if i == [sys.stdin]: 
            break

# LOAD FILES
# get al wav files in a list
print("Loaded audio loops:")
for root, dirs, files in os.walk("."):
    for filename in files:
        if filename.endswith('.wav'): 
            print(" - " + filename)
            nameList.append(filename)

# convert tot 16 bit to make sure audio is playable and copy the audio so the source files are safe
for name in nameList:
    data, samplerate = soundfile.read(name)
    newName = "".join(("new_", name))
    soundfile.write(newName, data, samplerate, subtype='PCM_16')
    newNameList.append(newName)

# set all entrys in list
for name in newNameList:
    # set possible transitions
    possibleTransitions = []
    tempName = name[:-4] # remove .wav
    while True:
        possibleTransition = tempName[-1]
        if possibleTransition != "_":
            possibleTransitions.append(possibleTransition)
            tempName = tempName[:-1]
        else:
            break
    # add entry
    entryList.append([name, name[4], possibleTransitions , name[6]]) # filename, loopnumber, [transition possibilities], vertical layer number

    # update layerAmount
    if int(name[6]) > layerAmount:
        layerAmount = int(name[6])

# divide entry list into 2d array ([vertical layer],[vertical layer],..)
# TODO: do this immediatly when setting al entrys
for x in range(layerAmount):
    newEntryList.append([])
    currentTransitionOptions.append([]) # initialise empty array to hold transition options
    for entry in entryList:
        if int(entry[3]) == (x + 1):
            newEntryList[x].append(entry)

# LOOP
# set duration of loop
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
# on destroy remove created files
for name in newNameList:
    os.remove(name)

