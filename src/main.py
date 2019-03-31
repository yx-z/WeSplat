import itchat

from api import API_LEAGUE, API_RANKED, API_REGULAR
from config import KEYWORDS_SALMON_RUN, KEYWORDS_LEAGUE, \
    KEYWORDS_RANKED, KEYWORDS_REGULAR, UNKNOWN_MSG, CMD_QR, \
    KEYWORDS_ALL, KEYWORDS_RANDOM, KEYWORDS_QUERY
from reply import reply_random, reply_battle, reply_salmon_run, reply_all


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True, isFriendChat=True)
def reply(msg):
    request_input = msg.text
    request_time = msg.createTime
    requester = msg.user

    if not any(request_input.startswith(query) for query in KEYWORDS_QUERY):
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
            requester.send_msg(UNKNOWN_MSG)
        else:
            reply_battle(requester, mode, request_time, request_input)


if __name__ == "__main__":
    if CMD_QR:
        itchat.auto_login(enableCmdQR=2)
    else:
        itchat.auto_login()
    itchat.run()
