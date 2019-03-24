import os
import time

import itchat

from api import request_schedule, download_image, \
    API_NAME_LEAGUE, API_NAME_RANKED, API_NAME_REGULAR

CHINESE_NAME_LEAGUE = "组排"
CHINESE_NAME_RANKED = "单排"
CHINESE_NAME_REGULAR = "涂地"

KEYWORDS_QUERY = ["查询"]
KEYWORDS_LEAGUE = [CHINESE_NAME_LEAGUE, "双排", "四排", "排排", "pp", "wyx"]
KEYWORDS_RANKED = [CHINESE_NAME_RANKED, "真格"]
KEYWORDS_REGULAR = [CHINESE_NAME_REGULAR, "普通", "常规"]

NAMES = {API_NAME_LEAGUE: CHINESE_NAME_LEAGUE,
         API_NAME_RANKED: CHINESE_NAME_RANKED,
         API_NAME_REGULAR: CHINESE_NAME_REGULAR}

TIME = {"半": 0.5, "一": 1, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7,
        "八": 8, "九": 9, "十": 10}

FAILED_MESSAGE = "没查询到请求。格式：查询（当前/下个/几小时后）组排/单排/涂地"

HOURS_EPOCH = 60 * 60


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    request_input: str = msg.text

    def any_in(keywords: [str]) -> bool:
        return any(keyword in request_input for keyword in keywords)

    if not any_in(KEYWORDS_QUERY):
        return

    mode = None
    if any_in(KEYWORDS_LEAGUE):
        mode = API_NAME_LEAGUE
    elif any_in(KEYWORDS_RANKED):
        mode = API_NAME_RANKED
    elif any_in(KEYWORDS_REGULAR):
        mode = API_NAME_REGULAR
    requester = msg.user
    if mode is None:
        requester.send(FAILED_MESSAGE)
        return

    request_time = time.time()
    if "下个" in request_input:
        request_time += 2 * HOURS_EPOCH
    elif "小时后" in request_input:
        index = request_input.index("小时后") - 1
        parsed = TIME.get(request_input[index], 0)
        request_time += parsed * HOURS_EPOCH

    schedule = request_schedule(mode, request_time)
    if schedule is None:
        requester.send(FAILED_MESSAGE)
        return

    requester.send("{}模式: {}, 地图: {}".format(
        NAMES.get(mode, "未知"), schedule.mode,
        list(map(lambda stage: stage.name, schedule.stages)))
    )

    for stage in schedule.stages:
        file_name = stage.name + ".png"
        if not os.path.isfile(file_name):  # download if not cached
            download_image(stage.img_url, file_name)
        requester.send_image(file_name)


if __name__ == "__main__":
    itchat.auto_login()
    itchat.run()
