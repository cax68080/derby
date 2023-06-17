#モジュールのインポート
import sqlite3
#データベースへの接続
connection = sqlite3.connect("../ecore.db")
#カーソルオブジェクトの生成
cursor = connection.cursor()

#コード表リスト
CodeTable = []
#外部ファイルの読み込み
f_in = open('../CodeTable.csv')
#コード表リストの生成
for line in f_in.readlines():
	values = line.split(',')
	CodeTable.append( values )
#ファイルクローズ
f_in.close()

#「コード」→「値」変換関数の定義
def getCodeValue( code, key, type ):
	for c in CodeTable:
		if(c[0] == code and c[1] == key ): return c[ type + 1 ]

#カラム名リスト
N_RACE_ColumnNames = []
#カラム名リストの生成
for row in cursor.execute("pragma table_info(N_RACE)"):
	N_RACE_ColumnNames.append(row[1])

#カラム名リスト
N_HARAI_ColumnNames = []
#カラム名リストの生成
for row in cursor.execute("pragma table_info(N_HARAI)"):
	N_HARAI_ColumnNames.append(row[1])

#カラム名リスト
N_UMA_RACE_ColumnNames = []
#カラム名リストの生成
for row in cursor.execute("pragma table_info(N_UMA_RACE)"):
	N_UMA_RACE_ColumnNames.append(row[1])


#レース情報リスト
RACEs = []
#SQL文
strSQL_SELECT = "SELECT * FROM N_RACE"
strSQL_WHERE  = " WHERE DataKubun = '7'"
strSQL_WHERE += " AND Year = '2019'"
strSQL_WHERE += " AND MonthDay = '1222'"
strSQL_WHERE += " AND JyoCD ='06'"
strSQL_WHERE += " AND RACENum ='11'"
#SQL文の連結
strSQL = strSQL_SELECT + strSQL_WHERE
#SQL文の実行
results = cursor.execute(strSQL)
#辞書型
for row in results:
	dic = {}
	for n in range(len(N_RACE_ColumnNames)):
		#辞書型へと変換
		dic[N_RACE_ColumnNames[n]] = row[n]
	#リストへの格納
	RACEs.append(dic)


#払い戻し情報リスト
HARAIs = []
#SQL文
strSQL_SELECT = "SELECT * FROM N_HARAI"
strSQL_WHERE  = " WHERE DataKubun = '2'"
strSQL_WHERE += " AND Year = '2019'"
strSQL_WHERE += " AND MonthDay = '1222'"
strSQL_WHERE += " AND JyoCD ='06'"
strSQL_WHERE += " AND RACENum ='11'"
#SQL文の連結
strSQL = strSQL_SELECT + strSQL_WHERE
#SQL文の実行
results = cursor.execute(strSQL)
#辞書型
for row in results:
	dic = {}
	for n in range(len(N_HARAI_ColumnNames)):
		#辞書型へと変換
		dic[N_HARAI_ColumnNames[n]] = row[n]
	#リストへの格納
	HARAIs.append(dic)


#レース情報リスト
UMA_RACEs = []
#SQL文
strSQL_SELECT = "SELECT * FROM N_UMA_RACE"
strSQL_WHERE  = " WHERE DataKubun = '7'"
strSQL_WHERE += " AND Year = '2019'"
strSQL_WHERE += " AND MonthDay = '1222'"
strSQL_WHERE += " AND JyoCD ='06'"
strSQL_WHERE += " AND RACENum ='11'"
strSQL_ORDER  = " ORDER BY KakuteiJyuni ASC"
#SQL文の連結
strSQL = strSQL_SELECT + strSQL_WHERE + strSQL_ORDER 
#SQL文の実行
results = cursor.execute(strSQL)
#辞書型
for row in results:
	dic = {}
	for n in range(len(N_UMA_RACE_ColumnNames)):
		#辞書型へと変換
		dic[N_UMA_RACE_ColumnNames[n]] = row[n]
	#リストへの格納
	UMA_RACEs.append(dic)

RACE = RACEs[0]
HARAI = HARAIs[0]

