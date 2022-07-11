from typing import List, Optional
from dataclasses_json import dataclass_json
from dataclasses import dataclass


@dataclass_json
@dataclass
class SekaiMusic:
    id: int
    seq: int
    releaseConditionId: int
    categories: List[str]
    title: str
    lyricist: str
    composer: str
    arranger: str
    dancerCount: int
    selfDancerPosition: int
    assetbundleName: str
    liveTalkBackgroundAssetbundleName: str
    publishedAt: float
    liveStageId: int
    fillerSec: int
    musicCollaborationId: Optional[str] = None
