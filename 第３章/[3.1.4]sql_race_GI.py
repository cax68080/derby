#モジュールのインポート
import sqlite3
#データベースへの接続
connection = sqlite3.connect("../ecore_2019.db")
#カーソルオブジェクトの生成
cursor = connection.cursor()

#カラム名リスト
N_RACE_ColumnNames = []
#カラム名リストの生成
for row in cursor.execute("pragma table_info(N_RACE)"):
	N_RACE_ColumnNames.append(row[1])

#レース情報リスト
RACEs = []
#SQL文
strSQL_SELECT = "SELECT * FROM N_RACE"
strSQL_WHERE  = " WHERE DataKubun = '7'"
strSQL_WHERE += " AND Year = '2019'"
strSQL_WHERE += " AND GradeCD ='A'"
strSQL_ORDER  = " ORDER BY JyoCD DESC, MonthDay ASC"
#SQL文の連結
strSQL = strSQL_SELECT + strSQL_WHERE + strSQL_ORDER 
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

#レースごとに
for RACE in RACEs:
	#年月日の取得
	Year = RACE["Year"] + "年"
	MonthDay = RACE["MonthDay"]
	Month = MonthDay[0] + MonthDay[1] + "月"
	Day = MonthDay[2] + MonthDay[3] + "日"
	#文字列整形
	text = ""
	text += Year + Month + Day + " "
	text += "第" + str(int(RACE["Nkai"])) + "回 "
	text += RACE["Hondai"] + " "
	text += getCodeValue( "2001", RACE["JyoCD"], 4) + " "
	text += getCodeValue( "2009", RACE["TrackCD"], 2) + " " 
	text +=  RACE["Kyori"] +"[m] " 
	text += getCodeValue( "2005", RACE["SyubetuCD"], 2) + " " 
	text += getCodeValue( "2008", RACE["JyuryoCD"], 1) + " " 
	text += getCodeValue( "2006", RACE["KigoCD"], 1) + " " 
	#ターミナルへ出力
	print(text)

