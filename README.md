# Dr. Moratorius' SteamPack

This is a repository explaining how I built my steam pack and also provide 
all of the required files and information.
Please note that this is more a repository that can help you build your own
or adapt it and not a full tutorial.

## Features
* Powered by USB (power bank)
* Powered by Raspberry Pi Pico 2 W using MicroPython
* Wooden Backpack
* Sounds
* Timed steam (ultrasonic fogger) output with corresponding supporting steam sound
* Sounds when turning on and off certain parts
* and more!

## Components
* [parts list](docs/PARTS.MD)
* [labels (DOCX)](docs/Schilder.docx)
* [vial holder outer part pattern](docs/Schnittmuster.pdf) - print 100% (do not resize to printer edges) - does not fully cover outer part, but sufficient
* 3D printer files
  * [Vial holder (left) - STL](3d/Moratorius_Steampack_Vial_Holder_R.stl) 
  * [Vial holder (right) - STL](3d/Moratorius_Steampack_Vial_Holder_R.stl)
  * [Vial holder (left) - GCODE for Anycubic i3 MEGA](3d/AIM/AIM_Moratorius_Steampack_Vial_Holder_L.gcode)
  * [Vial holder (right) - GCODE for Anycubic i3 MEGA](3d/AIM/AIM_Moratorius_Steampack_Vial_Holder_R.gcode)
* [Fritzing breadboard layout](fritzing/DrMoratorius-SteamPack-Breadboard.fzz) - still missing schematic and audio part 

## Software
* The code uses the latest MicroPython download from https://www.raspberrypi.com/documentation/microcontrollers/micropython.html
* The source code is available in the `src` directory and still WIP!
* It loads most of the configuration from the `config.json` file, but some parts are (still) hardcoded
* Potential ideas for the future: allow control via smartphone through a WiFi AP

## Sounds
The used sound module [DY-SV5W](https://shop.cpu.com.tw/upload/2022/09/VC0147_DY-SV5W-3.pdf) is using an
SD card (32 GB max, FAT32) with several sounds mixed from available sounds online. Here is a selection:
* https://freesound.org/people/qubodup/sounds/194882/
* https://freesound.org/people/qubodup/sounds/395041/
* https://freesound.org/people/mike_stranks/sounds/407394/
* https://freesound.org/people/craigsmith/sounds/438641/
* https://freesound.org/people/theshaggyfreak/sounds/440453/
* https://freesound.org/people/stib/sounds/487748/
* https://freesound.org/people/Engineer_815/sounds/493558/ (main steam sound used)
* https://freesound.org/people/rottako/sounds/693587/
* https://freesound.org/people/qubodup/sounds/752067/
* https://www.youtube.com/watch?v=LwiOCsfa_ZA (gear sounds)
* https://freesound.org/people/Vibratair/sounds/403892/ (electricity)
* https://freesound.org/people/Halleck/sounds/19487/ (electricity)
* https://freesound.org/people/Vibratair/sounds/403892/ (electricity)
* https://freesound.org/people/opyate/sounds/518945/ (on/off sound - off = reverted)

## Partical Notes
If you use a power bank please keep in mind that most turn off completely if the attached device
does not use a lot of power requiring you to open the case and turn on the powerbank again.
For the future using 18650 cells (with additional protection circuit) with corresponding
charging board might be an option.


