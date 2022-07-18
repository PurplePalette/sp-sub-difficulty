import csv
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split

# データの読み込み
with open("learnable.csv", "r") as f:
    reader = csv.reader(f)
    labels = []
    values = []
    for row in reader:
        labels.append(int(row[0]))
        values.append(list(map(float, row[1:])))

clf = RandomForestClassifier()

# 学習用とテスト用データに分ける
data_train, data_test, label_train, label_test = train_test_split(
    values, labels
)

# 学習と予測
clf = RandomForestClassifier(
    max_depth=None,
    max_features='log2',
    n_estimators=50
)
clf.fit(data_train, label_train)
predict = clf.predict(data_test)

# 精度を確認
ac_score = metrics.accuracy_score(label_test, predict)
cl_report = metrics.classification_report(label_test, predict)
print("正解率=", ac_score)
print("レポート=\n", cl_report)

filename = 'difficulty_model.sav'
pickle.dump(clf, open(filename, 'wb'))
print("モデルを保存しました。")
