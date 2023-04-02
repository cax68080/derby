# モジュールのインポート
import sqlite3
import getCodeValue as gc
# データベースへの接続
connection = sqlite3.connect("E:\Documents\競馬\everydb2.2\Application Files\EveryDB2.2_2_2_0_0\ecore.db")
# カーソルオブジェクトの生成
cursor = connection.cursor()
# カラム名リスト
N_UMA_RACE_ColumnNames = []
# カラム名リストの生成
for row in cursor.execute("pragma table_info(N_UMA_RACE)"):
    N_UMA_RACE_ColumnNames.append(row[1])

# レース情報リスト
UMA_RACEs = []
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
# SQL文の実行
results = cursor.execute(strSQL)
# 辞書型
for row in results:
    dic = {}
    for n in range(len(N_UMA_RACE_ColumnNames)):
        # 辞書型へ変換
        dic[N_UMA_RACE_ColumnNames[n]] = row[n]
    # リストへ格納
    UMA_RACEs.append(dic)

# レコードの確認
#print(RACEs[0])  # SQL文

# 出走馬ごとに
for UMA_RACE in UMA_RACEs:
    # 文字列整形
    text = ""
    text = str(int(UMA_RACE["KakuteiJyuni"])) + "着"
    text += UMA_RACE["Wakuban"] + "枠"
    text += UMA_RACE["Umaban"] +  "番"
    text += UMA_RACE["Bamei"]
    text += "(" + str(int(UMA_RACE["Jyuni1c"])) + "-" + str(int(UMA_RACE["Jyuni2c"]))
    text += "-" + str(int(UMA_RACE["Jyuni3c"])) + "-" + str(int(UMA_RACE["Jyuni4c"])) + ")"
    text += "タイム差：" + str(int(UMA_RACE["TimeDiff"])/10) + "秒" 
    text += "上がり3F" + str(int(UMA_RACE["HaronTimeL3"])/10) + "秒"
    if(UMA_RACE["Kyakusitukubun"] == "1"): kyakusitu = "逃" 
    if(UMA_RACE["Kyakusitukubun"] == "2"): kyakusitu = "先"
    if(UMA_RACE["Kyakusitukubun"] == "3"): kyakusitu = "差" 
    if(UMA_RACE["Kyakusitukubun"] == "4"): kyakusitu = "追" 
    text += "脚質：" + kyakusitu
 
    # ターミナルへ出力
    print(text)


