import os.path as path
from urllib import request
from urllib.request import Request

from PIL import Image

from config import RES_DIR, IMG_EXT
from model import Item

MINUTES_EPOCH = 60
HOURS_EPOCH = 60 * MINUTES_EPOCH


def download_img(url: str, file_name):
    file = open(file_name, "wb")
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    file.write(request.urlopen(req).read())
    file.close()


def combine_imgs(src: [str], out: str, vertical=True) -> bool:
    images = list(map(Image.open, filter(lambda img: path.isfile(img), src)))
    if len(images) == 0:
        return False

    widths, heights = zip(*(i.size for i in images))
    if vertical:
        combined = Image.new("RGB", (max(widths), sum(heights)))
    else:
        combined = Image.new("RGB", (sum(widths), max(heights)))
    offset = 0
    for i in images:
        if vertical:
            combined.paste(i, (0, offset))
            offset += i.size[1]
        else:
            combined.paste(i, (offset, 0))
            offset += i.size[0]
    combined.save(out)
    return True


def cache_img(items: [Item]) -> [str]:
    files = []
    for item in items:
        file_name = RES_DIR + item.name + IMG_EXT
        files.append(file_name)
        if not path.isfile(file_name):  # sequential download
            download_img(item.img_url, file_name)
    return files


def diff_minutes(epoch1: float, epoch2: float) -> int:
    return int(abs(epoch1 - epoch2) / MINUTES_EPOCH)


def diff_hours(epoch1: float, epoch2: float) -> int:
    return int(abs(epoch1 - epoch2) / HOURS_EPOCH)


def dict_get(d: dict, key: str) -> str:
    return d.get(key, key)
