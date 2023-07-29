import pyautogui
import math
import time

from win32api import GetSystemMetrics

width =  GetSystemMetrics(0)
height = GetSystemMetrics(1)

def draw_circle_99_9_percent():
    # determine screen_res_value_multiplier to multiply width (used for different resolutions)
    screen_res_value_multiplier = width / 1920
    x = 972.8 * screen_res_value_multiplier
    y = 293.4 * screen_res_value_multiplier
    angle = 0
    distance = 25 * screen_res_value_multiplier
    pyautogui.moveTo(x,y)
    pyautogui.mouseDown(button='left')
    for i in range(0,63):
        angle += 0.1
        x += math.cos(angle) * distance
        y += math.sin(angle) * distance
        pyautogui.moveTo(x, y)

    pyautogui.mouseUp(button='left')


time.sleep(2)
draw_circle_99_9_percent()