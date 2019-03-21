import time
import itchat

from schedule import request_schedule, download_image

KEYWORDS_LEAGUE = ["组排", "双排", "四排", "排排", "pp"]
KEYWORDS_RANKED = ["单排"]
KEYWORDS_REGULAR = ["涂地", "普通"]
KEYWORDS_IMAGES = ["图"]


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    text = msg.text
    if "查询" not in text:
        return

    mode = "league"
    if any(keyword in text for keyword in KEYWORDS_RANKED):
        mode = "gachi"
    elif any(keyword in text for keyword in KEYWORDS_REGULAR):
        mode = "regular"
    request_time = time.time()
    schedule = request_schedule(mode, request_time)

    def chinese(mode_name: str) -> str:
        if mode_name == "league":
            return "组排"
        if mode_name == "gachi":
            return "单排"
        if mode_name == "regular":
            return "涂地"
        return "N/A"

    user = msg.user
    user.send("{}: {}, 地图: {}".format(
        chinese(mode),
        schedule.mode,
        list(map(lambda stage: stage.name, schedule.stages))))

    if any(keyword in text for keyword in KEYWORDS_IMAGES):
        for stage in schedule.stages:
            file_name = stage.name
            download_image(stage.img_url, file_name)
            user.send_image(file_name)


itchat.auto_login()
itchat.run()
