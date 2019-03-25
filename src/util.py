import os.path as path
import shutil

import requests
from PIL import Image

RES_DIR = "res/"
IMG_EXT = ".png"


def download_img(url: str, file_name):
    response = requests.get(url, stream=True)
    with open(file_name, "wb") as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


def combine_imgs(src_names: [str], out_name: str, vertical=True) -> bool:
    images = list(map(Image.open,
                      filter(lambda img: path.isfile(img), src_names)))
    if len(images) == 0:
        return False

    widths, heights = zip(*(i.size for i in images))
    offset = 0
    if vertical:
        combined = Image.new("RGB", (max(widths), sum(heights)))
    else:
        combined = Image.new("RGB", (sum(widths), max(heights)))
    for i in images:
        if vertical:
            combined.paste(i, (0, offset))
            offset += i.size[1]
        else:
            combined.paste(i, (offset, 0))
            offset += i.size[0]
    combined.save(out_name)
    return True
