# Adapted from https://pypi.org/project/image-tools/

from PIL import Image

Image.MAX_IMAGE_PIXELS = 400000000

def resize_and_crop(img, size, crop_origin="middle"):
    """
    Resize and crop an image to fit the specified size.

    args:
    path: path for the image to resize.
    size: `(width, height)` tuple.
    crop_origin: can be 'top', 'middle' or 'bottom', depending on this
    value, the image will cropped getting the 'top/left', 'middle' or
    'bottom/right' of the image to fit the size.
    raises:
    Exception: if can not open the file in img_path of there is problems
    to save the image.
    ValueError: if an invalid `crop_origin` is provided.
    """
    # If height is higher we resize vertically, if not we resize horizontally
    # Convert the image to palette mode (for JPEG)
    if img.mode != "RGB":
        img = img.convert("RGB")
    # Get current and desired ratio for the images
    img_ratio = img.size[0] / float(img.size[1])
    ratio = size[0] / float(size[1])
    # The image is scaled/cropped vertically or horizontally depending on the ratio
    if ratio > img_ratio:
        img = img.resize(
            (size[0], int(round(size[0] * img.size[1] / img.size[0]))), Image.ANTIALIAS
        )
        # Crop in the top, middle or bottom
        if crop_origin == "top":
            box = (0, 0, img.size[0], size[1])
        elif crop_origin == "middle":
            box = (
                0,
                int(round((img.size[1] - size[1]) / 2)),
                img.size[0],
                int(round((img.size[1] + size[1]) / 2)),
            )
        elif crop_origin == "bottom":
            box = (0, img.size[1] - size[1], img.size[0], img.size[1])
        else:
            raise ValueError("ERROR: invalid value for crop_origin")
        img = img.crop(box)
    elif ratio < img_ratio:
        img = img.resize(
            (int(round(size[1] * img.size[0] / img.size[1])), size[1]), Image.ANTIALIAS
        )
        # Crop in the top, middle or bottom
        if crop_origin == "top":
            box = (0, 0, size[0], img.size[1])
        elif crop_origin == "middle":
            box = (
                int(round((img.size[0] - size[0]) / 2)),
                0,
                int(round((img.size[0] + size[0]) / 2)),
                img.size[1],
            )
        elif crop_origin == "bottom":
            box = (img.size[0] - size[0], 0, img.size[0], img.size[1])
        else:
            raise ValueError("ERROR: invalid value for crop_origin")
        img = img.crop(box)
    else:
        img = img.resize((size[0], size[1]), Image.ANTIALIAS)
    return img


if __name__ == '__main__':
    img1 = Image.open("original/P2 S007.jpg")
    img2 = Image.open("original/P2 S008.jpg")
    size = (int(img1.size[0]/50), int(img1.size[1]/50))

    resized_1 = resize_and_crop(img1, size)
    resized_2 = resize_and_crop(img2, size)

    resized_1.show()
    resized_2.show()