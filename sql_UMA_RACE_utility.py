# モジュールのインポート
import sqlite3
import getCodeValue as gc
import utility as U
# データベースへの接続
connection = sqlite3.connect("E:\Documents\競馬\everydb2.2\Application Files\EveryDB2.2_2_2_0_0\ecore.db")
# カーソルオブジェクトの生成
cursor = connection.cursor()
# カラム名リスト
N_UMA_RACE_ColumnNames = []
# カラム名リストの生成
for row in cursor.execute("pragma table_info(N_UMA_RACE)"):
    N_UMA_RACE_ColumnNames.append(row[1])
# SQL文
strSQL_SELECT = "SELECT * FROM N_UMA_RACE"
strSQL_WHERE = " WHERE DataKubun = '7'"
strSQL_WHERE += " AND Year = '2022'"
strSQL_WHERE += " AND MonthDay = '1224'"
strSQL_WHERE += " AND JyoCD = '06'"
strSQL_WHERE += " AND RaceNum = '11'"
strSQL_ORDER = " ORDER BY Umaban ASC"
# SQL文の連結
strSQL = strSQL_SELECT + strSQL_WHERE + strSQL_ORDER
# レース情報リスト
UMA_RACEs = U.getUMA_RACEs(strSQL)
# SQL文の実行
#results = cursor.execute(strSQL)
# 辞書型
#for row in results:
#    dic = {}
#    for n in range(len(N_UMA_RACE_ColumnNames)):
#        # 辞書型へ変換
#        dic[N_UMA_RACE_ColumnNames[n]] = row[n]
#    # リストへ格納
#    UMA_RACEs.append(dic)

# レコードの確認
#print(RACEs[0])  # SQL文

# 出走馬ごとに
for UMA_RACE in UMA_RACEs:
    # 文字列整形
    text = ""
    text += UMA_RACE["Wakuban"] + "枠"
    text += UMA_RACE["Umaban"] +  "番"
    text += UMA_RACE["Bamei"] + " ("
    text += gc.getCodeValue("2202",UMA_RACE["SexCD"],1) + " ,"
    text += str(int(UMA_RACE["Barei"])) + "歳"
    text += UMA_RACE["BaTaijyu"] + " kg("
    text += UMA_RACE["ZogenFugo"] + str(int(UMA_RACE["ZogenSa"])) + ")"
    text += str(int(UMA_RACE["Ninki"])) + "番人気"
    text += str(int(UMA_RACE["Odds"]) / 10) + "倍"
    text += UMA_RACE["KisyuRyakusyo"] + "騎手"
    text += str(int(UMA_RACE["Futan"]) / 10) + "kg"
    # ターミナルへ出力
    print(text)


