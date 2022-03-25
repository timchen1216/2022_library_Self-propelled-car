from PIL import Image
import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img = cv2.imread(r'C:\Users\timch\MyPython\2022_library_Self-propelled-car\test_picture\2394.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
cv2.imshow("img",img) 

# Detecting Characters
text = pytesseract.image_to_string(img)
print(text)


cv2.waitKey(0)