#独自ライブラリのインポート
import utility as U

#東京競馬場１番人気（2010-2019）
JyoCD = "06"
Ninki = "01"
Years = [0] * 10
for n in range(len(Years)):
	Years[n] = str(2020 + n)

#レース結果を格納する辞書型
tyakuKaisu = {}
#単勝・複勝の的中回数を格納する辞書型
tansho_tekityuKaisu = {}
fukusho_tekityuKaisu = {}
#単勝・複勝の払戻総額を格納する辞書型
tansho_haraimodoshi_sum = {}
fukusho_haraimodoshi_sum = {}

for Year in Years:
	#レース結果格納する配列：総数, １着, ２着, ３着
	tyakuKaisu[Year] = [0] * 4
	#単勝・複勝の的中回数
	tansho_tekityuKaisu[Year] = 0
	fukusho_tekityuKaisu[Year] = 0
	#単勝・複勝の払戻総額
	tansho_haraimodoshi_sum[Year] = 0
	fukusho_haraimodoshi_sum[Year] = 0

	#SQL文
	strSQL_SELECT = "SELECT * FROM N_RACE"
	strSQL_WHERE  = " WHERE DataKubun = '7'"
	strSQL_WHERE += " AND Year = '" + Year + "'" 
	strSQL_WHERE += " AND JyoCD = '" + JyoCD + "'"
	strSQL_ORDER = " ORDER BY MonthDay ASC"
	#SQL文の連結
	strSQL = strSQL_SELECT + strSQL_WHERE + strSQL_ORDER
	#該当レースを取得
	RACEs = U.getRACEs(strSQL)

	for RACE in RACEs:
		#障害競走を除外
		if(int(RACE["TrackCD"]) >= 30): continue
		#払戻情報を取得
		HARAI = U.getHARAI(RACE)
		#該当レースの出走馬を取得（人気順）
		UMA_RACEs = U.getShiteiRaceUMA_RACEs( RACE, "Ninki ASC" )
		#1番人気
		for UMA_RACE in UMA_RACEs:
			if(UMA_RACE["Ninki"] == Ninki): break
		#文字列整形
		text = ""
		text += UMA_RACE["Year"] + UMA_RACE["MonthDay"] + " "
		text += UMA_RACE["RaceNum"] + "R "
		text += UMA_RACE["Bamei"] + " \t\t"
		text += str(int(UMA_RACE["Ninki"])) + "番人気 "
		text += "（" + str(int(UMA_RACE["Odds"])/10) + "倍）" 
		text += UMA_RACE["KakuteiJyuni"] + "位 "
		#レース結果を集計
		tyakuKaisu[Year][0] += 1
		if( int(UMA_RACE["KakuteiJyuni"]) <= 3):
			tyakuKaisu[Year][int(UMA_RACE["KakuteiJyuni"])] += 1
		#単勝的中の場合
		for i in range(3):
			n = str(i + 1)
			if(HARAI["PayTansyoUmaban" + n] == UMA_RACE["Umaban"]):
				tansho_haraimodoshi_sum[Year] += int(HARAI["PayTansyoPay" + n])
				tansho_tekityuKaisu[Year] += 1
		#複勝的中の場合
		for i in range(5):
			n = str(i + 1)
			if(HARAI["PayFukusyoUmaban" + n] == UMA_RACE["Umaban"]):
				fukusho_haraimodoshi_sum[Year] += int(HARAI["PayFukusyoPay" + n])
				fukusho_tekityuKaisu[Year] += 1
		#ターミナルへ出力
		#print(text)

	#着外の回数
	kyakugai = tyakuKaisu[Year][0] - tyakuKaisu[Year][1] - tyakuKaisu[Year][2]- tyakuKaisu[Year][3]
	#単勝の的中率と回収率
	if tyakuKaisu[Year][0] == 0:
		tanshou_ritsu = 0
	else:
		tanshou_ritsu = round(tyakuKaisu[Year][1] / tyakuKaisu[Year][0] * 100, 1)
	if tyakuKaisu[Year][0] == 0:
		tanshou_kaishuritsu = 0
	else:	
		tanshou_kaishuritsu = round(tansho_haraimodoshi_sum[Year] / tyakuKaisu[Year][0], 1)
	#複勝の的中率と回収率
	if tyakuKaisu[Year][0] == 0:
		fukusho_ritsu = 0
	else:	
		fukusho_ritsu = round(fukusho_tekityuKaisu[Year] / tyakuKaisu[Year][0] * 100, 1)
	if tyakuKaisu[Year][0] == 0:
		fukusho_kaishuritsu = 0
	else:	
		fukusho_kaishuritsu = round(fukusho_haraimodoshi_sum[Year] / tyakuKaisu[Year][0], 1)

	#文字列整形
	text = "----------------" + Year + "年----------------------\n"
	text += "1着-2着-3着-着外|該当レース数 ： "
	text += str(tyakuKaisu[Year][1]) + "-" + str(tyakuKaisu[Year][2]) + "-" + str(tyakuKaisu[Year][3]) + "-" + str(kyakugai) + "|" + str(tyakuKaisu[Year][0]) + "\n"
	text += "単勝率：" + str(tanshou_ritsu) + "%  回収率：" +str(tanshou_kaishuritsu) + "\n"
	text += "複勝率：" + str(fukusho_ritsu) + "%  回収率：" +str(fukusho_kaishuritsu) + ""

	#着回数
	print(text)

