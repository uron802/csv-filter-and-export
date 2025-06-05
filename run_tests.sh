#!/bin/bash

# 必要なパッケージをインストール
pip install -r app/requirements.txt

# テストを実行
pytest -xvs tests/

