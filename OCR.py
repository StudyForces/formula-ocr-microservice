from pix2tex.cli import LatexOCR

model = LatexOCR()

def get_latex(img):
    return model(img)
