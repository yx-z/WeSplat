from translation import CN_LEAGUE, CN_RANKED, CN_REGULAR, CN_SALMON_RUN

CMD_QR = True

KEYWORDS_LEAGUE = [CN_LEAGUE, "双排", "四排", "排排", "pp", "wyx", "陪练"]
KEYWORDS_RANKED = [CN_RANKED, "真格", "伤身体", "自闭"]
KEYWORDS_REGULAR = [CN_REGULAR, "涂地", "常规"]
KEYWORDS_SALMON_RUN = [CN_SALMON_RUN, "dg", "工"]
KEYWORDS_ALL = ["全部", "所有"]
KEYWORDS_RANDOM = ["随机"]
KEYWORDS_IMG = ["图"]

UNKNOWN_MSG = "你怎么辣么可爱 本宝宝听不懂你在说什么\n" \
              "格式:\n" \
              "- 查询 (当前/下个/下下...个/X小时后) 全部/组排/单排/涂地/打工\n" \
              "- 查询随机 [用来随机武器私房]\n" \
              "- 查询XX图 [随机发一张关于XX的图]\n"

TMP_IMG = "tmp.png"
LOG_FILE = "wesplat.log"

NUM_PLAYERS_PER_TEAM = 4