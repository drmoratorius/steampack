# How To Build Dr. Moratorius' SteamPack

**Please note: This is more of a reference than a full tutorial!**

## 1. Box & Transport
The base is a wooden box (see [parts](PARTS.MD)) which can be opened easily and has a simple lock. Instead of the original
way to transport the box two new mounting options are used so that the box can be transported as a backpack using belts.

Belt:
![mounting top](pics/steampack-final-03.jpg)
![mounting top](pics/steampack-final-13.jpg)

Belt mounting:
![mounting top](pics/steampack-final-06.jpg)

![mounting bottom](pics/steampack-final-09.jpg)

In addition to allow to place it standing up on a table additional parts have been added:

![mounting bottom](pics/steampack-final-10.jpg)


 ## 2. LEDs, Switches and Labels

For the LEDs and switches holes have been drilled. The labels have been screwed in directly with the provided screws.
Two large Edison-style LEDs with 3V are used and three clear orange LEDs to simulate old-style glow lamps.
Furthermore, an old cathode ray tube has been used with a simple warm white LED glued to the bottom.

![mounting top](pics/steampack-11.jpg)
![mounting top](pics/steampack-12.jpg)

All of the elements have been "aged" using acrylic colors.

## 3. Simulated Fire

The simulated fire of the presumed steam engine is created using a simple USB LED flicker light where the top and bottom
parts have been removed and cables soldered directly to the +5V and GND pins.
![mounting top](pics/steampack-03.jpg)

A plastic dome is used and is filled with simple clear plastic foil at the bottom and top surrounding the LED flicker light.

![mounting top](pics/steampack-07.jpg)

For best lighting the bottom is made from cardboard and covered with aluminium foil which then again is covered by clear
packing tape to prevent any shorts through the aluminium.

![mounting top](pics/steampack-04.jpg)
![mounting top](pics/steampack-05.jpg)
![mounting top](pics/steampack-06.jpg)
![mounting top](pics/steampack-08.jpg)
![mounting top](pics/steampack-09.jpg)
![mounting top](pics/steampack-10.jpg)

Is is then covered with some foam rubber parts that have been painted with acrylic colors.

![mounting top](pics/steampack-final-11.jpg)

## 4. Foggers ("Steam")

The foggers are ultrasonic mist boards connected to a piezo speaker that you can buy as a complete part.
However, when purchasing the boards without buttons (which are working as long as they have USB power) the extensions
are a bit short so different ones were used (see [parts list](PARTS.MD) for details).

These things are then put into plastic vials which are held by 3d-printed vial holders made specifically for this
project. You can download the files from the `3d` directory.

![mounting top](pics/steampack-14.jpg)
![mounting top](pics/steampack-16.jpg)


However, when using these you have to take into account that you will have to pour in new water if all of it has
been used up. To achieve this the original cables are made longer using extension cables. Also, the boards are inside
the wooden box. That means even if overfilled it will simply drip to the floor and not reach any electronics. 

![mounting top](pics/steampack-21.jpg)

They are also covered with simple foam rubber parts so that you can easily take them out if the vials need to be 
refilled.

![mounting top](pics/steampack-20.jpg)

The foggers are also covered with some simple foam part:

![mounting top](pics/steampack-17.jpg)
![mounting top](pics/steampack-18.jpg)

The vial holders are then covered with more foam rubber painted black and gold to achieve a brass-like coloring.

![mounting top](pics/steampack-19.jpg)

There is a pattern available for them you can print (do not resize when printing, otherwise it won't fit).
Actually the coverings are a bit too large which means that the "outer" part of the vials cannot stick to the holder,
but is still holds perfectly when using superglue on all sides of the vial holder.

Please note that you have to be able to take out the full foggers so the cable needs to be long enough.

![mounting top](pics/steampack-final-08.jpg)



## 5. Sound

For sound the sound module DY-SV5W is used. It features several modes and the one used uses its 8 inputs to specify
the MP3 file to be played (`00001.mp3` - `00255.mp3`). The MP3 files are stored with respective names in the root of
the microSD card (max. 32 GB card supported - with FAT32 formatted).

The sound list can be found on the [home](README.MD) page.

## 6. Sound Functionality

The software plays certain sounds when certain switches are switched and always when steam is emitted to greatly
enhance the effect, because the foggers don't really create any audible sound at all so people are a bit confused
(hopefully) on the sound.

A simple 5W 4 ohms speaker is used attached to the sound board and its volume set accordingly through the built-in
potentiometer.

## 7. The Rest

The curly metal part I got from ebay from an old machine so I don't know any source to buy it.
![mounting top](pics/steampack-final-04.jpg)

It also features a "case open" reed contact to stop any program when opening the box (you usually don't want to get the
fog in your face there).

## 8. Electronics In The Box
As this essentially is a prototype it doesn't really look great from the inside. Creating a PCB for everything would
be a perfect addition (I know).

Everything's simply screwed or glued in there to ensure that it stays in place. 

![mounting top](pics/steampack-board-info.jpg)

![mounting top](pics/steampack-final-14.jpg)
![mounting top](pics/steampack-final-15.jpg)
![mounting top](pics/steampack-final-16.jpg)
![mounting top](pics/steampack-final-17.jpg)
![mounting top](pics/steampack-final-18.jpg)
![mounting top](pics/steampack-final-19.jpg)

I hope you like it! :) 