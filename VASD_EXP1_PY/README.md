# EXP1
The first VASD prototype. EXP1 allows the user to quickly test a horizontal non-linear system that doesn't require any input (doesn't adapt to game parameters). Export audio directly into the folder with specific file names and they will automatically be sequenced based on the given options.

## Example
Applied to Rookery
- [EXP1](https://streamable.com/wmomb)

## Instructions
Place audio files in the same folder as the python program. Set the export location of the DAW to this folder to allow for quick testing and prototyping of the non-linear audio system.
The amount of loops is limited to 10 files (0 to 9). 

### File naming
- Start the file name with the number of the loop and end with a '_'.
- Type any information or name you like and again end with a '_'
- End the file name with the numbers of the audio track that the loop can transition to

For example:
1_NameAndOtherInformation_124.wav
is the first track and can loop or transition to track 2 or 4

## Reflection
| Improvements    | Drawback       | Missing  |
| ------------- |:-------------:| -----:|
| quick testing | specific file naming | Vertical layering |
| | Clicks in transitions | Adaption to game parameters |
| | | Added context, both visual and interactive |
| | | Clear overview |
| | | Chance percentages |
| | | Transition techniques |
