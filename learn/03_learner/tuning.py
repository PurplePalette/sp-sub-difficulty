import csv
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split

# データの読み込み
with open("learnable.csv", "r") as f:
    reader = csv.reader(f)
    labels = []
    values = []
    for row in reader:
        labels.append(int(row[0]))
        values.append(list(map(float, row[1:])))

# 学習用とテスト用データに分ける
data_train, data_test, label_train, label_test = train_test_split(
    values, labels
)

# ランダムフォレストモデル
clf = RandomForestClassifier()

# ハイパーパラメータチューニングに使った値
parameters = {
    'n_estimators': [10, 20, 30, 50, 100, 300],     # 用意する決定木モデルの数
    'max_features': ('sqrt', 'log2', None),  # ランダムに指定する特徴量の数
    'max_depth':    (10, 20, 30, 40, 50, None),     # 決定木のノード深さの制限値
}

# ハイパーパラメータチューニング(グリッドサーチのコンストラクタにモデルと辞書パラメータを指定)
gridsearch = GridSearchCV(
    estimator=clf,        # モデル
    param_grid=parameters,  # チューニングするハイパーパラメータ
    scoring="accuracy"      # スコアリング
)
gridsearch.fit(data_train, label_train)


# グリッドサーチの結果から得られた最適なパラメータ候補を確認
print('Best params: {}'.format(gridsearch.best_params_))
print('Best Score: {}'.format(gridsearch.best_score_))

"""
Best params: {'max_depth': None, 'max_features': 'log2', 'n_estimators': 50}
Best Score: 0.41710934227063257
"""
