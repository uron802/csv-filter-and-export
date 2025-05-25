import pandas as pd
import yaml
import os

# デバッグ情報を表示する関数
def debug_log(message, debug_flag=False):
    if debug_flag:
        print(message)

def load_config(config_file_path='/app/config.yaml'):
    """設定ファイルを読み込む"""
    with open(config_file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def load_target_strings(target_strings_file_path, encoding, newline_char, debug_flag=False):
    """ターゲット文字列をファイルから読み込む"""
    with open(target_strings_file_path, 'r', encoding=encoding) as file:
        raw_target_strings = file.read()
    
    debug_log(f"Raw content read from file:\n{raw_target_strings}", debug_flag)
    
    # 改行コードで分割
    target_strings = raw_target_strings.split(newline_char)
    target_strings = [s.strip() for s in target_strings if s.strip()]
    
    debug_log(f"Using custom newline character for splitting: '{newline_char}'", debug_flag)
    debug_log(f"Target strings: {target_strings}", debug_flag)
    
    return target_strings

def filter_csv(csv_file_path, encoding, column_index, header_flag, target_strings, debug_flag=False):
    """CSVファイルをロードして、指定した列にターゲット文字列が含まれる行をフィルタリングする"""
    # CSVファイルの読み込み
    df = pd.read_csv(csv_file_path, encoding=encoding, header=0 if header_flag else None)
    
    debug_log(f"Dataframe head:\n{df.head()}", debug_flag)
    debug_log(f"Total rows: {len(df)}, Total columns: {len(df.columns)}", debug_flag)
    
    # フィルタリング
    filtered_df = df[df.iloc[:, column_index].astype(str).apply(lambda x: any(target in x for target in target_strings))]
    
    debug_log(f"Filtered dataframe head:\n{filtered_df.head()}", debug_flag)
    debug_log(f"Total matched rows: {len(filtered_df)}", debug_flag)
    
    return filtered_df

def save_filtered_csv(filtered_df, output_dir, output_file_path, encoding, debug_flag=False):
    """フィルタリングされたデータをCSVファイルとして保存する"""
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, output_file_path)
    filtered_df.to_csv(output_file, index=False, encoding=encoding)
    
    debug_log(f"Filtered data saved to {output_file}", debug_flag)
    
    return output_file

def main(config_file_path='/app/config.yaml'):
    """メイン処理を実行する"""
    # 設定の読み込み
    config = load_config(config_file_path)
    
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
    
    # ターゲット文字列の読み込み
    target_strings = load_target_strings(
        target_strings_file_path,
        encoding,
        newline_char,
        debug_flag
    )
    
    # CSVフィルタリング
    filtered_df = filter_csv(
        csv_file_path,
        encoding,
        column_index,
        header_flag,
        target_strings,
        debug_flag
    )
    
    # 結果を保存
    save_filtered_csv(
        filtered_df,
        output_dir,
        output_file_path,
        encoding,
        debug_flag
    )

# スクリプトが直接実行された場合のみメイン処理を実行
if __name__ == "__main__":
    # 設定ファイルのパス
    config_file_path = '/app/config.yaml'
    main(config_file_path)
