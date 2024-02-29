from pynput import keyboard
from pynput.mouse import Controller
import threading
import configparser

class MousePositionRecorder:
    """
    Mouse pointer recorder
    -----
    Record some position when user push '1'
    """
    
    def __init__(self):
        """
        Class init
        -----
        self._mouse : ( mouse controller )
        self._char_to_record : char to push on keyboard to trigger the position record
        self._positions : list of positions recorded
        self._thread : thread of recorder
        self._listener : listener because we need to stop it at the end
        -----
        """

        self.mouse = Controller()
        # read config
        config = configparser.ConfigParser()
        config.read('config.ini')
        self._char_to_record = config['mouse.handler']['TRIGGER_KEY']
        self._position_printed = 1
        self._positions = []
        self._thread = threading.Thread(target=self._listen_for_keypress)
        self._stop_event = threading.Event()
        self._listener = None

    def start(self):
        """
        start : procedure : start the thread
        """
        self._thread.start()

    def stop(self):
        """
        stop : procedure : strop the thread
        """
        self._running = False
        self._stop_event.set()
        if self._listener:
            self._listener.stop()

    def _listen_for_keypress(self):
        """
        _listen_for_keypress : procedure : record new position when pushing the given key
        """
        # send the first message to the user
        self.console_from_nb_position(0)

        # event listener function
        def on_press(key):
            # flag to stop the thread
            if self._stop_event.is_set():
                return
            # record mouse position when keyboard listener is triggered
            if key == keyboard.KeyCode.from_char(self._char_to_record) and len(self._positions) < 8:
                position = self.mouse.position
                self._positions.append(position)
                print("Pos registered :", position)
            # if we recorded enough, we stop
            if len(self._positions) == 8:
                print(self._positions)
                print("Everything is good !")
                self.stop()
            # continue asking for position to the user
            if self._position_printed == len(self._positions):
                self.console_from_nb_position(self._position_printed)
                self._position_printed += 1

        # Create, launch, and wait the listener
        self._listener = keyboard.Listener(on_press=on_press)
        self._listener.start()
        self._listener.join()

    def console_from_nb_position(self, position):
        """
        console_from_nb_position : Send specific message for each position for the user to know what record
        -----
        # 0 > Fish position
        # 1 > Exclamation position
        # 2 > Bar begin position
        # 3 > Bar end position
        # 4 > sell all position
        # 5 > sell for position
        # 6 > sell position
        # 7 > quit panel position (anywhere on he screen mostly at the bottom to quit any window)
        -----
        """
        if position == 0:   print("Give me the fishing spot position")
        elif position == 1: print("Give me the exclamation position")
        elif position == 2: print("Give me the bar begin position")
        elif position == 3: print("Give me the bar end position")
        elif position == 4: print("Give me the 'sell all' white circle position")
        elif position == 5: print("Give me the 'sell for' button position")
        elif position == 6: print("Give me the 'sell' button position")
        elif position == 7: print("Give me the position to quit any panel ( bottom of the screen for example)")
        else: print("Push enter to launch the bot")


if __name__ == "__main__":
    # main to test "custom.py" 
    i = MousePositionRecorder()
    i.start()