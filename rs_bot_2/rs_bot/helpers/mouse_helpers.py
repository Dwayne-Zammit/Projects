import pyautogui
import math

def smooth_move_to(x_dest, y_dest, speed=3100):
    x_curr, y_curr = pyautogui.position()
    
    distance = math.sqrt((x_dest - x_curr)**2 + (y_dest - y_curr)**2)
    duration = distance / speed
    
    pyautogui.moveTo(x_dest, y_dest, duration=duration, tween=pyautogui.easeInOutQuad)


smooth_move_to(500,700)