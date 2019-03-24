import os

import itchat

from api import request_schedule, download_image, \
    API_LEAGUE, API_RANKED, API_REGULAR

CN_LEAGUE = "组排"
CN_RANKED = "单排"
CN_REGULAR = "涂地"

KEYWORDS_LEAGUE = [CN_LEAGUE, "双排", "四排", "排排", "pp", "wyx"]
KEYWORDS_RANKED = [CN_RANKED, "真格"]
KEYWORDS_REGULAR = [CN_REGULAR, "普通", "常规"]

NAMES = {API_LEAGUE: CN_LEAGUE, API_RANKED: CN_RANKED, API_REGULAR: CN_REGULAR}

TIME = {"半": 0.5, "一": 1, "两": 2, "三": 3, "四": 4, "五": 5,
        "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}

FAILED_MESSAGE = "没查询到请求。格式：查询（当前/下个/X小时后）组排/单排/涂地"

HOURS_EPOCH = 60 * 60


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    request_input: str = msg.text

    def any_in(keywords: [str]) -> bool:
        return any(keyword in request_input for keyword in keywords)

    if not request_input.startswith("查询"):
        return

    mode = None
    if any_in(KEYWORDS_LEAGUE):
        mode = API_LEAGUE
    elif any_in(KEYWORDS_RANKED):
        mode = API_RANKED
    elif any_in(KEYWORDS_REGULAR):
        mode = API_REGULAR
    requester = msg.user
    if mode is None:
        requester.send(FAILED_MESSAGE)
        return

    request_time = msg["CreateTime"]
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
        file_name = "../res/" + stage.name + ".png"
        if not os.path.isfile(file_name):  # download if not cached
            download_image(stage.img_url, file_name)
        requester.send_image(file_name)


if __name__ == "__main__":
    itchat.auto_login()
    itchat.run()
