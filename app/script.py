import pandas as pd
import yaml
import os

# 設定ファイルのパス
config_file_path = '/app/config.yaml'

# 設定の読み込み
with open(config_file_path, 'r') as file:
    config = yaml.safe_load(file)

# 設定の取得
csv_file_path = config['csv_file_path']
output_dir = config['output_dir']
output_file_path = config['output_file_path']
encoding = config['encoding']
target_strings_file_path = config['target_strings_file_path']
column_index = config['column_index']
header_flag = config['header_flag']
newline_char = config['newline_char']
debug_flag = config['debug_flag']

# デバッグ情報を表示する関数
def debug_log(message):
    if debug_flag:
        print(message)

# ターゲット文字列の読み込み
with open(target_strings_file_path, 'r', encoding=encoding) as file:
    raw_target_strings = file.read()
    
debug_log(f"Raw content read from file:\n{raw_target_strings}")

# 改行コードで分割
target_strings = raw_target_strings.split(newline_char)
target_strings = [s.strip() for s in target_strings if s.strip()]

debug_log(f"Using custom newline character for splitting: '{newline_char}'")
debug_log(f"Target strings: {target_strings}")

# CSVファイルの読み込み
df = pd.read_csv(csv_file_path, encoding=encoding, header=0 if header_flag else None)

debug_log(f"Dataframe head:\n{df.head()}")
debug_log(f"Total rows: {len(df)}, Total columns: {len(df.columns)}")

# フィルタリング
filtered_df = df[df.iloc[:, column_index].astype(str).apply(lambda x: any(target in x for target in target_strings))]

debug_log(f"Filtered dataframe head:\n{filtered_df.head()}")
debug_log(f"Total matched rows: {len(filtered_df)}")

# 結果をCSVファイルに保存
os.makedirs(output_dir, exist_ok=True)
filtered_df.to_csv(os.path.join(output_dir, output_file_path), index=False, encoding=encoding)

debug_log(f"Filtered data saved to {os.path.join(output_dir, output_file_path)}")
