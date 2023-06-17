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
N_UMA_ColumnNames = []
#カラム名リストの生成
for row in cursor.execute("pragma table_info(N_UMA)"):
	N_UMA_ColumnNames.append(row[1])

#カラム名リスト
N_UMA_RACE_ColumnNames = []
#カラム名リストの生成
for row in cursor.execute("pragma table_info(N_UMA_RACE)"):
	N_UMA_RACE_ColumnNames.append(row[1])

#カラム名リスト
N_RACE_ColumnNames = []
#カラム名リストの生成
for row in cursor.execute("pragma table_info(N_RACE)"):
	N_RACE_ColumnNames.append(row[1])


#レース情報リスト
UMAs = []
#SQL文
strSQL_SELECT = "SELECT * FROM N_UMA"
strSQL_WHERE  = " WHERE KettoNum = '2014106220'"
#SQL文の連結
strSQL = strSQL_SELECT + strSQL_WHERE
#SQL文の実行
results = cursor.execute(strSQL)
#辞書型
for row in results:
	dic = {}
	for n in range(len(N_UMA_ColumnNames)):
		#辞書型へと変換
		dic[N_UMA_ColumnNames[n]] = row[n]
	#リストへの格納
	UMAs.append(dic)

UMA = UMAs[0]

import datetime
today = datetime.date.today()

b = UMA["BirthDate"]
b_year = int(b[0] + b[1] + b[2] + b[3])
barei = today.year - b_year

text ="-----------------------------------------------------------------------------------------------------"+ "\n"
text += "馬名 " + getCodeValue( "2204",  UMA["UmaKigoCD"] ,1) + UMA["Bamei"] + " "
text += getCodeValue( "2202", UMA["SexCD"], 1) + " " + str(barei) + "歳 " +  getCodeValue( "2203", UMA["KeiroCD"], 1) 
if(UMA["DelKubun"] == "0"): text += "（現役）"
if(UMA["DelKubun"] == "1"): text += "（抹消）"
text += "\n"
text +="-----------------------------------------------------------------------------------------------------"+ "\n"

text += "生年月日 " + str(b_year) + "年" + b[4] + b[5] + "月" + b[6] + b[7] + "日\n"
text += "調教師名 " + UMA["ChokyosiRyakusyo"] + "（" +  getCodeValue( "2301", UMA["TozaiCD"], 2) +  "）\n"
text += "生産者名 " + UMA["BreederName"] + "\n"
text += "産地名 " + UMA["SanchiName"] + "\n"
text += "馬主名 " + UMA["BanusiName"] + "\n"
text += "父" + UMA["Ketto3InfoBamei1"] + " （父父 "+ UMA["Ketto3InfoBamei3"] + "  父母 "+ UMA["Ketto3InfoBamei4"]  + "）\n"
text += "母 " + UMA["Ketto3InfoBamei2"] + " （母父 "+ UMA["Ketto3InfoBamei5"] + "  母母 " + UMA["Ketto3InfoBamei6"] + "）\n"

s = int(int(UMA["RuikeiHonsyoHeiti"])/100) + int(int(UMA["RuikeiFukaHeichi"])/100)
s1 = int(s / 10000)
s2 = s - s1 * 10000
text += "獲得賞金 " 
if(s1 > 0): text += str(s1) + "億"
text += str(s2) + "万円（中央のみ）\n"

SogoChakukaisu = int(UMA["SogoChakukaisu1"]) + int(UMA["SogoChakukaisu2"]) + int(UMA["SogoChakukaisu3"]) + int(UMA["SogoChakukaisu4"]) + int(UMA["SogoChakukaisu5"]) + int(UMA["SogoChakukaisu6"])

text += "通算成績" + " " + str(SogoChakukaisu) + "戦" + str(int(UMA["SogoChakukaisu1"])) + "勝 "
text += "[" + str(int(UMA["SogoChakukaisu1"])) + "-" + str(int(UMA["SogoChakukaisu2"])) + "-"
text += str(int(UMA["SogoChakukaisu3"])) + "-" + str(int(UMA["SogoChakukaisu4"])) + "-"
text += str(int(UMA["SogoChakukaisu5"])) + "-" + str(int(UMA["SogoChakukaisu6"])) + "]（中央＋地方＋海外)\n"

