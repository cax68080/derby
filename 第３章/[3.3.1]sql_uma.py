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

#馬マスタデータ
UMA = UMAs[0]
#時刻関連モジュールのインポート
import datetime
today = datetime.date.today()
#馬齢計算
b = UMA["BirthDate"]
b_year = int(b[0] + b[1] + b[2] + b[3])
barei = today.year - b_year

#テキスト整形
text = ""
text += "馬名： " + getCodeValue( "2204",  UMA["UmaKigoCD"] ,1) + UMA["Bamei"] + " "
text += getCodeValue( "2202", UMA["SexCD"], 1) + " " + str(barei) + "歳 " +  getCodeValue( "2203", UMA["KeiroCD"], 1) 
if(UMA["DelKubun"] == "0"): text += "（現役）"
if(UMA["DelKubun"] == "1"): text += "（抹消）"
text += "\n"
text += "生年月日： " + str(b_year) + "年" + b[4] + b[5] + "月" + b[6] + b[7] + "日\n"
text += "調教師名： " + UMA["ChokyosiRyakusyo"] + "（" +  getCodeValue( "2301", UMA["TozaiCD"], 2) +  "）\n"
text += "生産者名： " + UMA["BreederName"] + "\n"
text += "産地名： " + UMA["SanchiName"] + "\n"
text += "馬主名： " + UMA["BanusiName"] + "\n"
text += "父： " + UMA["Ketto3InfoBamei1"] + " （父父： "+ UMA["Ketto3InfoBamei3"] + "  父母： "+ UMA["Ketto3InfoBamei4"]  + "）\n"
text += "母： " + UMA["Ketto3InfoBamei2"] + " （母父： "+ UMA["Ketto3InfoBamei5"] + "  母母： " + UMA["Ketto3InfoBamei6"] + "）\n"
#獲得賞金の整形
s = int(int(UMA["RuikeiHonsyoHeiti"])/100) + int(int(UMA["RuikeiFukaHeichi"])/100)
s1 = int(s / 10000)
s2 = s - s1 * 10000
text += "獲得賞金： " 
if(s1 > 0): text += str(s1) + "億"
text += str(s2) + "万円（中央のみ）\n"
#出走数の集計
sogoChakukaisu = int(UMA["SogoChakukaisu1"]) + int(UMA["SogoChakukaisu2"]) + int(UMA["SogoChakukaisu3"]) + int(UMA["SogoChakukaisu4"]) + int(UMA["SogoChakukaisu5"]) + int(UMA["SogoChakukaisu6"])
#着外回数
tyakugaiKaisu = int(UMA["SogoChakukaisu4"])+int(UMA["SogoChakukaisu5"])+int(UMA["SogoChakukaisu6"])
text += "通算成績： " + str(sogoChakukaisu) + "戦" + str(int(UMA["SogoChakukaisu1"])) + "勝 "
text += "[" + str(int(UMA["SogoChakukaisu1"])) + "-" + str(int(UMA["SogoChakukaisu2"])) + "-" + str(int(UMA["SogoChakukaisu3"])) + "-" + str(tyakugaiKaisu) + "]（1着-2着-3着-着外)\n"
text += "脚質： 逃：" + str(int(UMA["Kyakusitu1"])) + " 回  先：" + str(int(UMA["Kyakusitu2"])) + " 回  差：" + str(int(UMA["Kyakusitu3"])) + " 回  追：" + str(int(UMA["Kyakusitu4"])) + " 回\n"

#ターミナルへ出力
print(text)