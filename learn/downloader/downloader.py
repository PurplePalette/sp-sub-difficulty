from models.sekai_difficulty import SekaiDifficulty
from models.sekai_music import SekaiMusic

from typing import Any, List
import httpx
import asyncio
import random


class ChartDownloader():
    API_ENDPOINT: str = ""
    MUSIC_LIST: List[SekaiMusic] = []
    SEMA: Any = None
    INITIALIZED: bool = False

    def __init__(self, api_endpoint: str, asset_endpoint: str) -> None:
        self.SEMA = asyncio.BoundedSemaphore(5)
        self.API_ENDPOINT = api_endpoint
        self.ASSET_ENDPOINT = asset_endpoint

    async def get_music_list(self) -> List[SekaiMusic]:
        """サーバーから曲リストを取得"""
        async with self.SEMA:
            print("Getting music list ...")
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    f"{self.API_ENDPOINT}/database/master/musics",
                    params={
                        "$limit": 999,
                        "$sort[id]": 1
                    }
                )
                print("Succeed to get music list")
                return [SekaiMusic(**m) for m in r.json()["data"]]

    async def get_music_difficulties(
        self, music_id: int, music_title: str = ""
    ) -> List[SekaiDifficulty]:
        """サーバーから指定した曲の難易度一覧情報(json)を取得、曲名も入れたい場合は手動で渡す"""
        async with self.SEMA:
            await asyncio.sleep(random.randint(0, 3))
            print(f"Getting music data: {music_id} ...")
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    f"{self.API_ENDPOINT}/database/master/musicDifficulties",
                    timeout=20,
                    params={
                        "musicId": music_id,
                    }
                )
                print(f"Succeeded to get music data: {music_id}")
                sekai_charts = [
                    SekaiDifficulty(musicTitle=music_title, **c)
                    for c in r.json()["data"]
                ]
                return sekai_charts

    async def download_music_chart(
        self, music_id: int, difficulty: str
    ) -> bytes:
        """サーバーから指定した曲/難易度の譜面(SUSファイル)をtextとして取得"""
        async with self.SEMA:
            await asyncio.sleep(random.randint(0, 3))
            print(f"Downloading music chart: {music_id} / {difficulty} ...")
            async with httpx.AsyncClient() as client:
                d = difficulty
                id = str(music_id).zfill(4)
                r = await client.get(
                    f"{self.ASSET_ENDPOINT}/file/"
                    + f"pjsekai-assets/startapp/music/music_score/{id}_01/{d}",
                    timeout=20,
                )
                print(f"Succeeded to get chart data: {music_id}/{difficulty}")
                return r.content

    async def save_music_chart(
        self, music_id: int, difficulty: str, file_path: str
    ) -> None:
        """指定した曲ID、難易度の譜面を指定されたパスのファイルに保存"""
        content = await self.download_music_chart(music_id, difficulty)
        with open(file_path, "wb") as f:
            f.write(content)

    async def get_entire_music_difficulties(
        self, music_data: List[SekaiMusic]
    ) -> List[SekaiDifficulty]:
        """指定されたSekaiMusicのリストから全ての難易度の譜面情報を取得して返す"""
        charts = await asyncio.gather(
            *[self.get_music_difficulties(c.id, c.title) for c in music_data]
        )
        charts = sum(charts, [])
        return charts

    async def download_entire_music_charts(
        self, output_path: str, chart_data: List[SekaiDifficulty]
    ) -> None:
        """指定されたSekaiDifficultyのリストから全ての譜面をダウンロードする"""
        tasks = [
            self.save_music_chart(
                c.musicId,
                c.musicDifficulty,
                f"{output_path}/{c.musicId}_{c.musicDifficulty}.sus"
            )
            for c in chart_data
        ]
        await asyncio.gather(*tasks)
