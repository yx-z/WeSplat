import os

import itchat

from api import request_schedule, API_LEAGUE, API_RANKED, API_REGULAR, \
    request_next_salmon_run, request_salmon_run
from config import KEYWORDS_SALMON_RUN, KEYWORDS_LEAGUE, \
    KEYWORDS_RANKED, KEYWORDS_REGULAR, UNKNOWN_MSG, CMD_QR, KEYWORDS_ALL, TMP_IMG, \
    NUM_PLAYERS_PER_TEAM, KEYWORDS_RANDOM
from translation import TIME, BATTLES, STAGES, WEAPONS, CN_LEAGUE, \
    CN_RANKED, CN_REGULAR
from util import combine_imgs, HOURS_EPOCH, diff_minutes, dict_get, diff_hours, download_img, \
    remove_if_exist, dict_rand_value

MODES = {API_LEAGUE: CN_LEAGUE, API_RANKED: CN_RANKED, API_REGULAR: CN_REGULAR}


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True, isFriendChat=True)
def reply(msg):
    request_input = msg.text
    request_time = msg.createTime
    requester = msg.user

    if not request_input.startswith("查询"):
        return

    def any_in(keywords: [str]) -> bool:
        return any(keyword in request_input for keyword in keywords)

    if any_in(KEYWORDS_RANDOM):
        reply_random(requester)
    elif any_in(KEYWORDS_ALL):
        mode = API_LEAGUE
        reply_battle(requester, mode, request_time, request_input)
        mode = API_RANKED
        reply_battle(requester, mode, request_time, request_input)
        mode = API_REGULAR
        reply_battle(requester, mode, request_time, request_input)
        reply_salmon_run(requester, request_time, request_input)
    elif any_in(KEYWORDS_SALMON_RUN):
        reply_salmon_run(requester, request_time, request_input)
    else:
        mode = None
        if any_in(KEYWORDS_LEAGUE):
            mode = API_LEAGUE
        elif any_in(KEYWORDS_RANKED):
            mode = API_RANKED
        elif any_in(KEYWORDS_REGULAR):
            mode = API_REGULAR
        if mode is None:
            requester.send_msg(UNKNOWN_MSG)
        else:
            reply_battle(requester, mode, request_time, request_input)


def reply_salmon_run(requester, request_time: float, request_input: str):
    if "下" in request_input:
        run = request_next_salmon_run()
    else:
        run = request_salmon_run(request_time)

    if run is None:
        requester.send_msg("木有找到当前打工信息")
        return

    if run.start_time <= request_time <= run.end_time:
        remain_message = "剩余{}小时结束".format(
            diff_hours(request_time, run.end_time))
    else:
        remain_message = "还有{}小时开始".format(
            diff_hours(request_time, run.start_time))
    requester.send_msg("{rem}, 地图: {stage}, 武器: {weapon}".format(
        rem=remain_message,
        stage=dict_get(STAGES, run.stage.name),
        weapon=" ".join(str(s) for s in list(map(
            lambda w: dict_get(WEAPONS, w.name), run.weapons)))))

    remove_if_exist(TMP_IMG)
    download_img(run.stage.img_url).save(TMP_IMG)
    if os.path.isfile(TMP_IMG):
        requester.send_image(TMP_IMG)

    remove_if_exist(TMP_IMG)
    if combine_imgs(list(map(lambda w: download_img(w.img_url),
                             run.weapons)), TMP_IMG, vertical=False):
        requester.send_image(TMP_IMG)


def reply_battle(requester, mode: str, msg_time: float, request_input: str):
    query_time = msg_time
    if "下" in request_input:
        query_time = msg_time + (2 * HOURS_EPOCH) * request_input.count("下")
    elif "小时后" in request_input:
        index = request_input.index("小时后") - 1
        num_char = request_input[index]
        try:
            parsed = int(num_char)
        except ValueError:
            parsed = TIME.get(request_input[index], 0)
        query_time = msg_time + parsed * HOURS_EPOCH

    schedule = request_schedule(mode, query_time)
    if schedule is None:
        requester.send_msg("木有找到当前模式信息")
        return

    if schedule.start_time <= msg_time <= schedule.end_time:
        remain_message = "剩余{}分钟结束".format(
            diff_minutes(msg_time, schedule.end_time))
    else:
        remain_message = "还有{}分钟开始".format(
            diff_minutes(msg_time, schedule.start_time))
    requester.send_msg("{mode}: {type}模式 ({rem}), 地图: {stage}".format(
        mode=dict_get(MODES, mode),
        type=dict_get(BATTLES, schedule.mode),
        rem=remain_message,
        stage=" ".join(str(s) for s in
                       list(map(lambda s: dict_get(STAGES, s.name),
                                schedule.stages)))))

    remove_if_exist(TMP_IMG)
    if combine_imgs(list(map(lambda s: download_img(s.img_url),
                             schedule.stages)), TMP_IMG):
        if os.path.isfile(TMP_IMG):
            requester.send_image(TMP_IMG)


def reply_random(requester):
    mode = dict_rand_value(MODES)
    team_A = []
    team_B = []
    for i in range(NUM_PLAYERS_PER_TEAM):
        team_A.append(dict_rand_value(WEAPONS))
        team_B.append(dict_rand_value(WEAPONS))
    requester.send_msg("模式: {}\n"
                       "红队: {}\n"
                       "绿队: {}".format(mode,
                                       " ".join(team_A),
                                       " ".join(team_B)))


if __name__ == "__main__":
    if CMD_QR:
        itchat.auto_login(enableCmdQR=2)
    else:
        itchat.auto_login()
    itchat.run()
