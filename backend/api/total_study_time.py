import csv
import datetime
from collections import defaultdict

# ログファイルを読み込み、辞書のリストに変換
with open('access_user.log', 'r') as file:
    logs = [{'date': datetime.datetime.strptime(line.split()[0], '%Y-%m-%d'),
             'time': datetime.datetime.strptime(line.split()[1], '%H:%M:%S,%f'),
             'user': line.split()[2]}
            for line in file.readlines()]

# 日付とユーザ名でログをグループ化
grouped_logs = defaultdict(list)
for log in logs:
    grouped_logs[(log['date'], log['user'])].append(log['time'])

# 各グループの最初と最後のアクセス時間の差を計算
total_access_time = [{'date': date, 'user': user, 'access_time': max(times) - min(times)}
                     for (date, user), times in grouped_logs.items()]

# 結果をCSVファイルに書き出し
with open('total_access_time.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=['date', 'user', 'access_time'])
    writer.writeheader()
    writer.writerows(total_access_time)
