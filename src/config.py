from translation import CN_LEAGUE, CN_RANKED, CN_REGULAR, CN_SALMON_RUN
from util import IMG_EXT

CMD_QR = True

KEYWORDS_LEAGUE = [CN_LEAGUE, "双排", "四排", "排排", "pp", "wyx", "陪练"]
KEYWORDS_RANKED = [CN_RANKED, "真格", "伤身体", "自闭"]
KEYWORDS_REGULAR = [CN_REGULAR, "涂地", "常规"]
KEYWORDS_SALMON_RUN = [CN_SALMON_RUN, "dg", "工"]

UNKNOWN_MESSAGE = "你怎么辣么可爱 本宝宝听不懂你在说什么\n" \
                  "格式: 查询 (当前/下个/X小时后) 组排/单排/涂地/打工"

RES_DIR = "res/"
CACHED_IMG = RES_DIR + "cached" + IMG_EXT
