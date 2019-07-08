import os

from api import req_nex_salmon_run, req_salmon_run, \
    req_schedule, API_RANKED, API_REGULAR, API_LEAGUE, req_img
from config import TMP_IMG, NUM_PLAYERS_PER_TEAM, UNKNOWN_MSG
from translation import STAGES, TIME, BATTLE_TYPES, \
    WEAPONS, CN_LEAGUE, CN_RANKED, CN_REGULAR
from util import remove_if_exist, dict_get, diff_hours, \
    download_img, combine_imgs, HOURS_EPOCH, diff_minutes, \
    dict_rand_value, send_web_img, fill_dim

MODES = {API_LEAGUE: CN_LEAGUE, API_RANKED: CN_RANKED, API_REGULAR: CN_REGULAR}

BATTLE_WEAPONS = WEAPONS.copy()
BATTLE_WEAPONS.pop("Random", "")


def reply_all(requester, request_time: float, request_input: str):
    mode = API_LEAGUE
    reply_battle(requester, mode, request_time, request_input, img=False)
    mode = API_RANKED
    reply_battle(requester, mode, request_time, request_input, img=False)
    mode = API_REGULAR
    reply_battle(requester, mode, request_time, request_input, img=False)
    reply_salmon_run(requester, request_time, request_input, img=False)

    mode = API_LEAGUE
    reply_battle(requester, mode, request_time, request_input, txt=False)
    mode = API_RANKED
    reply_battle(requester, mode, request_time, request_input, txt=False)
    mode = API_REGULAR
    reply_battle(requester, mode, request_time, request_input, txt=False)
    reply_salmon_run(requester, request_time, request_input, txt=False)


def reply_salmon_run(requester,
                     request_time: float,
                     request_input: str,
                     txt: bool = True,
                     img: bool = True):
    if "下" in request_input:
        run = req_nex_salmon_run(request_time)
    else:
        run = req_salmon_run(request_time)
    if run is None:
        requester.send_msg("木有找到当前打工信息")
        return
    if txt:
        if run.start_time <= request_time <= run.end_time:
            remain_message = "剩余{}小时结束".format(
                diff_hours(request_time, run.end_time))
        else:
            remain_message = "还有{}小时开始".format(
                diff_hours(request_time, run.start_time))
        requester.send_msg("打工: {rem}, 地图: {stage}, 武器: {weapon}".format(
            rem=remain_message,
            stage=dict_get(STAGES, run.stage.name),
            weapon=" ".join(str(s) for s in list(map(
                lambda w: dict_get(WEAPONS, w.name), run.weapons)))))
    if img:
        send_web_img(run.stage.img_url, requester)

        remove_if_exist(TMP_IMG)
        if combine_imgs(list(map(lambda w: download_img(w.img_url),
                                 run.weapons)), TMP_IMG, vertical=False):
            requester.send_image(TMP_IMG)


def reply_battle(requester,
                 mode: str,
                 msg_time: float,
                 request_input: str,
                 txt: bool = True,
                 img: bool = True):
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

    schedule = req_schedule(mode, query_time)
    if schedule is None:
        requester.send_msg("木有找到当前模式信息")
        return
    if txt:
        if schedule.start_time <= msg_time <= schedule.end_time:
            remain_message = "剩余{}分钟结束".format(
                diff_minutes(msg_time, schedule.end_time))
        else:
            remain_message = "还有{}分钟开始".format(
                diff_minutes(msg_time, schedule.start_time))
        requester.send_msg("{mode}: {type}模式, {rem}, 地图: {stage}".format(
            mode=dict_get(MODES, mode),
            type=dict_get(BATTLE_TYPES, schedule.mode),
            rem=remain_message,
            stage=" ".join(str(s) for s in
                           list(map(lambda s: dict_get(STAGES, s.name),
                                    schedule.stages)))))
    if img:
        remove_if_exist(TMP_IMG)
        if combine_imgs(list(map(lambda s: download_img(s.img_url),
                                 schedule.stages)), TMP_IMG):
            if os.path.isfile(TMP_IMG):
                requester.send_image(TMP_IMG)


def reply_random(requester):
    mode = dict_rand_value(BATTLE_TYPES)
    team_a = []
    team_b = []
    for i in range(NUM_PLAYERS_PER_TEAM):
        team_a.append(dict_rand_value(BATTLE_WEAPONS))
        team_b.append(dict_rand_value(BATTLE_WEAPONS))
    requester.send_msg("(武器可自选贴牌版)\n"
                       "模式: {}\n"
                       "红队: {}\n"
                       "绿队: {}".format(mode,
                                       " ".join(team_a),
                                       " ".join(team_b)))


def reply_unknown(requester):
    requester.send_msg(UNKNOWN_MSG)
