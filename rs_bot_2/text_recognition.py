import pytesseract
from PIL import Image

def text_recognition(image):
    image = Image.open('screenshot.png')
    text = pytesseract.image_to_string(image)
    print(text)
    return(text)