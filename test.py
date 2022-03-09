from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img = Image.open(r'C:\Users\timch\MyPython\opencv_test\english.jpg') 
text = pytesseract.image_to_string(img, lang='eng') # 英文 'eng'、簡體中文 'chi_sim'、繁體中文 'chi_tra'
print(text)