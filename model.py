from dataclasses import dataclass


@dataclass
class Stage:
    name: str
    img_url: str


@dataclass
class Schedule:
    start_time: float
    end_time: float
    mode: str
    stages: [Stage]