#１０年間の集計
total_tyakuKaisu = [0] * 4
total_tansho_tekityuKaisu = 0
total_fukusho_tekityuKaisu = 0
total_tansho_haraimodoshi_sum = 0
total_fukusho_haraimodoshi_sum = 0
for Year in Years:
	#レース結果格納する配列：総数, １着, ２着, ３着
	total_tyakuKaisu[0] += tyakuKaisu[Year][0]
	total_tyakuKaisu[1] += tyakuKaisu[Year][1]
	total_tyakuKaisu[2] += tyakuKaisu[Year][2]
	total_tyakuKaisu[3] += tyakuKaisu[Year][3]
	#単勝・複勝の的中回数
	total_tansho_tekityuKaisu += tansho_tekityuKaisu[Year]
	total_fukusho_tekityuKaisu += fukusho_tekityuKaisu[Year]
	#単勝・複勝の払戻総額
	total_tansho_haraimodoshi_sum += tansho_haraimodoshi_sum[Year]
	total_fukusho_haraimodoshi_sum += fukusho_haraimodoshi_sum[Year]

#着外の回数
total_kyakugai = total_tyakuKaisu[0] - total_tyakuKaisu[1] - total_tyakuKaisu[2]- total_tyakuKaisu[3]
#単勝の的中率と回収率
total_tanshou_ritsu = round(total_tyakuKaisu[1] / total_tyakuKaisu[0] * 100, 1)
total_tanshou_kaishuritsu = round(total_tansho_haraimodoshi_sum / total_tyakuKaisu[0], 1)
#複勝の的中率と回収率
total_fukusho_ritsu = round(total_fukusho_tekityuKaisu / total_tyakuKaisu[0] * 100, 1)
total_fukusho_kaishuritsu = round(total_fukusho_haraimodoshi_sum / total_tyakuKaisu[0], 1)

#文字列整形
text = "----------------１０年間（2010-2019）----------------------\n"
text += "1着-2着-3着-着外|該当レース数 ： "
text += str(total_tyakuKaisu[1]) + "-" + str(total_tyakuKaisu[2]) + "-" + str(total_tyakuKaisu[3]) + "-" + str(total_kyakugai) + "|" + str(total_tyakuKaisu[0]) + "\n"
text += "単勝率：" + str(total_tanshou_ritsu) + "%  回収率：" +str(total_tanshou_kaishuritsu) + "\n"
text += "複勝率：" + str(total_fukusho_ritsu) + "%  回収率：" +str(total_fukusho_kaishuritsu) + ""

#着回数
print(text)


