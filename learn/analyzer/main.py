from typing import Counter
import numpy as np
import glob
import sus

files = glob.glob("./charts/*.sus")
file = files[20]

with open(file, "r") as f:
    score = sus.load(f)
    # タップデータ
    tap_np = np.array(score.taps)
    tap_cnt = len(score.taps)
    tap_diff = np.diff([t.tick for t in tap_np])
    tap_diff = [abs(t) for t in tap_diff]
    tap_diff_max = max(tap_diff)
    tap_diff_min = min(tap_diff)
    tap_diff_avg = sum(tap_diff) / len(tap_diff)
    print("tap_cnt:", tap_cnt)
    print("tap_max:", tap_diff_max)
    print("tap_min:", tap_diff_min)
    print("tap_avg:", tap_diff_avg)
    # 同時押しデータ
    # タップの時間毎の同時押し数
    tap_ticks = [t.tick for t in score.taps]
    tap_counter = Counter(tap_ticks)
    # 同時押し数の最大値
    tap_counter_max = tap_counter.most_common()[0][0]
    # 同時押し数の平均値
    tap_counter_values = [c[0] for c in tap_counter.most_common()]
    tap_counter_avg = sum(tap_counter_values) / len(tap_counter_values)
    # タップレーンデータ
    tap_widths = [t.width for t in score.taps]
    tap_widths_cnt = len(tap_widths)
    tap_widths_max = max(tap_widths)
    tap_widths_min = min(tap_widths)
    tap_widths_avg = sum(tap_widths) / tap_widths_cnt
    print("tap_widths_max:", tap_widths_max)
    print("tap_widths_min:", tap_widths_min)
    print("tap_widths_avg:", tap_widths_avg)
    # スライドデータ
    sld_cnt = len(score.slides)
    sld_diff = [abs(sld[0].tick - sld[1].tick) for sld in score.slides]
    sld_diff_max = max(sld_diff)
    sld_diff_min = min(sld_diff)
    sld_diff_avg = sum(sld_diff) / len(sld_diff)
    print("sld_cnt:", sld_cnt)
    print("sld_max:", sld_diff_max)
    print("sld_min:", sld_diff_min)
    print("sld_avg:", sld_diff_avg)
    # フリックデータ
    dir_cnt = len(score.directionals)
    # BPMデータ
    bpm_cnt = len(score.bpms)
    bpm_avg = sum(bpm[1] for bpm in score.bpms) / bpm_cnt
    bpm_max = max(bpm[1] for bpm in score.bpms)
    bpm_min = min(bpm[1] for bpm in score.bpms)
    print(f"bpm_cnt: {bpm_cnt:.2f}")
    print(f"bpm_avg: {bpm_avg:.2f}")
    print(f"bpm_max: {bpm_max:.2f}")
    print(f"bpm_min: {bpm_min:.2f}")
    # TODO: 合計ノーツ数
    # TODO: 曲の秒数
    # TODO: 中央値
    # TODO: statisticsの利用