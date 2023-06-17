#モジュールのインポート
import sqlite3
#データベースへの接続
connection = sqlite3.connect("E:\Documents\競馬\everydb2.2\Application Files\EveryDB2.2_2_2_0_0\ecore.db")
#カーソルオブジェクトの生成
cursor = connection.cursor()

#コード表リスト
CodeTable = []
#外部ファイルの読み込み
f_in = open('./CodeTable.csv')
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

#騎手コード（武豊騎手）
KisyuCode = "00666"

#レース情報リスト
UMA_RACEs = []
#SQL文
strSQL_SELECT = "SELECT * FROM N_UMA_RACE"
strSQL_WHERE  = " WHERE DataKubun = '7'"
strSQL_WHERE += " AND Year = '2022'"
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

#print (UMA_RACEs[0])

#着度数集計用配列
tyaku_dosu = [0] * 5
#配当合計計算用変数
haito_sum = 0

#レースごとに
for UMA_RACE in UMA_RACEs:

	MonthDay = UMA_RACE["MonthDay"]
	Month = MonthDay[0] + MonthDay[1]
	Day = MonthDay[2] + MonthDay[3]

	Jyuni = int(UMA_RACE["KakuteiJyuni"])
	if(Jyuni<=3):
		tyaku_dosu[Jyuni] += 1
	else:
		tyaku_dosu[4] += 1

	if(Jyuni == 1):
		haito_sum += int(UMA_RACE["Odds"])*10

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
	print(text)

#レース数
tyaku_dosu[0] = tyaku_dosu[1] + tyaku_dosu[2] + tyaku_dosu[3] + tyaku_dosu[4]
#成績を出力
print("---------------------------------------------------------------------")
print( "成績：" + str(tyaku_dosu[1]) + "-" + str(tyaku_dosu[2]) + "-" + str(tyaku_dosu[3]) + "-" + str(tyaku_dosu[4]) + "|" + str(tyaku_dosu[0]) + "　勝率：" + str( round(tyaku_dosu[1]*100/tyaku_dosu[0],1) ) + "%"  +"　単勝回収率：" + str( round(haito_sum/tyaku_dosu[0],1) ) + "%" )


