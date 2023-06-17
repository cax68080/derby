#時刻関連モジュールのインポート
import datetime
today = datetime.date.today()

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
N_RACE_ColumnNames = []
N_HARAI_ColumnNames = []
N_UMA_RACE_ColumnNames = []

#カラム名リストの生成
for row in cursor.execute("pragma table_info(N_RACE)"):
	N_RACE_ColumnNames.append(row[1])
for row in cursor.execute("pragma table_info(N_HARAI)"):
	N_HARAI_ColumnNames.append(row[1])
for row in cursor.execute("pragma table_info(N_UMA_RACE)"):
	N_UMA_RACE_ColumnNames.append(row[1])
for row in cursor.execute("pragma table_info(N_UMA)"):
	N_UMA_ColumnNames.append(row[1])

#指定した条件の馬マスタデータを取得
def getUMAs(strSQL):
	#レース情報リスト
	UMAs = []
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
	return UMAs

#指定した条件のレースリストを取得
def getRACEs(strSQL):
	#レース情報リスト
	RACEs = []
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
	return RACEs

#指定した条件の払い戻しリストを取得
def getHARAIs(strSQL):
	#払い戻し情報リスト
	HARAIs = []
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
	return HARAIs

#指定した条件の馬リストを取得
def getUMA_RACEs(strSQL):
	#馬リスト
	UMA_RACEs = []	
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
	return UMA_RACEs

###########################################################################
#指定したレースの払戻情報
def getHARAI( raceData ):
	strSQL_SELECT = "SELECT * FROM N_HARAI "
	strSQL_WHERE  = " WHERE DataKubun = '2'"
	strSQL_WHERE += " AND JyoCD = '" + raceData["JyoCD"] + "'"
	strSQL_WHERE += " AND Year = '" + raceData["Year"] + "'"
	strSQL_WHERE += " AND MonthDay = '" + raceData["MonthDay"] + "'"
	strSQL_WHERE += " AND RaceNum = '" + raceData["RaceNum"] + "'"
	strSQL = strSQL_SELECT + strSQL_WHERE
	HARAIs = getHARAIs(strSQL)
	return HARAIs[0]
	
#指定したレースの馬毎レース情報
def getShiteiRaceUMA_RACEs( RACE, ORDER_BY = "Umaban ASC" ):
	strSQL_SELECT = "SELECT * FROM N_UMA_RACE"
	strSQL_WHERE  = " WHERE DataKubun IN ('7', 'A', 'B')"
	strSQL_WHERE += " AND JyoCD = '" + RACE["JyoCD"] + "'"
	strSQL_WHERE += " AND Year = '" + RACE["Year"] + "'"
	strSQL_WHERE += " AND MonthDay = '" + RACE["MonthDay"] + "'"
	strSQL_WHERE += " AND RaceNum = '" + RACE["RaceNum"] + "'"
	if( ORDER_BY != "" ): strSQL_ORDER = " ORDER BY " + ORDER_BY
	strSQL = strSQL_SELECT + strSQL_WHERE + strSQL_ORDER
	UMA_RACEs = getUMA_RACEs(strSQL)
	return UMA_RACEs

###########################################################################
#指定した競走馬の過去レース一覧を取得
def getShiteiKettoNumUMA_RACEs( KettoNum, onlyJRA = True):
	strSQL_SELECT = "SELECT * FROM N_UMA_RACE"
	if(onlyJRA): strSQL_WHERE  = " WHERE DataKubun = '7'"
	else: strSQL_WHERE  = " WHERE DataKubun IN ('7', 'A', 'B')"
	strSQL_WHERE += " AND KettoNum = '" + KettoNum + "'" 
	strSQL_ORDER = " ORDER BY Year DESC, MonthDay DESC"
	strSQL = strSQL_SELECT + strSQL_WHERE + strSQL_ORDER
	UMA_RACEs = getUMA_RACEs(strSQL)
	return UMA_RACEs


