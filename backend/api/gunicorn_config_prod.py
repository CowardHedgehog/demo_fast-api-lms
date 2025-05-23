# 実行するPythonがあるパス
pythonpath = './'

# ワーカー数
workers = 2

# ワーカーのクラス、*2 にあるようにUvicornWorkerを指定 (Uvicornがインストールされている必要がある)
worker_class = 'uvicorn.workers.UvicornWorker'

# IPアドレスとポート
bind = 'kit-ai.mars.kanazawa-it.ac.jp:80'

# # プロセスIDを保存するファイル名
# pidfile = 'prod.pid'

# Pythonアプリに渡す環境変数
raw_env = ['MODE=PROD']

# デーモン化する場合はTrue
daemon = True

# エラーログ
errorlog = './logs/error_log.txt'

# プロセスの名前
proc_name = 'backend'

# アクセスログ
accesslog = './logs/access_log.txt'
