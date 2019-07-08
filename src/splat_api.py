from typing import Optional

import requests
from splat_model import Item, Schedule, SalmonRun

API_LEAGUE = "league"
API_RANKED = "gachi"
API_REGULAR = "regular"


def req_schedule(mode: str, req_time: float) -> Optional[Schedule]:
    data_url = "https://splatoon2.ink/data/schedules.json"
    schedules = requests.get(data_url).json()

    for schedule in schedules.get(mode, []):
        start_time = schedule["start_time"]
        end_time = schedule["end_time"]
        if start_time <= req_time <= end_time:
            return Schedule(start_time, end_time, schedule["rule"]["name"],
                            [create_item(schedule["stage_a"]),
                             create_item(schedule["stage_b"])])
    return None


def req_salmon_run(req_time: float) -> Optional[SalmonRun]:
    data_url = "https://splatoon2.ink/data/coop-schedules.json"
    salmon_runs = requests.get(data_url).json()

    for salmon_run in salmon_runs.get("details", []):
        if salmon_run["start_time"] <= req_time <= salmon_run["end_time"]:
            return create_salmon_run(salmon_run)
    return None


def req_nex_salmon_run(req_time: float) -> Optional[SalmonRun]:
    data_url = "https://splatoon2.ink/data/coop-schedules.json"
    salmon_runs = requests.get(data_url).json()
    details = salmon_runs.get("details", [])

    l = len(details)
    for i in range(l):
        salmon_run = details[i]
        if salmon_run["start_time"] <= req_time <= salmon_run["end_time"]:
            if i + 1 < l:
                return create_salmon_run(details[i + 1])
            else:
                return None

    if l > 0:
        return create_salmon_run(details[0])
    else:
        return None


def create_salmon_run(run_dict: dict) -> SalmonRun:
    weapons = list(map(lambda weapon_dict: next(v for (k, v)
                                                in weapon_dict.items()
                                                if "weapon" in k),
                       run_dict["weapons"]))
    return SalmonRun(run_dict["start_time"], run_dict["end_time"],
                     create_item(run_dict["stage"]),
                     list(map(create_item, weapons)))


def create_item(item_dict: dict) -> Item:
    img_base = "https://splatoon2.ink/assets/splatnet"
    return Item(item_dict["name"], img_base + item_dict["image"])
