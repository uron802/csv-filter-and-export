import os
import shutil
import pandas as pd
import pytest
import sys
from pathlib import Path

# Add app directory to Python path - works in any environment
APP_DIR = str(Path(__file__).parent.parent / 'app')
if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)
import script

# テスト用のパス設定
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
FIXTURES_DIR = os.path.join(TESTS_DIR, 'fixtures')
TEST_CONFIG_PATH = os.path.join(FIXTURES_DIR, 'test_config.yaml')
TEST_DATA_CSV = os.path.join(FIXTURES_DIR, 'test_data.csv')
TEST_TARGET_STRINGS = os.path.join(FIXTURES_DIR, 'test_target_strings.txt')
TEST_OUTPUT_DIR = '/tmp/test_output'


@pytest.fixture()
def setup_test_files():
    """テスト用のファイルを /tmp にコピーし、終了後にクリーンアップする"""
    if os.path.exists(TEST_OUTPUT_DIR):
        shutil.rmtree(TEST_OUTPUT_DIR)
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)

    shutil.copy(TEST_DATA_CSV, '/tmp/test_data.csv')
    shutil.copy(TEST_TARGET_STRINGS, '/tmp/test_target_strings.txt')

    yield

    if os.path.exists('/tmp/test_data.csv'):
        os.remove('/tmp/test_data.csv')
    if os.path.exists('/tmp/test_target_strings.txt'):
        os.remove('/tmp/test_target_strings.txt')
    if os.path.exists(TEST_OUTPUT_DIR):
        shutil.rmtree(TEST_OUTPUT_DIR)


def test_load_config():
    """設定ファイルが正しく読み込まれるかテスト"""
    config = script.load_config(TEST_CONFIG_PATH)

    assert isinstance(config, dict)
    assert 'csv_file_path' in config
    assert 'output_dir' in config
    assert 'output_file_path' in config
    assert 'encoding' in config
    assert 'target_strings_file_path' in config
    assert 'column_index' in config
    assert 'header_flag' in config
    assert 'newline_char' in config
    assert 'debug_flag' in config

    assert config['csv_file_path'] == '/tmp/test_data.csv'
    assert config['column_index'] == 2
    assert config['header_flag'] is True

def test_load_target_strings(setup_test_files):
    """ターゲット文字列が正しく読み込まれるかテスト"""

    target_strings = script.load_target_strings(
        '/tmp/test_target_strings.txt',
        'utf-8',
        '\n',
        False
    )

    assert isinstance(target_strings, list)
    assert len(target_strings) == 2
    assert 'red' in target_strings
    assert 'orange' in target_strings


def test_filter_csv(setup_test_files):
    """CSVフィルタリングが正しく動作するかテスト"""

    # テスト用のターゲット文字列
    target_strings = ['red', 'orange']

    # フィルタリングを実行
    filtered_df = script.filter_csv(
        '/tmp/test_data.csv',
        'utf-8',
        2,  # description列
        True,  # ヘッダーあり
        target_strings,
        False  # デバッグフラグ
    )

    assert isinstance(filtered_df, pd.DataFrame)
    assert len(filtered_df) == 3  # 'red'または'orange'を含む行は3行

    # 期待される結果をチェック
    expected_ids = [1, 3, 5]  # apple, orange, cherryの行のID
    actual_ids = filtered_df['id'].tolist()
    assert sorted(actual_ids) == sorted(expected_ids)


def test_save_filtered_csv(setup_test_files):
    """フィルタリングされたデータが正しく保存されるかテスト"""

    # テスト用のデータフレーム
    data = {
        'id': [1, 3, 5],
        'name': ['apple', 'orange', 'cherry'],
        'description': ['A red fruit', 'An orange fruit', 'A red fruit']
    }
    df = pd.DataFrame(data)

    # ファイルに保存
    output_file = script.save_filtered_csv(
        df,
        TEST_OUTPUT_DIR,
        'test_filtered_data.csv',
        'utf-8',
        False
    )

    # ファイルが存在するか確認
    assert os.path.exists(output_file)

    # 保存されたファイルを読み込んで内容を確認
    saved_df = pd.read_csv(output_file)
    assert len(saved_df) == 3
    assert list(saved_df.columns) == ['id', 'name', 'description']


def test_main_function(setup_test_files):
    """メイン関数がエラーなく実行できるかテスト"""

    # メイン関数を実行
    script.main(TEST_CONFIG_PATH)

    # 出力ファイルが存在するか確認
    output_file = os.path.join(TEST_OUTPUT_DIR, 'test_filtered_data.csv')
    assert os.path.exists(output_file)

    # 出力ファイルの内容を確認
    output_df = pd.read_csv(output_file)
    assert isinstance(output_df, pd.DataFrame)
    assert len(output_df) == 3  # 'red'または'orange'を含む行は3行


def test_debug_log(capsys):
    """デバッグログ関数が正しく動作するかテスト"""
    # デバッグフラグがFalseの場合、何も出力されないことを確認
    script.debug_log("Test message", False)
    captured = capsys.readouterr()
    assert captured.out == ""

    # デバッグフラグがTrueの場合、メッセージが出力されることを確認
    script.debug_log("Test message", True)
    captured = capsys.readouterr()
    assert captured.out == "Test message\n"
