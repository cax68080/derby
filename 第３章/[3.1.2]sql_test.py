#モジュールのインポート
import sqlite3
#データベースへの接続
connection = sqlite3.connect("E:\Documents\競馬\everydb2.2\Application Files\EveryDB2.2_2_2_0_0\ecore.db")
#カーソルオブジェクトの生成
cursor = connection.cursor()
#SQL文
strSQL = "SELECT * FROM N_RACE WHERE JyoCD = '10' AND Year = '2023'"
#SQL文の実行
results = cursor.execute(strSQL)
#結果の表示（行）
for row in results:
	print(row)
