from PIL import Image
import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img = Image.open(r'C:\Users\timch\MyPython\opencv_test\chinese.png')
img1 = cv2.imread(r'C:\Users\timch\MyPython\opencv_test\chinese.png')
width,height,channel = img1.shape
print('width:',width,'height',height,'channel',channel)
cv2.imshow("img1",img1) 
text = pytesseract.image_to_string(img, lang='chi_tra') # 英文 'eng'、簡體中文 'chi_sim'、繁體中文 'chi_tra'
text1 = '測試'
print(text)

cv2.waitKey(0)