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
N_KISYU_ColumnNames = []
#カラム名リストの生成
for row in cursor.execute("pragma table_info(N_KISYU)"):
	N_KISYU_ColumnNames.append(row[1])

#騎手情報リスト
KISYUs = []
#SQL文
strSQL = "SELECT * FROM N_KISYU WHERE DelKubun = '0' ORDER BY IssueDate ASC"
#SQL文の実行
results = cursor.execute(strSQL)

#辞書型
for row in results:
	dic = {}
	for n in range(len(N_KISYU_ColumnNames)):
		#辞書型へと変換
		dic[N_KISYU_ColumnNames[n]] = row[n]
	#リストへの格納
	KISYUs.append(dic)

#カラム名リスト
N_UMA_RACE_ColumnNames = []
#カラム名リストの生成
for row in cursor.execute("pragma table_info(N_UMA_RACE)"):
	N_UMA_RACE_ColumnNames.append(row[1])

#騎手辞書の作成
KisyuDic = {}
for n in range(len(KISYUs)):
	print( KISYUs[n]["KisyuName"] )
	KisyuCode = KISYUs[n]["KisyuCode"]

	#騎手コードに対して辞書型変数を宣言
	KisyuDic[ KisyuCode ] = {}
	#騎手名
	KisyuDic[ KisyuCode ]["name"] = KISYUs[n]["KisyuName"]
	#着度数集計用配列
	KisyuDic[ KisyuCode ]["tyaku_dosu"] = [0] * 5
	#配当合計計算用変数
	KisyuDic[ KisyuCode ]["haito_sum"] = 0

	#レース情報リスト
	UMA_RACEs = []
	#SQL文
	strSQL_SELECT = "SELECT * FROM N_UMA_RACE"
	strSQL_WHERE  = " WHERE DataKubun = '7'"
	strSQL_WHERE += " AND Year = '2020'"
	strSQL_WHERE += " AND KisyuCode = '" + KisyuCode + "'"
	strSQL_ORDER  = " ORDER BY MonthDay DESC, RaceNum DESC"
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

		MonthDay = UMA_RACE["MonthDay"]
		Month = MonthDay[0] + MonthDay[1]
		Day = MonthDay[2] + MonthDay[3]

		Jyuni = int(UMA_RACE["KakuteiJyuni"])
		if(Jyuni <= 3):
			KisyuDic[ KisyuCode ]["tyaku_dosu"][Jyuni] += 1
		else:
			KisyuDic[ KisyuCode ]["tyaku_dosu"][4] += 1

		if(Jyuni == 1):
			KisyuDic[ KisyuCode ]["haito_sum"] += int(UMA_RACE["Odds"])*10

		#文字列整形
		text = ""
		text += UMA_RACE["Year"] + "年"
		text += Month + "月"
		text += Day + "日"
		text += getCodeValue( "2001", UMA_RACE["JyoCD"], 4) 
		text += UMA_RACE["RaceNum"] + "レース"
		text += UMA_RACE["Wakuban"] + "枠"
		text += UMA_RACE["Umaban"] + "番 "
		text += UMA_RACE["Bamei"] + "（"
		text +=  getCodeValue( "2202", UMA_RACE["SexCD"], 1) + ", "
		text += str(int(UMA_RACE["Barei"])) + "歳）"
		text += UMA_RACE["BaTaijyu"] + "kg "
		text += str(int(UMA_RACE["Ninki"])) + "番人気 "
		text += str(int(UMA_RACE["Odds"])/10) + "倍 " 
		text += str(int(UMA_RACE["Futan"])/10) + "kg "
		text += str(Jyuni) + "着"
		
		#ターミナルへ出力
		#print(text)

#ランキング作成用辞書型変数
ranking = {}
for KisyuCode in KisyuDic:
	ranking[ KisyuCode ] = KisyuDic[ KisyuCode ]["tyaku_dosu"][1]

#並び替え（降順）
ranking_sorted = sorted(ranking.items(), key=lambda x:x[1], reverse=True)

print("---------------------------------------------------------------------")
#結果出力
for i in range(len(ranking_sorted)):
	KisyuCode = ranking_sorted[i][0]
	KisyuDic[ KisyuCode ]["ranking"] = i + 1
	#リストの参照
	d = KisyuDic[ KisyuCode ]["tyaku_dosu"]
	#レース数
	d[0] = d[1] + d[2] + d[3] + d[4]
	if(d[0] > 0):
		print(str(KisyuDic[ KisyuCode ]["ranking"]) + "位 " + str(KisyuDic[ KisyuCode ]["name"] ) +  "（" + str(d[1]) + "-" + str(d[2]) + "-" + str(d[3]) + "-" + str(d[4]) + "|" + str(d[0]) + "）　勝率：" + str( round(d[1]*100/d[0],1) ) + "%"  +"　単勝回収率：" + str( round(KisyuDic[ KisyuCode ]["haito_sum"]/d[0],1) ) + "%")


