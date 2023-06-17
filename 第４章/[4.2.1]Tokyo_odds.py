import os
#独自ライブラリのインポート
import utility as U

#東京競馬場１番人気（2010-2019）
JyoCD = "05"

#オッズ配列（1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100）
OddsInts = [0] * 19
for n in range(len(OddsInts)):
	if(1+n<=9):
		OddsInts[n] = str(1 + n)
	elif(1+n<=18):
		OddsInts[n] = str(10 * (n-8))
	else:
		OddsInts[n] = str(100 * (n-17))


#年度配列
Years = [0] * 10
for n in range(len(Years)):
	Years[n] = str(2010 + n)

#レース結果を格納する辞書型
tyakuKaisu = {}
#単勝・複勝の的中回数を格納する辞書型
tansho_tekityuKaisu = {}
fukusho_tekityuKaisu = {}
#単勝・複勝の払戻総額を格納する辞書型
tansho_haraimodoshi_sum = {}
fukusho_haraimodoshi_sum = {}
for Year in Years:
	tyakuKaisu[Year] = {}
	tansho_tekityuKaisu[Year] = {}
	fukusho_tekityuKaisu[Year] = {}
	tansho_haraimodoshi_sum[Year] = {}
	fukusho_haraimodoshi_sum[Year] = {}
	for OddsInt in OddsInts:
		#レース結果格納する配列：総数, １着, ２着, ３着
		tyakuKaisu[Year][OddsInt] = [0] * 4
		#単勝・複勝の的中回数
		tansho_tekityuKaisu[Year][OddsInt] = 0
		fukusho_tekityuKaisu[Year][OddsInt] = 0
		#単勝・複勝の払戻総額
		tansho_haraimodoshi_sum[Year][OddsInt] = 0
		fukusho_haraimodoshi_sum[Year][OddsInt] = 0

#年度ごと
for Year in Years:
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
	#レースごと
	for RACE in RACEs:
		#障害競走を除外
		if(int(RACE["TrackCD"]) >= 30): continue
		#払戻情報を取得
		HARAI = U.getHARAI(RACE)
		#該当レースの出走馬を取得（人気順）
		UMA_RACEs = U.getShiteiRaceUMA_RACEs( RACE )
		for UMA_RACE in UMA_RACEs:
			#人気を取得
			Ninki = UMA_RACE["Ninki"]
			if(Ninki == "00"): continue
			#文字列整形
			text = ""
			text += UMA_RACE["Year"] + UMA_RACE["MonthDay"] + " "
			text += UMA_RACE["RaceNum"] + "R "
			text += UMA_RACE["Bamei"] + " \t\t"
			text += str(int(UMA_RACE["Ninki"])) + "番人気 "
			text += "（" + str(int(UMA_RACE["Odds"])/10) + "倍）" 
			text += UMA_RACE["KakuteiJyuni"] + "位 "
			#オッズ（小数切り捨て）
			Odds_int = int(int(UMA_RACE["Odds"])/10)
			if(Odds_int <= 9):
				OddsInt = str(Odds_int)
			elif(Odds_int < 100):
				for i in range(1,10):
					if( i*10 <= Odds_int < (i+1)*10 ):
						OddsInt = str(i*10)
			else:
				OddsInt = "100"

			#レース結果を集計
			tyakuKaisu[Year][OddsInt][0] += 1
			if( int(UMA_RACE["KakuteiJyuni"]) <= 3):
				tyakuKaisu[Year][OddsInt][int(UMA_RACE["KakuteiJyuni"])] += 1
			#単勝的中の場合
			for i in range(3):
				n = str(i + 1)
				if(HARAI["PayTansyoUmaban" + n] == UMA_RACE["Umaban"]):
					tansho_haraimodoshi_sum[Year][OddsInt] += int(HARAI["PayTansyoPay" + n])
					tansho_tekityuKaisu[Year][OddsInt] += 1
			#複勝的中の場合
			for i in range(5):
				n = str(i + 1)
				if(HARAI["PayFukusyoUmaban" + n] == UMA_RACE["Umaban"]):
					fukusho_haraimodoshi_sum[Year][OddsInt] += int(HARAI["PayFukusyoPay" + n])
					fukusho_tekityuKaisu[Year][OddsInt] += 1
			#ターミナルへ出力
			#print(text)

	#文字列整形
	text = "----------------" + Year + "年----------------------\n"
	#オッズごと
	for OddsInt in OddsInts:
		#着外の回数
		kyakugai = tyakuKaisu[Year][OddsInt][0] - tyakuKaisu[Year][OddsInt][1] - tyakuKaisu[Year][OddsInt][2]- tyakuKaisu[Year][OddsInt][3]
		#分母
		b_tyakuKaisu = tyakuKaisu[Year][OddsInt][0] if( tyakuKaisu[Year][OddsInt][0] > 0 ) else 1
		#単勝の的中率と回収率
		tanshou_ritsu = round(tyakuKaisu[Year][OddsInt][1] / b_tyakuKaisu * 100, 1)
		tanshou_kaishuritsu = round(tansho_haraimodoshi_sum[Year][OddsInt] / b_tyakuKaisu, 1)
		#複勝の的中率と回収率
		fukusho_ritsu = round(fukusho_tekityuKaisu[Year][OddsInt] / b_tyakuKaisu * 100, 1)
		fukusho_kaishuritsu = round(fukusho_haraimodoshi_sum[Year][OddsInt] / b_tyakuKaisu, 1)

		text += "【" + str(int(OddsInt)) +  "倍台】"
		text += "1着-2着-3着-着外|該当レース数 ： "
		text += str(tyakuKaisu[Year][OddsInt][1]) + "-" + str(tyakuKaisu[Year][OddsInt][2]) + "-" + str(tyakuKaisu[Year][OddsInt][3]) + "-" + str(kyakugai) + "|" + str(tyakuKaisu[Year][OddsInt][0]) + "\n"
		text += "単勝率：" + str(tanshou_ritsu) + "%  回収率：" +str(tanshou_kaishuritsu) + "\n"
		text += "複勝率：" + str(fukusho_ritsu) + "%  回収率：" +str(fukusho_kaishuritsu) + "\n"

	#ターミナルへ出力
	print(text)

