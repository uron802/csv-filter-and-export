import pandas as pd
import yaml
import os

# 設定ファイルの読み込み
with open('/app/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

csv_file_path = config['csv_file_path']
output_dir = config['output_dir']
output_file_path = os.path.join(output_dir, config['output_file_path'])
encoding = config['encoding']
target_strings_file_path = config['target_strings_file_path']
column_index = config['column_index']
header_flag = config['header_flag']
newline_char = config['newline_char']
debug_flag = config['debug_flag']

# デバッグ用のエンコーディングの出力
if debug_flag:
    print(f"Using encoding: {encoding}")

# 検索文字列の読み込み
with open(target_strings_file_path, 'r', encoding=encoding) as f:
    raw_content = f.read()

    # デバッグ用の生データ出力
    if debug_flag:
        print(f"Raw content read from file:\n{repr(raw_content)}")

    if newline_char:
        raw_target_strings = raw_content.split(newline_char)
        if debug_flag:
            print(f"Using custom newline character for splitting: {repr(newline_char)}")
    else:
        raw_target_strings = raw_content.splitlines()
        if debug_flag:
            print("Using default newline character for splitting")

# 分割後の各行のデバッグ出力
if debug_flag:
    for i, line in enumerate(raw_target_strings):
        print(f"Line {i}: {repr(line)}")

target_strings = [line.strip() for line in raw_target_strings if line.strip()]

if debug_flag:
    print(f"Target strings: {target_strings}")

# CSVファイルの読み込み
df = pd.read_csv(csv_file_path, encoding=encoding, header=0 if header_flag else None)

if debug_flag:
    print(f"Dataframe head:\n{df.head()}")
    print(f"Total rows: {len(df)}, Total columns: {len(df.columns)}")

# 検索対象列の内容をファイルに出力（デバッグ用）
if debug_flag:
    column_data_file = os.path.join(output_dir, 'column_data.txt')
    with open(column_data_file, 'w', encoding=encoding) as f:
        for item in df.iloc[:, column_index]:
            f.write(f"{item}\n")

# 検索条件に一致する行をフィルタリング
filtered_df = df[df.iloc[:, column_index].isin(target_strings)]

if debug_flag:
    print(f"Filtered dataframe head:\n{filtered_df.head()}")
    print(f"Total matched rows: {len(filtered_df)}")

# フィルタリングされたデータをCSVに出力
os.makedirs(output_dir, exist_ok=True)
filtered_df.to_csv(output_file_path, index=False, encoding=encoding)

if debug_flag:
    print(f"Filtered data saved to {output_file_path}")
