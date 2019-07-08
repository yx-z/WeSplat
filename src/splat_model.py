from dataclasses import dataclass


@dataclass
class Item:
    """
    ex. Stage, Weapon
    """
    name: str
    img_url: str


@dataclass
class Schedule:
    start_time: float
    end_time: float
    mode: str
    stages: [Item]


@dataclass
class SalmonRun:
    start_time: float
    end_time: float
    stage: Item
    weapons: [Item]
