# Fishington

Fishington is a game about fishing and talking to other players.
Enjoy a peacefull place around a lake, throw your line and get your first fishes and friends !

The game is accessible at:

https://fishington.io/


# Bot

## Setup

1. Install the dependencies :

```
pip install -r requirements.txt
```

## Files

1. exclamation_array.py

This file stores ( almost ) all the colors of the exclamation mark that appears above the player when he catches a fish.
You'll have to update it if the color changes one day.

2. mouse_handler.py

This module allows the user to manually enter the various crucial points on which the robot will be based.
Pressing '1' will register the current cursor position and save it.
The registration key can be modified in the config file if required, under the name 'TRIGGER KEY'.

3. launch_me.py

Main file for the fishing robot.

Simply run this file and interact with the program's various proposals/requests so that it runs smoothly.

The first time, you'll have to enter the positions manually, so that it adapts to the size of the window and screen. Once launched, the positions will be saved in the config file, so that the next time there's less fiddling to do, all you have to do is press enter frantically.

The last two config parameters are delta for the stopper. Adjustable in the file, they allow you to set the 'danger' zones so that it doesn't go too far from the edges.

## Use

Launch the game on your browser.

Simply launch the launch_me.py file and follow the program's instructions.

If you haven't set a specific key for capturing mouse positions, press '1' when the mouse is in the right place to validate the step and move on to the next.

You'll need to record 8 different positions.

Once done, place your character between the sales area and the water and press enter one last time, then select the game window before the program starts (you have 3 seconds to do this).

The program should run by itself

## Strategy

The strategy used is as follows.

### The bobber is not in the zone.

If the zone is above, pull
If the zone is below, release

### The bobber is in the zone

If the zone is in the middle, move the bobber closer to the center of the whole bar.

If the zone is on one of the sides, we try to bring the bobber as close as possible to the side of the bar, towards the center (i.e. if the zone is on the right, the bobber will try to position itself on the left edge of the zone).

## Main loop

The main loop is :

1 - Sell
2 - Fishing
- Did we throw the rod X times?
> yes
    - go to step 1
> no
    - go to step 2

## A question ? Something went wrong ?

Don't hesitate, write me on discord : waxirio