# モジュールのインポート
import sqlite3
import utility as U
# データベースへの接続
connection = sqlite3.connect("E:\Documents\競馬\everydb2.2\Application Files\EveryDB2.2_2_2_0_0\ecore.db")
# カーソルオブジェクトの生成
cursor = connection.cursor()
# SQL文
strSQL = "SELECT * FROM N_RACE WHERE JyoCD = '05' AND Year = '2022'"

# 結果取得（行）
for row in cursor.execute(strSQL):
    print(row)