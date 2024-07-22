import pandas as pd
import os

# パラメータ設定
csv_file_path = '/app/data.csv'  # 入力CSVファイルのパス
output_dir = '/app/output'  # 出力先ディレクトリ
output_file_path = os.path.join(output_dir, 'filtered_data.csv')  # 出力CSVファイルのパス
encoding = 'utf-8'  # 文字コード
target_strings_file_path = '/app/target_strings.txt'  # 検索する文字列を含むテキストファイルのパス
column_index = 0  # 検索対象の列番号（0から始まる）
header_flag = True  # ヘッダーありの場合はTrue、なしの場合はFalse
newline_char = '\n'  # 改行コード（例：\n、\r\n）

# 検索する文字列のリストをテキストファイルから読み込む
with open(target_strings_file_path, 'r', encoding=encoding) as file:
    target_strings = file.read().split(newline_char)

# ヘッダーの有無に応じた読み込み方法
if header_flag:
    df = pd.read_csv(csv_file_path, encoding=encoding)
else:
    df = pd.read_csv(csv_file_path, encoding=encoding, header=None)

# 列番号に基づくフィルタリング
filtered_df = df[df.iloc[:, column_index].isin(target_strings)]

# 出力ディレクトリが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 抽出したデータをCSVファイルとして出力（読み込んだときと同じエンコードを使用）
filtered_df.to_csv(output_file_path, index=False, encoding=encoding)

print(f'Filtered data has been written to {output_file_path}')
