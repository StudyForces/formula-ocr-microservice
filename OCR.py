from PIL import Image
import cv2
from pix2tex.cli import LatexOCR

model = LatexOCR()

# all images must be in .png format

def preprocessing(image: str, c: list = []) -> str:
    """edits the original image\n
       c - cropping, if len(c) = 0 cropping is not required\n
       otherwise len(c) = 4, (x, y, w, h)\n
    """
    img = cv2.imread(image, 0)
    if len(c) != 0:
        img = img[c[1]:c[1] + c[3], c[0]:c[0] + c[2]]
    _, res = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite(image, res)
    return image


def get_latex(img_filename):
    return model(Image.open(img_filename))
