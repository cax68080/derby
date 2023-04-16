# モジュールのインポート
import sqlite3
import getCodeValue as gc
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
strSQL_SELECT = "SELECT * FROM N_RACE"
strSQL_WHERE = " WHERE DataKubun = '7'"
strSQL_WHERE += " AND Year = '2022'"
strSQL_WHERE += " AND GradeCD = 'A'"
strSQL_ORDER = " ORDER BY MonthDay ASC,JyoCD DESC"
# SQL文の連結
strSQL = strSQL_SELECT + strSQL_WHERE + strSQL_ORDER
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
#print(RACEs[0])  # SQL文

# レースごとに
for RACE in RACEs:
    # 年月日の取得
    Year = RACE["Year"] + "年"
    MonthDay = RACE["MonthDay"]
    Month = MonthDay[0] + MonthDay[1] + "月"
    Day = MonthDay[2] + MonthDay[3] + "日"
    # 文字列整形
    text = ""
    text += Year + Month + Day + " "
    text += "第" + str(int(RACE["Nkai"])) + "回"
    text += RACE["Hondai"] +  " "
    text += gc.getCodeValue("2001",RACE["JyoCD"],4) + " "
    text += gc.getCodeValue("2009",RACE["TrackCD"],2) + " "
    text += RACE["Kyori"] + "[m] "
    text += gc.getCodeValue("2005",RACE["SyubetuCD"],2) + " "
    text += gc.getCodeValue("2008",RACE["JyuryoCD"],1) + " "
    text += gc.getCodeValue("2006",RACE["KigoCD"],1) + " "
    # ターミナルへ出力
    print(text)
