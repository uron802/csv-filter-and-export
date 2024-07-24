# ベースイメージ
FROM python:3.8-slim

# 作業ディレクトリを作成
WORKDIR /app

# 必要なパッケージをインストール
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# スクリプトと設定ファイルをコピー
COPY app/script.py /app/script.py
COPY app/config.yaml /app/config.yaml

# デフォルトでシェルを起動
CMD ["sh"]
