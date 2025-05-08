from collections import Counter

# ファイルを開く
with open('access_user.log', 'r') as f:
    lines = f.readlines()

# ユーザ名を抽出
users = [line.split()[-1] for line in lines]

# ユーザ名の出現回数をカウント
user_counts = Counter(users)

# 結果を表示
for user, count in user_counts.items():
    print(f'ユーザ名: {user}, アクセス回数: {count}')
