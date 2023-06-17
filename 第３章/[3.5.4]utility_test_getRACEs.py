#独自ライブラリのインポート
import utility as U

#SQL文
strSQL_SELECT = "SELECT * FROM N_RACE"
strSQL_WHERE  = " WHERE DataKubun = '7'"
strSQL_WHERE += " AND Year = '2019'"
strSQL_WHERE += " AND GradeCD ='A'"
strSQL_ORDER  = " ORDER BY JyoCD DESC, MonthDay ASC"
#SQL文の連結
strSQL = strSQL_SELECT + strSQL_WHERE + strSQL_ORDER

#該当レースを取得
RACEs = U.getRACEs(strSQL)

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
	text += U.getCodeValue( "2001", RACE["JyoCD"], 4) + " "
	text += U.getCodeValue( "2009", RACE["TrackCD"], 2) + " " 
	text += RACE["Kyori"] +"[m] " 
	text += U.getCodeValue( "2005", RACE["SyubetuCD"], 2) + " " 
	text += U.getCodeValue( "2008", RACE["JyuryoCD"], 1) + " " 
	text += U.getCodeValue( "2006", RACE["KigoCD"], 1) + " " 
	#ターミナルへ出力
	print(text)