#指定した競走馬の前走データを取得
def getZensoUMA_RACE( KettoNum, Year, MonthDay, onlyJRA = True):
	strSQL_SELECT = "SELECT * FROM N_UMA_RACE"
	if(onlyJRA): strSQL_WHERE  = " WHERE DataKubun = '7'"
	else: strSQL_WHERE  = " WHERE DataKubun IN ('7', 'A', 'B')"
	strSQL_WHERE += " AND KettoNum = '" + KettoNum + "'" 
	strSQL_WHERE += " AND ( (Year < '" + Year + "' )" 
	strSQL_WHERE += "        OR (Year = '" + Year + "' AND MonthDay < '" + MonthDay + "') )"
	strSQL_ORDER = " ORDER BY Year DESC, MonthDay DESC"
	strSQL = strSQL_SELECT + strSQL_WHERE + strSQL_ORDER
	UMA_RACEs = getUMA_RACEs(strSQL)
	if( len(UMA_RACEs) == 0 ): return False

	#直近レースを取得
	for UMA_RACE in UMA_RACEs:
		Ninki = UMA_RACE["Ninki"]
		if(Ninki == "00" and onlyJRA): continue
		return UMA_RACE
	return False

#指定した競走馬の前走レースデータを取得
def getZensoRACE( KettoNum, zensoUMA_RACE):
	strSQL_SELECT = "SELECT * FROM N_RACE"
	strSQL_WHERE  = " WHERE DataKubun IN ('7', 'A', 'B')"
	strSQL_WHERE += " AND JyoCD = '" + zensoUMA_RACE["JyoCD"] + "'"
	strSQL_WHERE += " AND Year = '" + zensoUMA_RACE["Year"] + "'"
	strSQL_WHERE += " AND Kaiji = '" + zensoUMA_RACE["Kaiji"] + "'"
	strSQL_WHERE += " AND Nichiji = '" + zensoUMA_RACE["Nichiji"] + "'"
	strSQL_WHERE += " AND RaceNum = '" + zensoUMA_RACE["RaceNum"] + "'"
	strSQL = strSQL_SELECT + strSQL_WHERE 
	RACEs = getRACEs(strSQL)
	if( len(RACEs) == 0 ): return False
	#該当レースを取得
	return RACEs[0]

#指定した競走馬のレース間隔を取得する
def getRaceInterval( KettoNum, Year, MonthDay, zensoData = False):

	if( zensoData == False ):
		#前走馬レース情報を取得（JRA＋地方＋海外）
		zensoData = getZensoUMA_RACE( KettoNum, Year, MonthDay, False)
	if( zensoData == False ): return False

	#基準年月日
	n_Year = int(Year)
	n_Month = int(MonthDay[0] + MonthDay[1])
	n_Day = int(MonthDay[2] + MonthDay[3])
	n_datetime = datetime.date(n_Year, n_Month, n_Day)

	#前走年月日
	z_Year = int(zensoData["Year"])
	z_MonthDay = zensoData["MonthDay"]
	z_Month = int(z_MonthDay[0] + z_MonthDay[1])
	z_Day = int(z_MonthDay[2] + z_MonthDay[3])
	z_datetime = datetime.date(z_Year, z_Month, z_Day)

	#間隔（日単位）
	interval = n_datetime - z_datetime
	#間隔（週単位）
	interval_week = int( (interval.days + 1) / 7 ) - 1

	if(interval_week == -1): interval_week = 0

	return interval_week

def getRaceIntervalByList( KettoNum, Year, MonthDay, List):
	if(len(List) == 0): return False

	#基準年月日
	n_Year = int(Year)
	n_Month = int(MonthDay[0] + MonthDay[1])
	n_Day = int(MonthDay[2] + MonthDay[3])
	n_datetime = datetime.date(n_Year, n_Month, n_Day)

	#前走年月日
	z_Year = int(List[0]["Year"])
	z_MonthDay = List[0]["MonthDay"]
	z_Month = int(z_MonthDay[0] + z_MonthDay[1])
	z_Day = int(z_MonthDay[2] + z_MonthDay[3])
	z_datetime = datetime.date(z_Year, z_Month, z_Day)

	#間隔（日単位）
	interval = n_datetime - z_datetime

	if(interval.days > 0):
		#間隔（週単位）
		interval_week = int( (interval.days + 1) / 7 ) - 1
		if(interval_week == -1): interval_week = 0
		return interval_week
	else:

		for l in range(len(List)):
			list = List[l]

			if(list["Year"] == Year and list["MonthDay"] == MonthDay):
				if( l == len(List) - 1): 
					return False
				else:
					list = List[l+1]
					#前走年月日
					z_Year = int(list["Year"])
					z_MonthDay = list["MonthDay"]
					z_Month = int(z_MonthDay[0] + z_MonthDay[1])
					z_Day = int(z_MonthDay[2] + z_MonthDay[3])
					z_datetime = datetime.date(z_Year, z_Month, z_Day)

					#間隔（日単位）
					interval = n_datetime - z_datetime
					#間隔（週単位）
					interval_week = int( (interval.days + 1) / 7 ) - 1

					if(interval_week == -1): interval_week = 0

					return interval_week


