from typing import Counter, List, Union
import numpy as np
import glob
import sus
import statistics
import math
import json
import csv


class ChartAnalyzer():
    TICKS_PER_BEAT = 480

    def get_feature_values(
        self, values: List[Union[float, int]]
    ) -> List[float]:
        """配列から特徴量となりうる値(個数,最大値,最小値,平均値,中央値,標準偏差)を求めて返す"""
        len_value = len(values)
        max_value = max(values)
        # min_value = min(values)
        avg_value = statistics.mean(values)
        med_value = statistics.median(values)
        value_np = np.array(values)
        sd_value = np.std(value_np, ddof=0)
        return [
            len_value, max_value, avg_value, med_value, sd_value
        ]

    def get_count_values(self, score) -> List[int]:
        """Scoreから各ノーツの個数を求める"""
        # 全データごちゃまぜ
        all_notes = score.taps + sum(score.slides, []) + score.directionals
        # 合計ノーツ/タップ/フリック/スライド数
        notes_cnt = len(all_notes)
        tap_cnt = len(score.taps)
        dir_cnt = len(score.directionals)
        sld_cnt = len(score.slides)
        # 譜面長
        chart_len = max([n.tick for n in all_notes])
        return [notes_cnt, tap_cnt, dir_cnt, sld_cnt, chart_len]

    def get_feature_values_from_sus(self, file_path: str) -> List[float]:
        """SUSファイルから特徴データを求める"""
        with open(file_path, "r", encoding="utf8") as f:
            score = sus.load(f)
        # 全データごちゃまぜ
        all_notes = score.taps + sum(score.slides, []) + score.directionals
        notes_counts = self.get_count_values(score)
        # 譜面長
        chart_len = max([n.tick for n in all_notes])
        # タップ間隔
        tap_np = np.array(score.taps)
        tap_diff = np.diff([t.tick for t in tap_np])
        tap_diff = [abs(t) for t in tap_diff if t != 0]
        tap_diff_features = self.get_feature_values(tap_diff)
        # タップ同時押し数
        tap_ticks = [t.tick for t in score.taps]
        tap_counter = Counter(tap_ticks)
        tap_counter_values = [c[1] for c in tap_counter.most_common()]
        tap_counter_features = self.get_feature_values(tap_counter_values)
        # タップレーン幅
        tap_widths = [t.width for t in score.taps]
        tap_widths_features = self.get_feature_values(tap_widths)
        # スライド長
        sld_diff = [abs(sld[0].tick - sld[1].tick) for sld in score.slides]
        sld_diff_features = self.get_feature_values(sld_diff)
        # BPM
        bpm_values = [bpm[1] for bpm in score.bpms]
        bpm_features = self.get_feature_values(bpm_values)[:1]
        # 曲長のうち 4分音符の個数
        beat_cnt = math.ceil(chart_len / self.TICKS_PER_BEAT)
        # 4分音符 1つあたりのノーツ数
        notes_per_beat = [
            len([
                n for n in all_notes
                if n.tick >= i * self.TICKS_PER_BEAT
                and n.tick < (i + 1) * self.TICKS_PER_BEAT
            ])
            for i in range(beat_cnt)
        ]
        notes_per_beat_features = self.get_feature_values(notes_per_beat)
        # 特長データ配列を生成
        # NOTE: スライドは2ノーツ以上で構成されるのでtotal_notesとsld_cntは不一致
        feature_values = [
            notes_counts,
            [chart_len],
            tap_diff_features,
            tap_counter_features,
            tap_widths_features,
            sld_diff_features,
            bpm_features,
            notes_per_beat_features,
        ]
        resp = sum(feature_values, [])
        return resp


def generate_learnable_csv_from_sus_dir(
    sus_dir: str, difficulties_file: str,  out_file: str
) -> None:
    """SUSフォルダから学習用のCSVを生成する"""
    with open(difficulties_file, "r", encoding="utf8") as f:
        difficulties = json.loads(f.read())
    analyzer = ChartAnalyzer()
    csv_data = []
    for file_path in glob.glob(sus_dir + "/*.sus"):
        filename = file_path.split("\\")[-1]
        music_id = int(filename.split("_")[0])
        difficulty_name = filename.split("_")[1].split(".sus")[0]
        print(music_id, difficulty_name)
        difficulty = [
            d
            for d in difficulties
            if d["id"] == music_id and d["musicDifficulty"] == difficulty_name
        ][0]["playLevel"]
        feat = analyzer.get_feature_values_from_sus(file_path)
        csv_data.append([difficulty] + feat)
    with open(out_file, 'w', newline="") as f:
        writer = csv.writer(f)
        for row in csv_data:
            writer.writerow(row)
    print("Success!")


if __name__ == "__main__":
    generate_learnable_csv_from_sus_dir(
        "charts", "result.json", "learnable.csv"
    )
