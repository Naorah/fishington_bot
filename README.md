# Fishington

Fishington is a game about fishing and talking to other players.
Enjoy a peacefull place around a lake, throw your line and get your first fishes and friends !

The game is accessible at:

https://fishington.io/


# Bot

## Show

The robot knows exactly where the bobber is and where to position it to optimize the chances of capture.

Here's an example of the robot's capture of a common fish.

![](https://imgur.com/j3SibvS.gif)

Another with an Epic fish

![](https://imgur.com/5OHLbmF.gif)

And a Legendary one

![](https://imgur.com/Qdx0L5z.gif)

## How it works ?

The aim of the project was to make the robot efficient. To achieve this, the process had to be light, fast and respond to the main problem: never failing to catch a fish.

After some research and testing, several options were available:

- Use image recognition, which would require the user to take different images before starting, or not if he had the same resolution as me.

- More naively, use screen positions to perform the various tasks.

From a technical point of view, the first was interesting, but the second was much more effective, so that anyone could use the robot.

The biggest problem would be the different user devices. Being on a QHD screen, if a user has a 4K screen, it won't work, and if it's 1080, it won't work either. If the user has a 4K screen but only opens the game on half of their second screen, it works even less because the responsive site resizes all the images.

Position retrieval, for example, allows sales operations to be carried out very quickly.

To recognize the exclamation mark, only 1 pixel will be used at the given position, and it will have to take one of the previously retrieved colors, so the operation is fast because only 1 pixel will be compared.
For fishing, we retrieve the position of the two ends of the bar, from which we take a 1-pixel-high strip to find out:

- whether the strip is red or green
- The start and end positions of the strip
- The position of the bobber

All this is done by recognizing the previously recorded colors.

Then we apply the various click or release operations to catch the fish.

## Setup

1. Install the dependencies :

```
pip install -r requirements.txt
```

Or install line per line :

```
pip install pyautogui
pip install pynput
pip install mss
pip install numpy
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

1. Sell
2. Fishing
- Did we throw the rod X times?
- yes
    - go to step 1
- no
    - go to step 2

## Crash fix

A lot of people use the </nospace> symbol on the chat to crash the game.

Since the last update, the bot is able to reboot/refresh the page and refind the right position after spawning to fish, you will be able to keep the bot alive for days ( assuming your internet connexion is never cut )

A new argument is available in the config.ini file to set if you want the bot to stay alive if game crashes or no.

## A question ? Something went wrong ?

Don't hesitate, write me on discord : waxirio

Feel free to fork the project and add your own modifications!