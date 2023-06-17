#モジュールのインポート
import sqlite3
#データベースへの接続
connection = sqlite3.connect("E:\Documents\競馬\everydb2.2\Application Files\EveryDB2.2_2_2_0_0\ecore.db")
#カーソルオブジェクトの生成
cursor = connection.cursor()
