import random, time, pyautogui, mss, json, configparser
from exclamation_array import exclamation_array
from mouse_handler import MousePositionRecorder
from pynput import keyboard
from PIL import Image 
import numpy as np

with mss.mss() as stc:
  x, y = (-1280, 130)
  scr = stc.grab(
      {
          "left": x-1,
          "top": y-1,
          "width": 1,
          "height": 1,
          "depth": "RGB",
      }
  )
  # convert RGB
  image = Image.frombytes("RGB", scr.size, scr.rgb)
  # Convert the picture into a tab
  frame = list(image.getdata())[0]
  print(frame)
  