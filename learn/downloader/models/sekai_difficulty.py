from dataclasses_json import dataclass_json
from dataclasses import dataclass


@dataclass_json
@dataclass
class SekaiDifficulty:
    id: int
    musicId: int
    musicTitle: str
    musicDifficulty: str
    playLevel: int
    releaseConditionId: int
    noteCount: int
