import sqlite3
from pprint import pprint

# SQLite を準備
db = 'database.db'
con = sqlite3.connect(db)
cur = con.cursor()

# sql : SQLiteに渡すSQL
# inputs : 入力されたリスト
sql = ''
inputs = []

# 初回の入力待ち
# quit exit のどちらかが入力されたら終了
key_input = input('>>> ').lower()
while not key_input in ('quit', 'exit'):

    # （任意）
    # SHOW TABLES で始まったら、SQLite用のSQLに置き換え
    is_show_tables = key_input.startswith('show tables')
    if is_show_tables:
        key_input = 'select name from sqlite_master where type="table";'

    # （任意）
    # SHOW COLUMNS FROM で始まったら
    # テーブル名を抽出し、SQLite用SQLに置き換え
    is_show_column = key_input.startswith('show columns from')
    if is_show_column:
        table = key_input.split(' ')[3]
        table = table[:-1] if table[-1] == ';' else table
        key_input = f'PRAGMA table_info({table});'

    # 入力されたSQLを inputs に追加
    inputs.append(key_input)

    # 入力が ; で終わっていたらリストの文字列を連結
    # SQLiteに投げてみる
    if key_input.endswith(';'):
        sql = ' '.join(inputs)
        try:
            cur.execute(sql)
            res = cur.fetchall()
            pprint(res)
        except Exception as e:
            print(e)
        finally:
            # 成功しても失敗しても、リストは初期化
            inputs = []

    # 改行して、次の入力待ち
    print()
    key_input = input('>>> ').lower()

# DB にコミットして終了
cur.close()
con.commit()
con.close()
