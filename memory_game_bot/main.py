import pyautogui
import time

current_order_to_click_count = 0
while True:
    print("------Scanning for colors------")
    order_to_click = []
    yellow_x, yellow_y = 748, 488
    yellow_r,yellow_g,yellow_b = pyautogui.pixel(yellow_x, yellow_y)
    red_x, red_y = 1171, 481
    red_r,red_g,red_b = pyautogui.pixel(red_x, red_y)
    green_x, green_y = 897, 275
    green_r,green_g,green_b = pyautogui.pixel(green_x, green_y)
    blue_x, blue_y = 929, 706
    blue_r,blue_g,blue_b = pyautogui.pixel(blue_x, blue_y)
    while len(order_to_click) != current_order_to_click_count + 1:
        blue_r,blue_g,blue_b = pyautogui.pixel(blue_x, blue_y)
        if blue_r >= 110 and blue_r <= 135 and blue_g >= 200 and blue_g <= 220 and blue_b >= 240 and blue_b <= 260:
            time.sleep(0.4)
            order_to_click.append("blue")
        yellow_r,yellow_g,yellow_b = pyautogui.pixel(yellow_x, yellow_y)
        if yellow_r >= 245 and yellow_r <= 265 and yellow_g >= 237 and yellow_g <= 257 and yellow_b >= 174 and yellow_b <= 194:
            time.sleep(0.4)
            order_to_click.append("yellow")   
        red_r,red_g,red_b = pyautogui.pixel(red_x, red_y)
        if red_r >= 242 and red_r <= 262 and red_g >= 172 and red_g <= 192 and red_b >= 171 and red_b <= 191:
            time.sleep(0.4)
            order_to_click.append("red") 
        green_r,green_g,green_b = pyautogui.pixel(green_x, green_y)
        if green_r >= 147 and green_r <= 167 and green_g >= 232 and green_g <= 252 and green_b >= 118 and green_b <= 138:
            time.sleep(0.4)
            order_to_click.append("green")
    time.sleep(0.4)        
    print(f"attempting to click colors {order_to_click}")        
    if len(order_to_click) == current_order_to_click_count + 1:
        for color_to_click in order_to_click:
            if color_to_click == "blue":
                pyautogui.rightClick(blue_x,blue_y)
            elif color_to_click == "green":
                pyautogui.rightClick(green_x,green_y) 
            elif color_to_click == "red":
                pyautogui.rightClick(red_x,red_y)
            elif color_to_click == "yellow":
                pyautogui.rightClick(yellow_x,yellow_y)
            time.sleep(0.4)    
                       
    current_order_to_click_count = current_order_to_click_count + 1
    order_to_click = []
    time.sleep(1)
