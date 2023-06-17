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

#時刻関連モジュールのインポート
import datetime
today = datetime.date.today()
#print(type(today))
#テキストの整形
text = "騎手免許交付年順（" + "現役騎手：" + str(len(KISYUs)) + "人" + "）\n"
for n in range(len(KISYUs)):
	i = KISYUs[n]["IssueDate"]
	i_year = i[0] + i[1] + i[2] + i[3]

	#年齢計算用
	b = KISYUs[n]["BirthDate"]
	b_year = int(b[0] + b[1] + b[2] + b[3])
	b_month = int(b[4] + b[5])
	b_day = int(b[6] + b[7]) 
	nenrei = today - datetime.date(b_year, b_month, b_day)
	nenrei_year = int(nenrei.days/365)

	text += KISYUs[n]["KisyuName"] + "（" + KISYUs[n]["KisyuCode"] + "）"  + "\t" 
	text += str(b_year) + "年" +  str(b_month) + "月" + str(b_day) + "日生まれ" +"（" +str(nenrei_year) + "歳）\t" 
	text += "免許取得年：" + i_year + "年\t" 
	text += getCodeValue( "2301", KISYUs[n]["TozaiCD"], 1) + "\t"

	if(KISYUs[n]["ChokyosiRyakusyo"] == ""):
		text += "フリー\t"
	else:
		text += KISYUs[n]["ChokyosiRyakusyo"] + "厩舎\t"
	text += "\n"

#ターミナルへ出力
print(text)
