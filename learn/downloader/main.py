from typing import List
from downloader import ChartDownloader
from models.sekai_difficulty import SekaiDifficulty
from models.learn_chart import LearnChart
import json
import asyncio


def convert_raw_to_learnable(
    sekai_difficulties: List[SekaiDifficulty],
) -> List[LearnChart]:
    """機械学習用のデータ型に変換する"""
    learn_charts = [
        LearnChart(
            id=s.musicId,
            title=s.musicTitle,
            musicDifficulty=s.musicDifficulty,
            playLevel=s.playLevel,
            noteCount=s.noteCount
        )
        for s in sekai_difficulties
    ]
    return learn_charts


async def main():
    """メイン処理"""
    cl = ChartDownloader("INSERT_API_ENDPOINT", "INSERT_ASSET_ENDPOINT")
    musics = await cl.get_music_list()
    charts = await cl.get_entire_music_difficulties(musics)
    learn_charts = convert_raw_to_learnable(charts)
    with open("result.json", "w", encoding="utf8") as f:
        out = [c.to_dict() for c in learn_charts]
        f.write(json.dumps(out, indent=4, ensure_ascii=False))
    await cl.download_entire_music_charts("./charts", charts)

if __name__ == '__main__':
    asyncio.run(main())
