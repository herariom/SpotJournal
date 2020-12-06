from dataclasses import dataclass

@dataclass
class SongData():
    legend: str
    values: list
    color_r: int
    color_g: int
    color_b: int
