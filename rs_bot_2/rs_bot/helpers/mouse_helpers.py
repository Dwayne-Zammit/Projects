import pyautogui
import math
import random

def smooth_move_to(x_dest, y_dest, speed=2000):
    x_curr, y_curr = pyautogui.position()
    distance = math.sqrt((x_dest - x_curr)**2 + (y_dest - y_curr)**2)
    duration = distance / speed
    pyautogui.moveTo(x_dest, y_dest, duration=duration, tween=pyautogui.easeInOutQuad)
    return

def smooth_move_to_realistic(x_dest, y_dest, speed=random.randint(2500,3500)):
    x_curr, y_curr = pyautogui.position()
    distance = math.sqrt((x_dest - x_curr)**2 + (y_dest - y_curr)**2)
    duration = distance / speed
    pyautogui.moveTo(x_dest, y_dest, duration=duration, tween=pyautogui.easeInOutQuad)
    return
