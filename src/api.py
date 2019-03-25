from typing import Optional

import requests

from model import Item, Schedule, SalmonRun

API_LEAGUE = "league"
API_RANKED = "gachi"
API_REGULAR = "regular"

img_base = "https://splatoon2.ink/assets/splatnet"


def request_schedule(mode: str, request_time: float) -> Optional[Schedule]:
    data_url = "https://splatoon2.ink/data/schedules.json"
    schedules = requests.get(data_url).json()

    for schedule in schedules.get(mode, []):
        start_time = schedule["start_time"]
        end_time = schedule["end_time"]

        if start_time <= request_time <= end_time:
            return Schedule(start_time, end_time, schedule["rule"]["name"],
                            [create_item(schedule["stage_a"]),
                             create_item(schedule["stage_b"])])
    return None


def request_salmon_run(request_time: float) -> Optional[SalmonRun]:
    data_url = "https://splatoon2.ink/data/coop-schedules.json"
    salmon_runs = requests.get(data_url).json()

    for salmon_run in salmon_runs["details"]:
        start_time = salmon_run["start_time"]
        end_time = salmon_run["end_time"]

        if start_time <= request_time <= end_time:
            weapons = list(map(lambda weapon_dict: next(v for (k, v)
                                                        in weapon_dict.items()
                                                        if "weapon" in k),
                               salmon_run["weapons"]))
            return SalmonRun(start_time, end_time,
                             create_item(salmon_run["stage"]),
                             list(map(create_item, weapons)))
    return None


def request_next_salmon_run() -> Optional[SalmonRun]:
    data_url = "https://splatoon2.ink/data/coop-schedules.json"
    salmon_runs = requests.get(data_url).json()
    details = salmon_runs["details"]
    if len(details) == 0:
        return None
    else:
        return request_salmon_run(details[-1]["start_time"])

def create_item(item_dict: dict) -> Item:
    return Item(item_dict["name"], img_base + item_dict["image"])
