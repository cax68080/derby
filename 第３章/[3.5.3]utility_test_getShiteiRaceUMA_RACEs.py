#独自ライブラリのインポート
import utility as U

#SQL文
strSQL_SELECT = "SELECT * FROM N_RACE"
strSQL_WHERE  = " WHERE DataKubun = '7'"
strSQL_WHERE += " AND Year = '2019'"
strSQL_WHERE += " AND MonthDay = '1222'"
strSQL_WHERE += " AND JyoCD ='06'"
strSQL_WHERE += " AND RaceNum ='11'"
#SQL文の連結
strSQL = strSQL_SELECT + strSQL_WHERE
#該当レースを取得
RACEs = U.getRACEs(strSQL)

#該当競走馬を取得
UMA_RACEs = U.getShiteiRaceUMA_RACEs( RACEs[0] )

#出走馬ごとに
for UMA_RACE in UMA_RACEs:
	#文字列整形
	text = ""
	text += UMA_RACE["Wakuban"] + "枠"
	text += UMA_RACE["Umaban"] + "番 "
	text += UMA_RACE["Bamei"] + "（"
	text += U.getCodeValue( "2202", UMA_RACE["SexCD"], 1) + ", "
	text += str(int(UMA_RACE["Barei"])) + "歳）"
	text += UMA_RACE["BaTaijyu"] + "kg（"
	text += UMA_RACE["ZogenFugo"] + str(int(UMA_RACE["ZogenSa"])) + "）"
	text += str(int(UMA_RACE["Ninki"])) + "番人気 "
	text += str(int(UMA_RACE["Odds"])/10) + "倍 " 
	text += UMA_RACE["KisyuRyakusyo"] + "騎手 "
	text += str(int(UMA_RACE["Futan"])/10) + "kg"
	
	#ターミナルへ出力
	print(text)