#指定した競走馬の前走の上がり順位
def getZensoAgariJyuni( KettoNum, zensoData ):

	#該当レースの馬毎レース情報を取得
	UMA_RACEs = getShiteiRaceUMA_RACEs( zensoData )

	#該当レースの出走馬の血統番号と上がりタイムを格納
	HaronTimeL3s = {}
	for i in range(len(UMA_RACEs)):
		HaronTimeL3s[UMA_RACEs[i]["KettoNum"]] = int(UMA_RACEs[i]["HaronTimeL3"])
		if( UMA_RACEs[i]["KettoNum"] == KettoNum ): 
			myHaronTimeL3 = int(UMA_RACEs[i]["HaronTimeL3"])

	#上がりタイムが設定されていない場合
	if(myHaronTimeL3 == 0): return False

	#上がりタイムで並び替え
	HaronTimeL3s_sorted = sorted(HaronTimeL3s.items(), key=lambda x:x[1])
	#並び替えた結果との比較
	for i in range(len(HaronTimeL3s_sorted)):
		if( myHaronTimeL3 == HaronTimeL3s_sorted[i][1] ):
			return i + 1


#指定した馬の過去レースから脚質を判定
def getUmaKyakushitu( KettoNum , Year = "", MonthDay = "", num = 10):
	if( Year == "" or MonthDay == "" ):
		strSQL_SELECT = "SELECT * FROM N_UMA"
		strSQL_WHERE  = " WHERE KettoNum = '" + KettoNum + "'"
		strSQL = strSQL_SELECT + strSQL_WHERE
		UMAs = getUMAs(strSQL)
		#馬情報
		UMA = UMAs[0]
		#過去の脚質を取得
		RaceCount = int(UMA["RaceCount"])   # レース数
		Kyakusitu1 = int(UMA["Kyakusitu1"]) #「逃げ」回数
		Kyakusitu2 = int(UMA["Kyakusitu2"]) #「先行」回数
		Kyakusitu3 = int(UMA["Kyakusitu3"]) #「差し」回数
		Kyakusitu4 = int(UMA["Kyakusitu4"]) #「追込」回数
	else:
		strSQL_SELECT = "SELECT * FROM N_UMA_RACE"
		strSQL_WHERE  = " WHERE DataKubun = '7'"
		strSQL_WHERE += " AND KettoNum = '" + KettoNum + "'" 
		strSQL_WHERE += " AND ( (Year < '" + Year + "' )" 
		strSQL_WHERE += "        OR (Year = '" + Year + "' AND MonthDay < '" + MonthDay + "') )"
		strSQL_ORDER = " ORDER BY Year DESC, MonthDay DESC"
		strSQL = strSQL_SELECT + strSQL_WHERE + strSQL_ORDER
		UMA_RACEs = getUMA_RACEs(strSQL)
		RaceCount = 0  # レース数
		Kyakusitu1 = 0 #「逃げ」回数
		Kyakusitu2 = 0 #「先行」回数
		Kyakusitu3 = 0 #「差し」回数
		Kyakusitu4 = 0 #「追込」回数
		for i in range(len(UMA_RACEs)):
			#過去の脚質を取得
			if( UMA_RACEs[i]["KyakusituKubun"] == "0" ) : continue
			if( UMA_RACEs[i]["KyakusituKubun"] == "1" ) : Kyakusitu1 += 1
			if( UMA_RACEs[i]["KyakusituKubun"] == "2" ) : Kyakusitu2 += 1
			if( UMA_RACEs[i]["KyakusituKubun"] == "3" ) : Kyakusitu3 += 1
			if( UMA_RACEs[i]["KyakusituKubun"] == "4" ) : Kyakusitu4 += 1
			RaceCount += 1
			if( RaceCount == num ): break
	#レース数が０の場合
	if( RaceCount == 0): return 0

	#逃げ・先行
	if(Kyakusitu1 + Kyakusitu2 > Kyakusitu3 + Kyakusitu4):
		if(Kyakusitu1 >= Kyakusitu2 ): Kyakusitu = 1
		else: Kyakusitu = 2
	else: # 差し・追込
		if(Kyakusitu3 > Kyakusitu4 ): Kyakusitu = 3
		else: Kyakusitu = 4

	return Kyakusitu




