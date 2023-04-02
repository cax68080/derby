# モジュールのインポート
import sqlite3
# データベースへの接続
connection = sqlite3.connect("E:\Documents\競馬\everydb2.2\Application Files\EveryDB2.2_2_2_0_0\ecore.db")
# カーソルオブジェクトの生成
cursor = connection.cursor()
# カラム名リスト
N_RACE_ColumnNames = []
# カラム名リストの生成
for row in cursor.execute("pragma table_info(N_RACE)"):
    N_RACE_ColumnNames.append(row[1])

# レース情報リスト
RACEs = []
# SQL文
strSQL = "SELECT * FROM N_RACE WHERE JyoCD = '01' AND Year = '2022'"
# SQL文の実行
results = cursor.execute(strSQL)
# 辞書型
for row in results:
    dic = {}
    for n in range(len(N_RACE_ColumnNames)):
        # 辞書型へ変換
        dic[N_RACE_ColumnNames[n]] = row[n]
    # リストへ格納
    RACEs.append(dic)

# レコードの確認
print(RACEs[0])  