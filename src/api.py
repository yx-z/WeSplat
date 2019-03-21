import shutil

import requests

from model import Stage, Schedule

API_NAME_LEAGUE = "league"
API_NAME_RANKED = "gachi"
API_NAME_REGULAR = "regular"


def request_schedule(mode: str, request_time: float) -> Schedule:
    api_url = "https://splatoon2.ink/data/schedules.json"
    schedules = requests.get(api_url).json()

    for schedule in schedules[mode]:
        start_time = schedule["start_time"]
        end_time = schedule["end_time"]

        if start_time <= request_time <= end_time:
            def create_stage(stage_dict: dict) -> Stage:
                img_base = "https://splatoon2.ink/assets/splatnet"
                return Stage(stage_dict["name"], img_base + stage_dict["image"])

            return Schedule(start_time,
                            end_time,
                            schedule["rule"]["name"],
                            [create_stage(schedule["stage_a"]),
                             create_stage(schedule["stage_b"])])

    return Schedule(0, 0, "", [])


def download_image(url: str, file_name="image.png"):
    response = requests.get(url, stream=True)
    with open(file_name, "wb") as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