#フォルダ指定
dir_path = "results/" 
#フォルダ生成
os.makedirs(dir_path, exist_ok = True)
#ファイルオープン
fout = open( dir_path + JyoCD  + ".txt", "w")
fout.write( "東京競馬場　オッズ別成績（10年間平均）\n" )
fout.write( "オッズ\t単勝率\t（回収率）\t複勝率\t（回収率）\t着回数\n" )

#文字列整形
text = "----------------１０年間（2010-2019）----------------------\n"
for OddsInt in OddsInts:
	text += "【" + str(int(OddsInt)) +  "倍台】"
	total_tyakuKaisu = [0] * 4
	total_tansho_tekityuKaisu = 0
	total_fukusho_tekityuKaisu = 0
	total_tansho_haraimodoshi_sum = 0
	total_fukusho_haraimodoshi_sum = 0
	for Year in Years:
		#レース結果格納する配列：総数, １着, ２着, ３着
		total_tyakuKaisu[0] += tyakuKaisu[Year][OddsInt][0]
		total_tyakuKaisu[1] += tyakuKaisu[Year][OddsInt][1]
		total_tyakuKaisu[2] += tyakuKaisu[Year][OddsInt][2]
		total_tyakuKaisu[3] += tyakuKaisu[Year][OddsInt][3]
		#単勝・複勝の的中回数
		total_tansho_tekityuKaisu += tansho_tekityuKaisu[Year][OddsInt]
		total_fukusho_tekityuKaisu += fukusho_tekityuKaisu[Year][OddsInt]
		#単勝・複勝の払戻総額
		total_tansho_haraimodoshi_sum += tansho_haraimodoshi_sum[Year][OddsInt]
		total_fukusho_haraimodoshi_sum += fukusho_haraimodoshi_sum[Year][OddsInt]

	#着外の回数
	total_kyakugai = total_tyakuKaisu[0] - total_tyakuKaisu[1] - total_tyakuKaisu[2]- total_tyakuKaisu[3]
	#分母
	b_total_tyakuKaisu = total_tyakuKaisu[0] if( total_tyakuKaisu[0] > 0 ) else 1
	#単勝の的中率と回収率
	total_tanshou_ritsu = round(total_tyakuKaisu[1] / b_total_tyakuKaisu * 100, 1)
	total_tanshou_kaishuritsu = round(total_tansho_haraimodoshi_sum / b_total_tyakuKaisu, 1)
	#複勝の的中率と回収率
	total_fukusho_ritsu = round(total_fukusho_tekityuKaisu / b_total_tyakuKaisu * 100, 1)
	total_fukusho_kaishuritsu = round(total_fukusho_haraimodoshi_sum / b_total_tyakuKaisu, 1)

	#着回数
	tyaku = str(total_tyakuKaisu[1]) + "-" + str(total_tyakuKaisu[2]) + "-" + str(total_tyakuKaisu[3]) + "-" + str(total_kyakugai) + "|" + str(total_tyakuKaisu[0])
	text += "1着-2着-3着-着外|該当レース数 ： "
	text += tyaku + "\n"
	text += "単勝率：" + str(total_tanshou_ritsu) + "%  回収率：" +str(total_tanshou_kaishuritsu) + "\n"
	text += "複勝率：" + str(total_fukusho_ritsu) + "%  回収率：" +str(total_fukusho_kaishuritsu) + "\n"
	#ファイルへ書き出し
	fout.write( str(int(OddsInt)) + "〜\t")  
	fout.write( str(total_tanshou_ritsu) + "\t" + str(total_tanshou_kaishuritsu)  + "\t" )
	fout.write( str(total_fukusho_ritsu) + "\t" + str(total_fukusho_kaishuritsu)  + "\t" )
	fout.write( tyaku + "\n" )

#ターミナルへ出力
print(text)
#ファイルクローズ
fout.close()

