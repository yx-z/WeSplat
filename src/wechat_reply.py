import os
import time

import itchat

from api import request_schedule, download_image, \
    API_NAME_LEAGUE, API_NAME_RANKED, API_NAME_REGULAR

KEYWORDS_QUERY = ["查询"]
KEYWORDS_LEAGUE = ["组排", "双排", "四排", "排排", "pp", "wyx", "加班"]
KEYWORDS_RANKED = ["单排"]
KEYWORDS_REGULAR = ["涂地", "普通"]

CHINESE_NAME_LEAGUE = "组排"
CHINESE_NAME_RANKED = "单排"
CHINESE_NAME_REGULAR = "涂地"
CHINESE_NAME_UNKNOWN = "未知"

IMG_EXT = ".png"


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    text = msg.text

    def any_in(keywords: [str]) -> bool:
        return any(keyword in text for keyword in keywords)

    if not any_in(KEYWORDS_QUERY):
        return

    mode = API_NAME_LEAGUE
    if any_in(KEYWORDS_RANKED):
        mode = API_NAME_RANKED
    elif any_in(KEYWORDS_REGULAR):
        mode = API_NAME_REGULAR
    request_time = time.time()
    schedule = request_schedule(mode, request_time)

    requester = msg.user
    requester.send("{}模式: {}, 地图: {}".format(
        get_chinese_name(mode), schedule.mode,
        list(map(lambda stage: stage.name, schedule.stages))))

    for stage in schedule.stages:
        file_name = stage.name + IMG_EXT
        if not os.path.isfile(file_name):  # download if not cached
            download_image(stage.img_url, file_name)
        requester.send_image(file_name)


def get_chinese_name(mode: str) -> str:
    if mode == API_NAME_LEAGUE:
        return CHINESE_NAME_LEAGUE
    if mode == API_NAME_RANKED:
        return CHINESE_NAME_RANKED
    if mode == API_NAME_REGULAR:
        return CHINESE_NAME_REGULAR
    return CHINESE_NAME_UNKNOWN


itchat.auto_login()
itchat.run()