###########################################################################
# 競馬場ごとのコース情報が格納された辞書型
Courses = {}
#札幌競馬場
Courses["01"] = [] 
Courses["01"].append( { "TrackCD" : "17" , "Kyori" : "1200" } ) #芝・右
Courses["01"].append( { "TrackCD" : "17" , "Kyori" : "1500" } ) #芝・右
Courses["01"].append( { "TrackCD" : "17" , "Kyori" : "1800" } ) #芝・右
Courses["01"].append( { "TrackCD" : "17" , "Kyori" : "2000" } ) #芝・右
Courses["01"].append( { "TrackCD" : "17" , "Kyori" : "2600" } ) #芝・右
Courses["01"].append( { "TrackCD" : "24" , "Kyori" : "1000" } ) #ダート・右
Courses["01"].append( { "TrackCD" : "24" , "Kyori" : "1700" } ) #ダート・右
Courses["01"].append( { "TrackCD" : "24" , "Kyori" : "2400" } ) #ダート・右
#函館競馬場
Courses["02"] = [] 
Courses["02"].append( { "TrackCD" : "17" , "Kyori" : "1000" } ) #芝・右（殆どなし）
Courses["02"].append( { "TrackCD" : "17" , "Kyori" : "1200" } ) #芝・右
Courses["02"].append( { "TrackCD" : "17" , "Kyori" : "1800" } ) #芝・右
Courses["02"].append( { "TrackCD" : "17" , "Kyori" : "2000" } ) #芝・右
Courses["02"].append( { "TrackCD" : "17" , "Kyori" : "2600" } ) #芝・右
Courses["02"].append( { "TrackCD" : "24" , "Kyori" : "1000" } ) #ダート・右
Courses["02"].append( { "TrackCD" : "24" , "Kyori" : "1700" } ) #ダート・右
Courses["02"].append( { "TrackCD" : "24" , "Kyori" : "2400" } ) #ダート・右
#福島競馬場
Courses["03"] = [] 
Courses["03"].append( { "TrackCD" : "17" , "Kyori" : "1200" } ) #芝・右
Courses["03"].append( { "TrackCD" : "17" , "Kyori" : "1800" } ) #芝・右
Courses["03"].append( { "TrackCD" : "17" , "Kyori" : "2000" } ) #芝・右
Courses["03"].append( { "TrackCD" : "17" , "Kyori" : "2600" } ) #芝・右
Courses["03"].append( { "TrackCD" : "24" , "Kyori" : "1150" } ) #ダート・右
Courses["03"].append( { "TrackCD" : "24" , "Kyori" : "1700" } ) #ダート・右
Courses["03"].append( { "TrackCD" : "24" , "Kyori" : "2400" } ) #ダート・右（殆どなし）
#新潟競馬場
Courses["04"] = [] 
Courses["04"].append( { "TrackCD" : "10" , "Kyori" : "1000" } ) #直線
Courses["04"].append( { "TrackCD" : "11" , "Kyori" : "1200" } ) #芝・左・内回り
Courses["04"].append( { "TrackCD" : "11" , "Kyori" : "1400" } ) #芝・左・内回り
Courses["04"].append( { "TrackCD" : "11" , "Kyori" : "2000" } ) #芝・左・内回り
Courses["04"].append( { "TrackCD" : "11" , "Kyori" : "2200" } ) #芝・左・内回り
Courses["04"].append( { "TrackCD" : "11" , "Kyori" : "2400" } ) #芝・左・内回り
Courses["04"].append( { "TrackCD" : "12" , "Kyori" : "1600" } ) #芝・左・外回り
Courses["04"].append( { "TrackCD" : "12" , "Kyori" : "1800" } ) #芝・左・外回り
Courses["04"].append( { "TrackCD" : "12" , "Kyori" : "2000" } ) #芝・左・外回り
Courses["04"].append( { "TrackCD" : "23" , "Kyori" : "1200" } ) #ダート・左
Courses["04"].append( { "TrackCD" : "23" , "Kyori" : "1800" } ) #ダート・左
Courses["04"].append( { "TrackCD" : "23" , "Kyori" : "2500" } ) #ダート・左（殆どなし）
#東京競馬場
Courses["05"] = [] 
Courses["05"].append( { "TrackCD" : "11" , "Kyori" : "1400" } ) #芝・左
Courses["05"].append( { "TrackCD" : "11" , "Kyori" : "1600" } ) #芝・左
Courses["05"].append( { "TrackCD" : "11" , "Kyori" : "1800" } ) #芝・左
Courses["05"].append( { "TrackCD" : "11" , "Kyori" : "2000" } ) #芝・左
Courses["05"].append( { "TrackCD" : "11" , "Kyori" : "2300" } ) #芝・左（殆どなし）
Courses["05"].append( { "TrackCD" : "11" , "Kyori" : "2400" } ) #芝・左
Courses["05"].append( { "TrackCD" : "11" , "Kyori" : "2500" } ) #芝・左（殆どなし）
Courses["05"].append( { "TrackCD" : "11" , "Kyori" : "3400" } ) #芝・左（殆どなし）
Courses["05"].append( { "TrackCD" : "23" , "Kyori" : "1300" } ) #ダート・左
Courses["05"].append( { "TrackCD" : "23" , "Kyori" : "1400" } ) #ダート・左
Courses["05"].append( { "TrackCD" : "23" , "Kyori" : "1600" } ) #ダート・左
Courses["05"].append( { "TrackCD" : "23" , "Kyori" : "2100" } ) #ダート・左
Courses["05"].append( { "TrackCD" : "23" , "Kyori" : "2400" } ) #ダート・左（殆どなし）
#中山競馬場
Courses["06"] = [] 
Courses["06"].append( { "TrackCD" : "17" , "Kyori" : "1800" } ) #芝・右
Courses["06"].append( { "TrackCD" : "17" , "Kyori" : "2000" } ) #芝・右
Courses["06"].append( { "TrackCD" : "17" , "Kyori" : "2500" } ) #芝・右
Courses["06"].append( { "TrackCD" : "18" , "Kyori" : "1200" } ) #芝・右・外回り
Courses["06"].append( { "TrackCD" : "18" , "Kyori" : "1600" } ) #芝・右・外回り
Courses["06"].append( { "TrackCD" : "18" , "Kyori" : "2200" } ) #芝・右・外回り
Courses["06"].append( { "TrackCD" : "21" , "Kyori" : "3600" } ) #芝・右・２周
Courses["06"].append( { "TrackCD" : "24" , "Kyori" : "1200" } ) #ダート・右
Courses["06"].append( { "TrackCD" : "24" , "Kyori" : "1800" } ) #ダート・右
Courses["06"].append( { "TrackCD" : "24" , "Kyori" : "2400" } ) #ダート・右
Courses["06"].append( { "TrackCD" : "24" , "Kyori" : "2500" } ) #ダート・右（殆どなし）
#中京競馬場
Courses["07"] = [] 
Courses["07"].append( { "TrackCD" : "11" , "Kyori" : "1200" } ) #芝・左
Courses["07"].append( { "TrackCD" : "11" , "Kyori" : "1400" } ) #芝・左
Courses["07"].append( { "TrackCD" : "11" , "Kyori" : "1600" } ) #芝・左
Courses["07"].append( { "TrackCD" : "11" , "Kyori" : "2000" } ) #芝・左
Courses["07"].append( { "TrackCD" : "11" , "Kyori" : "2200" } ) #芝・左
Courses["07"].append( { "TrackCD" : "23" , "Kyori" : "1200" } ) #ダート・左
Courses["07"].append( { "TrackCD" : "23" , "Kyori" : "1400" } ) #ダート・左
Courses["07"].append( { "TrackCD" : "23" , "Kyori" : "1800" } ) #ダート・左
Courses["07"].append( { "TrackCD" : "23" , "Kyori" : "1900" } ) #ダート・左
#京都競馬場
Courses["08"] = [] 
Courses["08"].append( { "TrackCD" : "17" , "Kyori" : "1200" } ) #芝・右・内回り
Courses["08"].append( { "TrackCD" : "17" , "Kyori" : "1400" } ) #芝・右・内回り
Courses["08"].append( { "TrackCD" : "17" , "Kyori" : "1600" } ) #芝・右・内回り
Courses["08"].append( { "TrackCD" : "17" , "Kyori" : "2000" } ) #芝・右・内回り
Courses["08"].append( { "TrackCD" : "18" , "Kyori" : "1400" } ) #芝・右・外回り
Courses["08"].append( { "TrackCD" : "18" , "Kyori" : "1600" } ) #芝・右・外回り
Courses["08"].append( { "TrackCD" : "18" , "Kyori" : "1800" } ) #芝・右・外回り
Courses["08"].append( { "TrackCD" : "18" , "Kyori" : "2200" } ) #芝・右・外回り
Courses["08"].append( { "TrackCD" : "18" , "Kyori" : "2400" } ) #芝・右・外回り
Courses["08"].append( { "TrackCD" : "18" , "Kyori" : "3000" } ) #芝・右・外回り（殆どなし）
Courses["08"].append( { "TrackCD" : "18" , "Kyori" : "3200" } ) #芝・右・外回り（殆どなし）
Courses["08"].append( { "TrackCD" : "24" , "Kyori" : "1200" } ) #ダート・右
Courses["08"].append( { "TrackCD" : "24" , "Kyori" : "1400" } ) #ダート・右
Courses["08"].append( { "TrackCD" : "24" , "Kyori" : "1800" } ) #ダート・右
Courses["08"].append( { "TrackCD" : "24" , "Kyori" : "1900" } ) #ダート・右
#阪神競馬場
Courses["09"] = [] 
Courses["09"].append( { "TrackCD" : "17" , "Kyori" : "1200" } ) #芝・右・内回り
Courses["09"].append( { "TrackCD" : "17" , "Kyori" : "1400" } ) #芝・右・内回り
Courses["09"].append( { "TrackCD" : "17" , "Kyori" : "2000" } ) #芝・右・内回り
Courses["09"].append( { "TrackCD" : "17" , "Kyori" : "2200" } ) #芝・右・内回り
Courses["09"].append( { "TrackCD" : "17" , "Kyori" : "3000" } ) #芝・右（殆どなし）
Courses["09"].append( { "TrackCD" : "18" , "Kyori" : "1600" } ) #芝・右・外回り
Courses["09"].append( { "TrackCD" : "18" , "Kyori" : "1800" } ) #芝・右・外回り
Courses["09"].append( { "TrackCD" : "18" , "Kyori" : "2400" } ) #芝・右・外回り
Courses["09"].append( { "TrackCD" : "18" , "Kyori" : "2600" } ) #芝・右・外回り（殆どなし）
Courses["09"].append( { "TrackCD" : "24" , "Kyori" : "1200" } ) #ダート・右
Courses["09"].append( { "TrackCD" : "24" , "Kyori" : "1400" } ) #ダート・右
Courses["09"].append( { "TrackCD" : "24" , "Kyori" : "1800" } ) #ダート・右
Courses["09"].append( { "TrackCD" : "24" , "Kyori" : "2000" } ) #ダート・右
#小倉競馬場
Courses["10"] = [] 
Courses["10"].append( { "TrackCD" : "17" , "Kyori" : "1200" } ) #芝・右
Courses["10"].append( { "TrackCD" : "17" , "Kyori" : "1700" } ) #芝・右（殆どなし）
Courses["10"].append( { "TrackCD" : "17" , "Kyori" : "1800" } ) #芝・右
Courses["10"].append( { "TrackCD" : "17" , "Kyori" : "2000" } ) #芝・右
Courses["10"].append( { "TrackCD" : "17" , "Kyori" : "2600" } ) #芝・右
Courses["10"].append( { "TrackCD" : "24" , "Kyori" : "1000" } ) #ダート・右
Courses["10"].append( { "TrackCD" : "24" , "Kyori" : "1700" } ) #ダート・右
Courses["10"].append( { "TrackCD" : "24" , "Kyori" : "2400" } ) #ダート・右（殆どなし）
