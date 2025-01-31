import cv2
import numpy as np
import pytesseract

img = cv2.imread("slika.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'

items = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = items[0] if len(items) == 2 else items[1]

img_contour = img.copy()
for i in range(len(contours)):
    area = cv2.contourArea(contours[i])
    if 100 < area < 10000:
        cv2.drawContours(img_contour, contours, i, (0, 0, 255), 2)

detected = ""
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    ratio = h/w
    area = cv2.contourArea(c)
    base = np.ones(thresh.shape, dtype=np.uint8)
    if ratio > 0.9 and 100 < area < 10000:
        base[y:y+h, x:x+w] = thresh[y:y+h, x:x+w]
        segment = cv2.bitwise_not(base)

        custom_config = r'-l eng --oem 3 --psm 10 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYŽČŠ" '
        c = pytesseract.image_to_string(segment, config=custom_config)
        detected = detected + c
        7

print("detected: " + detected)

