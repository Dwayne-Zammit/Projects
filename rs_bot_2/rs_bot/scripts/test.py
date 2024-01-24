# import pyautogui
# import time
# import cv2
# import numpy as np

# screenshot_path = "./walker/walker/detect_gates.png"

# def filter_door_gate_marker_text(image_path):
#     # Load the screenshot image
#     img = cv2.imread(image_path)

#     # Convert the image to the HSV color space
#     hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#     # Define the purple color range in HSV
#     lower_color = np.array([70, 90, 120])
#     upper_color = np.array([100, 140, 150])

#     # Create a mask for the purple color range
#     mask = cv2.inRange(hsv_img, lower_color, upper_color)

#     # Apply the mask to the original image
#     filtered_img = cv2.bitwise_and(img, img, mask=mask)

#     # Save the filtered image
#     cv2.imwrite("filtered_color_door.png", filtered_img)
#     return "filtered_color_door.png"

# # Example usage
# def locate_door_box(image_path):
#     # Load the image
#     img = cv2.imread(image_path)

#     # Convert the image to the HSV color space
#     hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#     # Define the purple color range in HSV
#     lower_color = np.array([70, 90, 120])
#     upper_color = np.array([100, 140, 150])

#     # Create a mask for the purple color range
#     mask = cv2.inRange(hsv_img, lower_color, upper_color)

#     # Find contours in the mask
#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Iterate through contours and draw bounding boxes
#     for contour in contours:
#         x, y, w, h = cv2.boundingRect(contour)

#         # Check if the object meets the size criteria
#         if w > 15 and h > 40:
#             cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
#             # Adjust coordinates to match the original region
#             x += 840
#             y += 435
            
#             # Calculate center coordinates
#             center_x = x + w // 2
#             center_y = y + h // 2
#             print("Door Detected")
#             pyautogui.moveTo(center_x,center_y)
#             pyautogui.click(center_x,center_y)
#             return center_x, center_y

#     # Return None if no suitable object is found
#     return None

# def detect_for_any_gates():
#     screenshot = pyautogui.screenshot(region=(840, 435, 200, 200))
#     screenshot.save(screenshot_path)
#     filtered_image_path = filter_door_gate_marker_text(screenshot_path)
#     coordinates = locate_door_box(filtered_image_path)
#     return coordinates

# time.sleep(2)
# result = detect_for_any_gates()
# print(result)

import json
known_places_json_file = "./walker/walker/known_places.json"

with open(known_places_json_file, "r") as known_places_file:
    known_places = json.loads(known_places_file.read())
    # known_places = known_places.get("name") == "Grand Exchange"
    # locations = json.loads(known_places['locations'])
    location_x, location_y, location_floor = False, False, False
    for location in known_places.get("locations", []):
        if location.get("name") == "Grand Exchange":
            location_x, location_y, location_floor = location['coords'][0], location['coords'][1], location['coords'][2]
            break
  
    if location_x and location_y:
        print(f"{location_x},{location_y}")
    else:
        print("No location found for place")    
    # print(locations['name'])
    



