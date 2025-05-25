#!/bin/bash

# Docker環境内でテストを実行するスクリプト

# コンテナが起動しているかチェック
if ! docker-compose ps | grep -q "python.*Up"; then
  echo "Pythonコンテナが起動していません。起動します..."
  docker-compose up -d
fi

# コンテナ内でテスト実行
echo "コンテナ内でテストを実行中..."
docker-compose exec python sh -c "cd /app && pytest -xvs tests/"

exit_code=$?

echo ""
if [ $exit_code -eq 0 ]; then
  echo "✅ テストが正常に完了しました"
else
  echo "❌ テスト実行中にエラーが発生しました"
fi

exit $exit_code