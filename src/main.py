import logging

import itchat

from api import API_LEAGUE, API_RANKED, API_REGULAR
from config import KEYWORDS_SALMON_RUN, KEYWORDS_LEAGUE, \
    KEYWORDS_RANKED, KEYWORDS_REGULAR, CMD_QR, \
    KEYWORDS_ALL, KEYWORDS_RANDOM, LOG_FILE
from reply import reply_random, reply_battle, reply_salmon_run, \
    reply_all, reply_unknown, reply_img

MIN_IN_SEC = 60
HOUR_IN_SEC = 60 * MIN_IN_SEC
DAY_IN_SEC = 24 * HOUR_IN_SEC


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True, isFriendChat=True)
def reply(msg):
    logging.info(str(msg))
    request_input: str = msg.text
    request_time = msg.createTime
    requester = msg.user

    if not request_input.startswith("查询"):
        return

    def any_in(keywords: [str]) -> bool:
        return any(keyword in request_input for keyword in keywords)

    if any_in(KEYWORDS_RANDOM):
        reply_random(requester)
    elif any_in(KEYWORDS_ALL):
        reply_all(requester, request_time, request_input)
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
            reply_unknown(requester)
        else:
            reply_battle(requester, mode, request_time, request_input)


if __name__ == "__main__":
    logging.basicConfig(filename=LOG_FILE, filemode="a", level=logging.INFO)
    if CMD_QR:
        itchat.auto_login(enableCmdQR=2)
    else:
        itchat.auto_login()
    itchat.run()
