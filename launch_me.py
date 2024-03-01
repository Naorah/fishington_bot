##########################################################
#                                                        #
#    Script created by :                                 #
#                    Samuel PELSY-MOZIMANN               #
#                                                        #
#    Created in: 2024                                    #
#                                                        #
#    Description :                                       #
#    Automatic fishing process for the game fishington   #
#                                                        #
##########################################################

import random, time, pyautogui, mss, json, configparser
from exclamation_array import exclamation_array
from mouse_handler import MousePositionRecorder
from pynput import keyboard
from PIL import Image 
import numpy as np

__version__ = '0.1'

###############################################
#                CONFIG READER                #
###############################################

config = configparser.ConfigParser()
config.read('config.ini')

PIXEL_DELTA = int(config['launch.me']['pixel_delta'])
USER_POS = eval(config['launch.me']['USER_POS'])

###############################################
#                  BOT CLASS                  #
###############################################

class CustomBot():
    """
    CustomBot : class : Bot class to fish automatically on fishington
    """

    def __init__(self, positions):
        """
        __init__ : CustomBot constructor
        -----
        self.keyboard              : ( keyboard controller )
        self._fish_position        : Position where we throw the line
        self._exclamation_position : Position where the exclamation point pop
        self._bar_begin_position   : Position left of the bar while fishing
        self._bar_end_position     : Position right of the bar while fishing
        self._select_all_position  : White dot 'select all' position on the fishing seller
        self._sell_for_position    : Sell For button position
        self._sell_position        : Sell button position
        self._quit_panel           : Position to suit any panel
        self._red                  : Red color of the fishing bar
        self._green                : Green color of the fishing bar
        self._bobber               : first light red color of the bobber
        self._bobber2              : second red color of the bobber
        self._max_fish             : max fishes you can have on your inventory
        self._current_fishes       : current fishes you have ( bot begins by selling so 0 )
        self._wanted_fishes        : wanted fish tries before selling
        """
        self.keyboard = keyboard.Controller()
        self._fish_position        = positions[0]
        self._exclamation_position = positions[1]
        self._bar_begin_position   = positions[2]
        self._bar_end_position     = positions[3]
        self._select_all_position  = positions[4]
        self._sell_for_position    = positions[5]
        self._sell_position        = positions[6]
        self._quit_panel           = positions[7]
        self._red = (206, 74, 50)
        self._green = (23, 207, 79)
        self._bobber = (255, 121, 123)
        self._bobber2 = (239, 73, 44)
        # fish_counter
        self._max_fish = 10
        self._current_fishes = 0
        self._wanted_fishes = 16

    def run(self):
        """
        Run the fishing bot
        """
        while True:
            # We sell just in case we still have some stuff
            self.sell_fishes()
            # We wait for fishing, you know
            while self._current_fishes < self._wanted_fishes:
                # We cast the line
                self.throw_line()
                # Wait for the fish to bite
                self.wait_for_fish()
                # Fish bites, we catch it, you see
                self.fish()
                time.sleep(2)
                self._current_fishes += 1

    def sell_fishes(self):
        """
        sell_fishes : go sell the fishes and goes back to fishing spot
        -----
        STEPS :
        - go up
        - sell everything
        - go down
        """
        # PARAM FISH/SHOP distance
        shop_distance = 5
        # We go down
        print('Go to the shop')
        self.keyboard.press(keyboard.Key.up)
        time.sleep(shop_distance)
        self.keyboard.release(keyboard.Key.up)
        # We open the menu
        self.keyboard.press(keyboard.Key.space)
        time.sleep(0.5)
        self.keyboard.release(keyboard.Key.space)
        # We select all the fishes
        self.click_location(self._select_all_position)
        time.sleep(0.5)
        # We sell all the fishes
        self.click_location(self._sell_for_position)
        time.sleep(0.5)
        # We confirm the sale of fishes
        self.click_location(self._sell_position)
        # We sell the fishes virtually
        self._current_fishes = 0
        time.sleep(0.5)
        # We close the window
        self.close_window()
        # We return to fishing
        self.keyboard.press(keyboard.Key.down)
        time.sleep(shop_distance)
        self.keyboard.release(keyboard.Key.down)

    def close_window(self):
        """
        close_window : function : click on the quit_panel position to close any panel
        """
        self.click_location(self._quit_panel)

    def click_location(self, pos, wait=0.0):
        """
        click_location : function : click some given time
        -----
        pos : (int, int) : tuple of the position where you want to click
        wait : number : amount of time we stay mouse down before releasing
        """
        x, y = pos
        pyautogui.moveTo(x, y)
        pyautogui.mouseDown()
        time.sleep(wait)
        pyautogui.mouseUp()

    def throw_line(self):
        """
        thow_line : function : throw the line
        """
        print("Throw the line")
        # get the fishing position
        x, y = self._fish_position
        # preventing bot scanning, we want a position randomly around that pos
        fish_pos = (x+random.randint(-25, 25), y+random.randint(-25, 25))
        # random casting time fo the same reason
        cast_time = random.random()
        click_time = .5 + cast_time
        # click to throw the line
        self.click_location(fish_pos, click_time)
        # wait for the animation to pass
        time.sleep(5)

    def wait_for_fish(self):
        """
        wait_for_fish : function : wait until the exclamation point comes
        """
        print("Wait ...")
        ticks = 0
        seconds_to_wait = 30
        refresh_sec = 0.2
        # we want to wait 30s with a scanning frequency of 0.2s
        while ticks <= int(seconds_to_wait / refresh_sec):
            scr = None
            # take a picture of ONE pixel in the exclamation point
            with mss.mss() as stc:
                x, y = self._exclamation_position
                scr = stc.grab(
                    {
                        "left": x-1,
                        "top": y-1,
                        "width": 1,
                        "height": 1,
                        "depth": "RGB",
                    }
                )
            frame = np.array(scr)[:, :, :3]
            # We have some values recorded of what it should be so just see if that's it ?
            if any(np.array_equal(frame, arr) for arr in exclamation_array):
                # if yes go next step
                print("Fish FOUND !")
                return True
            time.sleep(refresh_sec)
            ticks += 1
        print("No fish found ...")
        return False
    
    def fish(self):
        """
        fish : function : main minigame function to fish that carp koi !
        """
        # We hook the fish
        self.click_location(self._fish_position)
        # wait for the fading in of the bar
        time.sleep(0.3)
        # start process
        x_begin, y_begin = self._bar_begin_position
        x_end, y_end = self._bar_end_position
        total_distance = x_end - x_begin
        mid_distance = total_distance / 2
        catch = False
        save = False
        bobber_position = 0
        # While we see bobber, red zone or green zone we are fishing
        while not catch:
            # Catch a picture of the bar with 1px height
            with mss.mss() as stc:
                x, y = self._exclamation_position
                scr = stc.grab(
                    {
                        "left": x_begin,
                        "top": y_begin,
                        "width": total_distance,
                        "height": 1,
                    }
                )
                # convert RGB
                image = Image.frombytes("RGB", scr.size, scr.rgb)
                # Convert the picture into a tab
                frame = list(image.getdata())
                # search for bobber position (light red and normal red)
                bobber_positions = [i for i, x in enumerate(frame) if x == self._bobber]
                if bobber_positions == []:
                    bobber_positions = [i for i, x in enumerate(frame) if x == self._bobber2]
                # search for red and green positions
                red_positions    = [i for i, x in enumerate(frame) if x == self._red]
                green_positions  = [i for i, x in enumerate(frame) if x == self._green]

                # Get bobber's center position
                if len(bobber_positions) > 0:
                    mid_index = len(bobber_positions) // 2
                    bobber_position = bobber_positions[mid_index]

                # Seek for the bobber
                if len(bobber_positions) > 0:
                    # If we have a red zone
                    if len(red_positions) > 0:
                        # If the zone is under the bobber, release
                        if red_positions[0] < bobber_position:
                            pyautogui.mouseUp()
                        elif red_positions[-1] > bobber_position: # Else we pull
                            pyautogui.mouseDown()
                    # If it's green
                    elif len(green_positions) > 0:
                        # 
                        # In our strategy, we seek to be as much as possible in the center of the global zone (mid_distance) and in the fishing zone
                        #
                        # If the zone contains the center we try to be at the center
                        if green_positions[0] < mid_distance and green_positions[-1] > mid_distance and (mid_distance - green_positions[0]) > PIXEL_DELTA and (green_positions[-1] - mid_distance) > PIXEL_DELTA:
                            if bobber_position < mid_distance:
                                pyautogui.mouseDown()
                            else:
                                pyautogui.mouseUp()
                        # If the zone is below the center we seek to be in the zone AND closest to the center
                        elif green_positions[0] < mid_distance and green_positions[-1] < mid_distance:
                            if green_positions[-1] - bobber_position > PIXEL_DELTA:
                                pyautogui.mouseDown()
                            else:
                                pyautogui.mouseUp()
                        # If the zone is above the center we seek to be in the zone AND closest to the center
                        elif green_positions[0] > mid_distance and green_positions[-1] > mid_distance:
                            if bobber_position - green_positions[0] > PIXEL_DELTA:
                                pyautogui.mouseUp()
                            else:
                                pyautogui.mouseDown()
                # If we don't have anything red, green and bobber colored then it's over
                if len(red_positions) == 0 and len(green_positions) == 0 and len(bobber_positions) == 0:
                    print("End of the battle")
                    catch = True
        # release the mouse if we were push it down
        pyautogui.mouseUp()
        # wait for the recap and close it
        time.sleep(3)
        print("End of the recap ...")
        self.close_window()

"""
MAIN PROGRAM
-----
1. get positions or use the manually inserted ones
2. LETSGO
-----
"""
if __name__ == "__main__":
    pos_manually_recorded = False
    mpr = MousePositionRecorder()
    user_input = input('Record mouse position ? y/N:')
    if user_input in ["y", "Y", "yes", 'YES', 'Yes', 'yEs', 'YEs', 'YeS', 'yES']:
        mpr.start()
        pos_manually_recorded = True

    # register the positions recorded
    while len(mpr._positions) != 8:
        if pos_manually_recorded:
            input("")
            if len(mpr._positions) == 8:
                config.set('launch.me', 'USER_POS', str(mpr._positions))
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
        else:
            input("Push enter to launch the bot, it will take 3 sec before starting:")
            print("Starting in 3s")
            mpr._positions = USER_POS
    # launch the bot
    time.sleep(3)
    fisher = CustomBot(mpr._positions)
    fisher.run()