text += "脚質 [逃-先-差-追]：[" + str(int(UMA["Kyakusitu1"])) + "-" + str(int(UMA["Kyakusitu2"]))
text += "-" + str(int(UMA["Kyakusitu3"])) + "-" + str(int(UMA["Kyakusitu4"])) + "]" + "\n"
text +="-----------------------" + "\n"


#レース情報リスト
UMA_RACEs = []
#SQL文
strSQL_SELECT = "SELECT * FROM N_UMA_RACE"
strSQL_WHERE  = " WHERE DataKubun = '7'"
strSQL_WHERE += " AND KettoNum = '2014106220'"
strSQL_ORDER  = " ORDER BY Year ASC, MonthDay ASC"
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

#レースごとに
for UMA_RACE in UMA_RACEs:
	#レース情報リスト
	RACEs = []
	#SQL文
	strSQL_SELECT = "SELECT * FROM N_RACE"
	strSQL_WHERE  = " WHERE DataKubun = '7'"
	strSQL_WHERE += " AND Year = '" + UMA_RACE["Year"] + "'"
	strSQL_WHERE += " AND MonthDay = '" + UMA_RACE["MonthDay"] + "'"
	strSQL_WHERE += " AND JyoCD = '" + UMA_RACE["JyoCD"] + "'"
	strSQL_WHERE += " AND RaceNum = '" + UMA_RACE["RaceNum"] + "'"
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
	#該当レースの取得
	RACE = RACEs[0]

	#年月日の取得
	Year = RACE["Year"] + "年"
	MonthDay = RACE["MonthDay"]
	Month = MonthDay[0] + MonthDay[1] + "月"
	Day = MonthDay[2] + MonthDay[3] + "日"
	#テキストの整形
	text += Year + Month + Day + " "
	text += getCodeValue( "2001", RACE["JyoCD"], 4) + RACE["RaceNum"] + "R "
	if(RACE["Hondai"] != ""):
		text += RACE["Hondai"]
		if( RACE["GradeCD"] == "A" or RACE["GradeCD"] == "B" or RACE["GradeCD"] == "C" or RACE["GradeCD"] == "L"):
			text += "(" +  getCodeValue( "2003", RACE["GradeCD"], 2) + ") "
	else:
		if(RACE["JyokenCD5"] == "701"):
			text += "新馬戦 "
		elif(RACE["JyokenCD5"] == "703"):
			text += "未勝利戦 "
		elif(RACE["JyokenCD5"] == "005"):
			text += "１勝クラス "
		elif(RACE["JyokenCD5"] == "010"):
			text += "２勝クラス "
		elif(RACE["JyokenCD5"] == "016"):
			text += "３勝クラス "
	text += getCodeValue( "2009", RACE["TrackCD"], 2) + " " 
	text += RACE["Kyori"] +"[m] " 
	text += UMA_RACE["BaTaijyu"] + "kg "
	if( (UMA_RACE["ZogenSa"] == "999" or UMA_RACE["ZogenSa"] == "") == False ):
		text += "(" + UMA_RACE["ZogenFugo"] + str(int(UMA_RACE["ZogenSa"])) + "kg) "
	text += UMA_RACE["KisyuRyakusyo"] + "騎手 "
	text += str(int(UMA_RACE["Ninki"])) + "番人気 "
	text += str(int(UMA_RACE["Odds"])/10) + "倍 "
	text += str(int(UMA_RACE["KakuteiJyuni"])) + "着（" + str(int(UMA_RACE["TimeDiff"])/10) + "秒）"
	'''
	text += "（" + str(int(UMA_RACE["Jyuni1c"])) + "-" + str(int(UMA_RACE["Jyuni2c"]))
	text += "-" + str(int(UMA_RACE["Jyuni3c"])) + "-" + str(int(UMA_RACE["Jyuni4c"])) + "）"
	if(UMA_RACE["KyakusituKubun"] == "1"): text += "逃"
	if(UMA_RACE["KyakusituKubun"] == "2"): text += "先"
	if(UMA_RACE["KyakusituKubun"] == "3"): text += "差"
	if(UMA_RACE["KyakusituKubun"] == "4"): text += "追"
	'''
	text += "\n"

#ターミナルへ出力
print(text)



