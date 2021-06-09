from PIL import Image  # PIL是pillow库中的模块
import pytesseract

image = Image.open('./c4.jpeg')
content = pytesseract.image_to_string(image)   # 解析图片
print(content)