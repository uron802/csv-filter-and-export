# CSVフィルタリングプログラム

このプロジェクトでは、CSVファイルをフィルタリングし、指定した条件に基づいて結果を別のCSVファイルとして出力するプログラムを提供します。以下の手順で環境を構築し、プログラムを実行することができます。

## 環境構築

### 1. 必要なファイルを準備

プロジェクトディレクトリを作成し、以下のファイルを配置します。

```
my_project/
├── docker-compose.yml
├── requirements.txt
├── script.py
├── data.csv
└── target_strings.txt
```

- `data.csv`: 入力CSVファイル。
- `target_strings.txt`: 検索する文字列が改行ごとにリストされたテキストファイル。
- `docker-compose.yml`: Docker Composeの設定ファイル。
- `requirements.txt`: 必要なPythonパッケージを指定するファイル。
- `script.py`: CSVフィルタリングを行うPythonスクリプト。

### 2. 実行手順
#### 1. Docker Composeの起動
プロジェクトディレクトリで以下のコマンドを実行し、Docker Composeを使ってPython環境を立ち上げます。

```
docker-compose up -d
```

#### 2. コンテナ内でPythonスクリプトを実行
コンテナ内に入るには以下のコマンドを実行します。

```
docker exec -it python_container sh
```

#### 3. コンテナ内で以下のコマンドを実行して、Pythonスクリプトを実行します。

```
python /app/script.py
```

これにより、data.csvの内容が指定された条件でフィルタリングされ、結果がoutput/filtered_data.csvに保存されます。

### 3. 注意事項

data.csvとtarget_strings.txtのファイルパスは、script.py内で設定されたパスに合わせてください。

target_strings.txtの改行コードは、newline_char変数で指定してください（例：\n、\r\n）。

encoding変数で指定された文字コードは、CSVファイルのエンコードに一致する必要があります。

### 4. 最後に 

本プログラムの開発には、ChatGPTに協力していただきました。

ありがとう。ChatGPT！