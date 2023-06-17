#モジュールのインポート
import sqlite3
#データベースへの接続
connection = sqlite3.connect("../ecore_2019.db")
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
N_UMA_RACE_ColumnNames = []
#カラム名リストの生成
for row in cursor.execute("pragma table_info(N_UMA_RACE)"):
	N_UMA_RACE_ColumnNames.append(row[1])

#レース情報リスト
UMA_RACEs = []
#SQL文
strSQL_SELECT = "SELECT * FROM N_UMA_RACE"
strSQL_WHERE  = " WHERE DataKubun = '7'"
strSQL_WHERE += " AND Year = '2019'"
strSQL_WHERE += " AND MonthDay = '1222'"
strSQL_WHERE += " AND JyoCD ='06'"
#strSQL_WHERE += " AND Kaiji = '05'"
#strSQL_WHERE += " AND Nichiji = '08'"
strSQL_WHERE += " AND RaceNum ='11'"
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

#print (UMA_RACEs[0])

#出走馬ごとに
for UMA_RACE in UMA_RACEs:
	#文字列整形
	text = str(int(UMA_RACE["KakuteiJyuni"])) + "着 "
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
	text += " 脚質：" + kyakusitu
	#ターミナルへ出力
	print(text)


