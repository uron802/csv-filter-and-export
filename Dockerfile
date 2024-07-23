FROM python:3.8-slim

WORKDIR /app

# requirements.txt をコピーして、必要なパッケージをインストール
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 他のファイルをコピー
COPY . .

CMD ["tail", "-f", "/dev/null"]
