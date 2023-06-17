#独自ライブラリのインポート
import utility as U

#2019年有馬記念
Year = "2019"
MonthDay = "1222"

#SQL文
strSQL_SELECT = "SELECT * FROM N_UMA_RACE"
strSQL_WHERE  = " WHERE DataKubun = '7'"
strSQL_WHERE += " AND Year = '" + Year + "'"
strSQL_WHERE += " AND MonthDay = '" + MonthDay + "'"
strSQL_WHERE += " AND JyoCD = '06'"
strSQL_WHERE += " AND RaceNum ='11'"
strSQL_ORDER  = " ORDER BY Umaban ASC"
#SQL文の連結
strSQL = strSQL_SELECT + strSQL_WHERE + strSQL_ORDER 

#該当競走馬を取得
UMA_RACEs = U.getUMA_RACEs(strSQL)

#出走馬ごとに
for UMA_RACE in UMA_RACEs:
	#血統番号
	KettoNum = UMA_RACE["KettoNum"]
	#前走馬レース情報を取得
	zensoUMA_RACE = U.getZensoUMA_RACE( KettoNum, Year, MonthDay, False )
	#前走レース情報を取得
	zensoRACE = U.getZensoRACE( KettoNum, zensoUMA_RACE)
	#レース間隔を取得
	raceInterval = U.getRaceInterval( KettoNum, Year, MonthDay, zensoRACE)

	#前走の年月日
	z_Year = int(zensoRACE["Year"]) 
	z_MonthDay = zensoRACE["MonthDay"]
	z_Month = int(z_MonthDay[0] + z_MonthDay[1])
	z_Day = int(z_MonthDay[2] + z_MonthDay[3])

	#文字列整形
	text = ""
	text += UMA_RACE["Wakuban"] + "枠"
	text += UMA_RACE["Umaban"] + "番 "
	text += UMA_RACE["Bamei"]
	text += "　前走：" + str(z_Year) + "年" + str(z_Month) + "月" + str(z_Day) + "日" + zensoRACE["Hondai"]
	text += "（中" + str(raceInterval)  + "週）"

	#ターミナルへ出力
	print(text)

