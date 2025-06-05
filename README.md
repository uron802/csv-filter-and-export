# CSVフィルタリングプログラム

このプロジェクトでは、CSVファイルをフィルタリングし、指定した条件に基づいて結果を別のCSVファイルとして出力するプログラムを提供します。以下の手順で環境を構築し、プログラムを実行することができます。

## 環境構築

### 1. 必要なファイルを準備

プロジェクトディレクトリを作成し、以下のファイルを配置します。

```
my_project/
├── app/
│   ├── script.py
│   ├── config.yaml  # プログラムの設定ファイル。（内容は適宜変更してください）。
│   └── requirements.txt
├── docker/
│   └── Dockerfile
├── data/
│   └── data.csv  # ユーザーが用意する入力ファイル
├── target/
│   └── target_strings.txt  # ユーザーが用意する検索文字列ファイル
├── tests/
│   ├── fixtures/
│   │   ├── test_config.yaml
│   │   ├── test_data.csv
│   │   └── test_target_strings.txt
│   └── test_script.py
└── output/
    └── filtered_data.csv  # フィルタリング結果が保存されるファイル
```

### 2. 実行手順
#### 1. Docker Composeの起動
プロジェクトディレクトリで以下のコマンドを実行し、Docker Composeを使ってPython環境を立ち上げます。

```
docker-compose up -d
```

#### 2. コンテナに入る
コンテナ内に入るには以下のコマンドを実行します。

```
docker-compose exec python sh
```

#### 3. Pythonスクリプトを実行

```
python /app/script.py
```

これにより、data.csvの内容が指定された条件でフィルタリングされ、結果がoutput/filtered_data.csvに保存されます。

### 3. テスト実行方法

Docker環境内でテストを実行するには、以下のコマンドを使用します。

```
./run_tests_docker.sh
```

テストを直接実行する場合は、事前に依存パッケージをインストールしておきます。

```
pip install -r app/requirements.txt
```

または、コンテナ内で直接実行することもできます。

```
docker-compose exec python sh -c "cd /app && pytest -xvs tests/"
```

VSCodeのテストエクスプローラーでもテストを実行できます。プロジェクトルートの`pytest.ini`ファイルにより、テストが自動的に認識されます。

### 4. デバッグ情報

デバッグフラグが有効になっている場合、以下の情報がコンソールに出力されます。

- target_strings の内容と改行コード
- 読み込んだ列のデータ
- データフレームのヘッドと統計情報

### 5. 注意事項

- data.csvとtarget_strings.txtのファイルパスは、script.py内で設定されたパスに合わせてください。
- target_strings.txtの改行コードは、newline_char変数で指定してください（例：\n、\r\n）。
- encoding変数で指定された文字コードは、CSVファイルのエンコードに一致する必要があります。

### 6. 最後に 

本プログラムの開発には、ChatGPTに協力していただきました。

ありがとう。ChatGPT！
