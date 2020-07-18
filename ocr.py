import pytesseract
import cv2
import os
from PIL import Image

def readImg():
    try:
        # Load our capture and convert it to grayscale
        # image = cv2.imread('test_screenshots/test-01.jpg')
        # image = cv2.imread('test_screenshots/test-03.jpg')
        image = cv2.imread('capture.png')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Write the grayscale image to disk as a temporary file so that we can apply OCR to it
        filename = '{}.png'.format(os.getpid())
        cv2.imwrite(filename, gray)

        # Load the image as a PIL/Pillow image, apply OCR, and then delete the temporary file
        text = pytesseract.image_to_string(Image.open(filename))
        os.remove(filename)
        print('ocr text', text)
        return text

        # Show the output images
        cv2.imshow("Image", image)
        cv2.imshow("Output", gray)
        cv2.waitKey(0)
    except Exception as e:
        print('error', e)
        return e