#年月日の取得
Year = RACE["Year"] + "年"
MonthDay = RACE["MonthDay"]
Month = MonthDay[0] + MonthDay[1] + "月"
Day = MonthDay[2] + MonthDay[3] + "日"
#発走時刻
HassoTime = RACE["HassoTime"]
HassoTime = HassoTime[0] + HassoTime[1] + ":" + HassoTime[2] + HassoTime[3]

#馬場状態の取得
if(int(RACE["TrackCD"])<= 22): 
	BabaCD = RACE["SibaBabaCD"]
else:
	BabaCD = RACE["DirtBabaCD"]
#1000m通過時タイムの計算
if( int(RACE["Kyori"])%200 == 0 ):
	time1000m = int(RACE["LapTime1"])/10 + int(RACE["LapTime2"])/10 + int(RACE["LapTime3"])/10 + int(RACE["LapTime4"])/10 + int(RACE["LapTime5"])/10
else:
	time1000m = int(RACE["LapTime1"])/10 + int(RACE["LapTime2"])/10 + int(RACE["LapTime3"])/10 + int(RACE["LapTime4"])/10 + int(RACE["LapTime5"])/10 + int(RACE["LapTime6"])/10 /2

#文字列整形
text = "-----------------------------------------------------------------------------------------------------"+ "\n"
text += Year + Month + Day + " "
text += "第" + str(int(RACE["Nkai"])) + "回 "
text += RACE["Hondai"] + " "
text += getCodeValue( "2003", RACE["GradeCD"], 2) + " \n"
text += getCodeValue( "2001", RACE["JyoCD"], 1) + " "
text += getCodeValue( "2009", RACE["TrackCD"], 2) + " " 
text += RACE["Kyori"] +"[m] " 
text += getCodeValue( "2005", RACE["SyubetuCD"], 2) + " " 
text += getCodeValue( "2008", RACE["JyuryoCD"], 1) + " " 
text += getCodeValue( "2006", RACE["KigoCD"], 1) + " "
text += getCodeValue( "2007", RACE["JyokenCD5"], 1) + "\n" 
text += "本賞金："
for i in range(5):
	n = str(i + 1)	
	if( i!=0 ): text += ", "
	text += str(int(int(RACE["Honsyokin" + n ])/100)) + "万円"
text += "\n"
text += "発走時刻：" + HassoTime + " / "
text += "天候：" + getCodeValue( "2011", RACE["TenkoCD"], 1) + " / "
text += "馬場：" + getCodeValue( "2010", BabaCD, 1) + " / "
text += "出走頭数：" + RACE["SyussoTosu"] + "\n"
text +="-----------------------------------------------------------------------------------------------------"+ "\n"
text += "勝ちタイム：" + UMA_RACEs[0]["Time"][0] + ":" + UMA_RACEs[0]["Time"][1] + UMA_RACEs[0]["Time"][2] + "." + UMA_RACEs[0]["Time"][3] + " / "
text += "上がり4F：" + str(int(RACE["HaronTimeL3"])/10) + "秒 / "
text += "上がり3F：" + str(int(RACE["HaronTimeL3"])/10) + "秒 / "
text += "1000m通過時：" + str(time1000m) + "秒\n"
text += "ラップタイム："
for i in range(25):
	strLapTime = "LapTime" + str(i+1)
	if( RACE[strLapTime] != "000" ):
		if( i > 0 ): text += "-"
		text += str(int(RACE[strLapTime])/10)
text += "\n"
#コーナー通過順位
for i in range(4):
	n = str(i+1)
	if( RACE["Corner" + n] != "0" ): text += "第" + RACE["Corner" + n] + "コーナー : "  + RACE["Jyuni" + n] + "\n"

