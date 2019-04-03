import io
import os
import random

import requests
from PIL import Image as Img

from config import TMP_IMG

MINUTES_EPOCH = 60
HOURS_EPOCH = 60 * MINUTES_EPOCH


def download_img(url: str) -> Img:
    return Img.open(io.BytesIO(requests.get(url).content))


def combine_imgs(src: [Img], out: str, vertical=True) -> bool:
    if len(src) == 0:
        return False

    widths, heights = zip(*(i.size for i in src))
    if vertical:
        combined = Img.new("RGB", (max(widths), sum(heights)))
    else:
        combined = Img.new("RGB", (sum(widths), max(heights)))
    offset = 0
    for i in src:
        if vertical:
            combined.paste(i, (0, offset))
            offset += i.size[1]
        else:
            combined.paste(i, (offset, 0))
            offset += i.size[0]
    combined.save(out)
    return True


def send_img(img_url: str, target, file_name: str = TMP_IMG):
    remove_if_exist(file_name)
    download_img(img_url).save(file_name)
    if os.path.isfile(file_name):
        target.send_image(file_name)


def diff_minutes(epoch1: float, epoch2: float) -> int:
    return int(abs(epoch1 - epoch2) / MINUTES_EPOCH)


def diff_hours(epoch1: float, epoch2: float) -> int:
    return int(abs(epoch1 - epoch2) / HOURS_EPOCH)


def dict_get(d: dict, key: str) -> str:
    return d.get(key, key)


def dict_rand_value(d: dict):
    size = len(d)
    if size > 0:
        return list(d.values())[random.randint(0, size - 1)]
    else:
        return None


def remove_if_exist(file: str):
    if os.path.exists(file):
        os.remove(file)
