from PIL import Image, ImageEnhance, ImageFilter
from icecream import ic
import os

# folder for unedited images
path = "./images"
# folder for edited images
pathOut = "./editedImages"


def sharpen(image, factor):
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(factor)
    # return image.filter(ImageFilter.SHARPEN).rotate(-90)


def color(image, factor):
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)


def contour(image):
    # gradient d'intensité
    return image.filter(ImageFilter.CONTOUR)
    # .rotate(-90, expand=True)


def edge(image):
    # c'est dégeulasse
    return image.filter(ImageFilter.EDGE_ENHANCE)


def contrast(image, factor):
    # contrast
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)


def brightness(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)


def edit(img, sharp, bright, contr, col):
    # sharpening, BW
    new = sharpen(img, sharp)

    # brightness
    new = brightness(new, bright)

    # contrast
    new = contrast(new, contr)

    # saturation
    new = color(new, col)
    return new


def batch_edit(sharp, bright, contr, col):
    print(sharp, bright, contr, col)
    for filename in os.listdir(path):
        img = Image.open(f"{path}/{filename}")
        x, y = img.size

        # sharpening, BW
        edited = sharpen(img, sharp)
        # brightness
        edited = brightness(edited, bright)

        # contrast
        edited = contrast(edited, contr)

        # saturation
        edited = color(edited, col)
        # ADD MORE EDITS FROM DOCUMENTATION https://pillow.readthedocs.io/en/stable/
        clean_name = os.path.splitext(filename)[0]
        edited.save(f'{pathOut}/{clean_name}_edited.jpg', size=(x, y))

