# EXP2
The second VASD prototype. EXP2 builds further on [EXP1](https://github.com/StijndeK/VASD/tree/master/VASD_EXP1_PY). Added features are vertical layering and allowing audiotails.

## Example
Applied to Rookery
- [EXP2](https://streamable.com/reu4v)

## Instructions
Place audio files in the same folder as the python program. Set the export location of the DAW to this folder to allow for quick testing and prototyping of the non-linear audio system.
The amount of loops and the amount of layers are limited to 9 files (1 to 9). 

### File naming
- Start the file name with the number of the loop (1 to 9) and end with '_'
- Then type the number of the layer (1 to 9) and end with '_'
- Type any information or name you like and again end with '_'
- End the file name with the numbers of the audio track that the loop can transition to

For example:
1_1_NameAndOtherInformation_124.wav
is the first track on the first layer and can loop or transition to track 2 or 4

## Reflection
| Improvements    | Drawback       | Missing  |
| ------------- |:-------------:| -----:|
| Tail playback | Even more specific file naming | Transition techniques |
| Vertical layering | Requires more user input | Adaption to game parameters |
| | | Added context, both visual and interactive |
| | | Clear overview |
| | | Chance percentages |