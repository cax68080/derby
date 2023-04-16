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
strSQL = "SELECT * FROM N_RACE WHERE JyoCD = '09' AND Year = '2022'"
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
    #print(text)

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
# カラム名リスト
N_HARAI_ColumnNames = []

# カラム名リストの生成
for row in cursor.execute("pragma table_info(N_HARAI)"):
    N_HARAI_ColumnNames.append(row[1])

# 払い戻し情報リスト
HARAIs = []

# SQL文
strSQL_SELECT = "SELECT * FROM N_HARAI"
strSQL_WHERE = " WHERE DataKubun = '2'"
strSQL_WHERE = " AND Year = '2022'"
strSQL_WHERE = " AND MonthDay = '1222'"
strSQL_WHERE = " AND JyoCD = '06'"
strSQL_WHERE = " AND RaceNum = '11'"

# SQL文の連結
strSQL = strSQL_SELECT + strSQL_WHERE

# SQL文の実行
results = cursor.execute(strSQL)

# 辞書型
for row in results:
    dic = {}
    for n in range(len(N_HARAI_ColumnNames)):
        # 辞書型への変換
        dic[N_RACE_ColumnNames[n]] = row[n]
    # リストへの格納
    HARAIs.append(dic)
HARAI = HARAIs[0]
# 年月日の取得
Year = RACE["Year"] + "年"
MonthDay = RACE["HassoTime"]
Month = MonthDay[0] + MonthDay[1] + "月"
Day = MonthDay[2] + MonthDay[3] + "日"
# 発送時刻
HassoTime = RACE["HassoTime"]
HassoTime = HassoTime[0] + HassoTime[1] + ":" + HassoTime[2] + HassoTime[3]
# 馬場状態の取得
if(int(RACE["TrackCD"]) <= 22):
    BabaCD = RACE["SibaBabaCD"]
else:
    BabaCD = RACE["DirtBabaCD"]
# 1000m通過時タイムの計算
if(int(RACE["Kyori"]) % 200 == 0):
    time1000m = int(RACE["LapTime1"]) / 10 + int(RACE["LapTime2"]) / 10
    + int(RACE["LapTime3"]) / 10 + int(RACE["LapTime4"]) / 10
    + int(RACE["LapTime5"]) / 10
else:
    time1000m = int(RACE["LapTime1"]) / 10 + int(RACE["LapTime2"]) / 10
    + int(RACE["LapTime3"]) / 10 + int(RACE["LapTime4"]) / 10
    + int(RACE["LapTime5"]) / 10 + int(RACE["LapTime6"]) / 10 / 2

# 文字列整形
text = "-----------------------------------------------------------" + "\n"
text += Year + Month + Day + " "
text += "第" + str(int(RACE["NKai"])) + "回"
text += RACE["Hondai"] + " "
text += gc.getCodeValue("2003",RACE["GradeCD"],2) + "\n"
text += gc.getCodeValue("2001",RACE["JyoCD"],1) + " "
text += gc.getCodeValue("2009",RACE["TrackCD"],2) + " "
text += RACE["Kyori"] + "[m] "
text += gc.getCodeValue("2005",RACE["SyubetuCD"],2) + " "
text += gc.getCodeValue("2008",RACE["JyuryoCD"],1) + " "
text += gc.getCodeValue("2006",RACE["KigoCD"],1) + " "
text += gc.getCodeValue("2007",RACE["JyokenCD5"],1) + "\n"
text += "本賞金："
for i in range(5):
    n = str(i + 1)
    if(i != 0):
        text += ","
    text += str(int(int(RACE["Honsyokin" + n]) / 100)) + "万円"
text += "\n"
text += "発送時刻：" + HassoTime + " / "
text += "天候：" + gc.getCodeValue("2011",RACE["TenkoCD"],1) + " / "
text += "馬場：" + gc.getCodeValue("2010",BabaCD,1) + " / "
text += "出走頭数：" + RACE["SyussoTosu"] + "\n"
text += "--------------------------------------------------------" + "\n"
text += "\n"
text += "勝ちタイム：" + UMA_RACEs[0]["Time"][0] + ":" + UMA_RACEs[0]["Time"][1] + UMA_RACEs[0]["Time"][2] + "." + UMA_RACEs[0]["Time"][3] + " "
text += "上がり4F：" + str(int(RACE["HaronTimeL4"]) / 10) + "秒"
text += "上がり3F：" + str(int(RACE["HaronTimeL3"]) / 10) + "秒"
text += "1000m通過時：" + str(time1000m) + "秒\n"
text += "ラップタイム："
for i in range(25):
    strLapTime = "LapTime" + str(i + 1)
    if(RACE[strLapTime] != "000"):
        if(i > 0):
            text += "-"
        text += str(int(RACE[strLapTime]) / 10)
text += "\n"
# コーナー通過順位
for i in range(4):
    n = str(i + 1)
    if(RACE["Corner" + n] != "0"):
        text += "第" + RACE["Corner" + n] + "コーナー：" + RACE["Jyuni" + n] + "\n"
text += "----------------" + "\n"
text += "----------------" + "\n"




