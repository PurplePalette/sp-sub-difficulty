from dataclasses_json import dataclass_json
from dataclasses import dataclass


@dataclass_json
@dataclass
class LearnChart:
    id: int
    title: str
    musicDifficulty: str
    playLevel: int
    noteCount: int
