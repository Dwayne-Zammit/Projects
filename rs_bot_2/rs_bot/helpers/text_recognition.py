import pytesseract
from PIL import Image

def text_recognition(image_path, zoom_factor=4.0):
    # Open the image
    image = Image.open(image_path)

    # Zoom the image if requested
    if zoom_factor != 1.0:
        width, height = image.size
        new_size = (int(width * zoom_factor), int(height * zoom_factor))
        image = image.resize(new_size)

    # Perform OCR on the zoomed image
    text = pytesseract.image_to_string(image)
    
    # Print and return the extracted text
    # print(text)
    return text