text +="-----------------------"+ "\n"
#出走馬ごとに
for UMA_RACE in UMA_RACEs:
	#文字列整形
	text += str(int(UMA_RACE["KakuteiJyuni"])) + "着 "
	text += UMA_RACE["Wakuban"] + "枠"
	text += UMA_RACE["Umaban"] + "番 "
	text += UMA_RACE["Bamei"]
	text += "（" + str(int(UMA_RACE["Jyuni1c"])) + "-" + str(int(UMA_RACE["Jyuni2c"]))
	text += "-" + str(int(UMA_RACE["Jyuni3c"])) + "-" + str(int(UMA_RACE["Jyuni4c"])) + "）"
	text += " タイム差：" + str(int(UMA_RACE["TimeDiff"])/10) + "秒"
	text += " 上がり3F：" + str(int(UMA_RACE["HaronTimeL3"])/10) + "秒"
	if(UMA_RACE["KyakusituKubun"] == "1"): kyakusitu = "逃"
	if(UMA_RACE["KyakusituKubun"] == "2"): kyakusitu = "先"
	if(UMA_RACE["KyakusituKubun"] == "3"): kyakusitu = "差"
	if(UMA_RACE["KyakusituKubun"] == "4"): kyakusitu = "追"
	text += " 脚質：" + kyakusitu + "\n"

text +="-----------------------"+ "\n"
text += "単勝："

for i in range(3):
	n = str(i + 1)
	if(HARAI["PayTansyoUmaban" + n] !=""):
		text += str(int(HARAI["PayTansyoUmaban" + n])) + "番 " + str(int(HARAI["PayTansyoPay" + n])) + "円（" + str(int(HARAI["PayTansyoNinki" + n])) + "人気） "
text += "\n"
text += "複勝："
for i in range(5):
	n = str(i + 1)
	if(HARAI["PayFukusyoUmaban" + n] !=""):
		text += str(int(HARAI["PayFukusyoUmaban" + n])) + "番 " + str(int(HARAI["PayFukusyoPay" + n])) + "円（" + str(int(HARAI["PayFukusyoNinki" + n])) + "人気） "
text += "\n"
text += "枠連："
for i in range(3):
	n = str(i + 1)
	kumi = HARAI["PayWakurenKumi" + n]
	if(kumi !=""):
		text += kumi[0] + "-" + kumi[1] + "  " + str(int(HARAI["PayWakurenPay" + n])) + "円（" + str(int(HARAI["PayWakurenNinki" + n])) + "人気） "
text += "\n"
text += "馬連："
for i in range(3):
	n = str(i + 1)
	kumi = HARAI["PayUmarenKumi" + n]	
	if( kumi !=""):
		text += str(int(kumi[0] + kumi[1])) + "-" + str(int(kumi[2] + kumi[3])) + "  " + str(int(HARAI["PayUmarenPay" + n])) + "円（" + str(int(HARAI["PayUmarenNinki" + n])) + "人気） "
text += "\n"
text += "ワイド："
for i in range(7):
	n = str(i + 1)
	kumi = HARAI["PayWideKumi" + n]	
	if( kumi !=""):
		text += str(int(kumi[0] + kumi[1])) + "-" + str(int(kumi[2] + kumi[3])) + "  " + str(int(HARAI["PayWidePay" + n])) + "円（" + str(int(HARAI["PayWideNinki" + n])) + "人気） "
text += "\n"
text += "3連複："
for i in range(3):
	n = str(i + 1)
	kumi = HARAI["PaySanrenpukuKumi" + n]	
	if( kumi !=""):	
		text += str(int(kumi[0] + kumi[1])) + "-" + str(int(kumi[2] + kumi[3])) + "-" + str(int(kumi[4] + kumi[5])) + "  " + str(int(HARAI["PaySanrenpukuPay" + n])) + "円（" + str(int(HARAI["PaySanrenpukuNinki" + n])) + "人気） "
text += "\n"
text += "3連単："
for i in range(6):
	n = str(i + 1)
	kumi = HARAI["PaySanrentanKumi" + n]	
	if( kumi !=""):	
		text += str(int(kumi[0] + kumi[1])) + "-" + str(int(kumi[2] + kumi[3])) + "-" + str(int(kumi[4] + kumi[5])) + "  " + str(int(HARAI["PaySanrentanPay" + n])) + "円（" + str(int(HARAI["PaySanrentanNinki" + n])) + "人気） "
text += "\n"

#ターミナルへ出力
print(text)


