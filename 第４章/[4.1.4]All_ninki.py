import os
#独自ライブラリのインポート
import utility as U

#人気配列
Ninkis = [0] * 18
for n in range(len(Ninkis)):
	Ninkis[n] = str(1 + n)
	if( n + 1 <= 9): Ninkis[n] = "0" + Ninkis[n]

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

#フォルダ指定
dir_path = "results/" 
#フォルダ生成
os.makedirs(dir_path, exist_ok = True)

#JRA全競馬場
JyoCDs = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]

#競馬場ごと
for JyoCD in JyoCDs:
	print("##############################################")
	print("#" + U.getCodeValue( "2001", JyoCD, 1 ))
	print("##############################################")

	tyakuKaisu[JyoCD] = {}
	tansho_tekityuKaisu[JyoCD] = {}
	fukusho_tekityuKaisu[JyoCD] = {}
	tansho_haraimodoshi_sum[JyoCD] = {}
	fukusho_haraimodoshi_sum[JyoCD] = {}

	#年度ごと
	for Year in Years:

		tyakuKaisu[JyoCD][Year] = {}
		tansho_tekityuKaisu[JyoCD][Year] = {}
		fukusho_tekityuKaisu[JyoCD][Year] = {}
		tansho_haraimodoshi_sum[JyoCD][Year] = {}
		fukusho_haraimodoshi_sum[JyoCD][Year] = {}

		#人気ごと
		for Ninki in Ninkis:
			#レース結果格納する配列：総数, １着, ２着, ３着
			tyakuKaisu[JyoCD][Year][Ninki] = [0] * 4
			#単勝・複勝の的中回数
			tansho_tekityuKaisu[JyoCD][Year][Ninki] = 0
			fukusho_tekityuKaisu[JyoCD][Year][Ninki] = 0
			#単勝・複勝の払戻総額
			tansho_haraimodoshi_sum[JyoCD][Year][Ninki] = 0
			fukusho_haraimodoshi_sum[JyoCD][Year][Ninki] = 0

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
			UMA_RACEs = U.getShiteiRaceUMA_RACEs( RACE, "Ninki ASC" )
			for UMA_RACE in UMA_RACEs:
				#人気を取得
				Ninki = UMA_RACE["Ninki"]
				if(Ninki == "00"): continue
				#レース結果を集計
				tyakuKaisu[JyoCD][Year][Ninki][0] += 1
				if( int(UMA_RACE["KakuteiJyuni"]) <= 3):
					tyakuKaisu[JyoCD][Year][Ninki][int(UMA_RACE["KakuteiJyuni"])] += 1
				#単勝的中の場合
				for i in range(3):
					n = str(i + 1)
					if(HARAI["PayTansyoUmaban" + n] == UMA_RACE["Umaban"]):
						tansho_haraimodoshi_sum[JyoCD][Year][Ninki] += int(HARAI["PayTansyoPay" + n])
						tansho_tekityuKaisu[JyoCD][Year][Ninki] += 1
				#複勝的中の場合
				for i in range(5):
					n = str(i + 1)
					if(HARAI["PayFukusyoUmaban" + n] == UMA_RACE["Umaban"]):
						fukusho_haraimodoshi_sum[JyoCD][Year][Ninki] += int(HARAI["PayFukusyoPay" + n])
						fukusho_tekityuKaisu[JyoCD][Year][Ninki] += 1

		#文字列整形
		text = "----------------" + Year + "年----------------------\n"
		for Ninki in Ninkis:
			#着外の回数
			kyakugai = tyakuKaisu[JyoCD][Year][Ninki][0] - tyakuKaisu[JyoCD][Year][Ninki][1] - tyakuKaisu[JyoCD][Year][Ninki][2]- tyakuKaisu[JyoCD][Year][Ninki][3]
			#分母
			b_tyakuKaisu = tyakuKaisu[JyoCD][Year][Ninki][0] if(tyakuKaisu[JyoCD][Year][Ninki][0]>0) else 1
			#単勝の的中率と回収率
			tanshou_ritsu = round(tyakuKaisu[JyoCD][Year][Ninki][1] / b_tyakuKaisu * 100, 1)
			tanshou_kaishuritsu = round(tansho_haraimodoshi_sum[JyoCD][Year][Ninki] / b_tyakuKaisu, 1)
			#複勝の的中率と回収率
			fukusho_ritsu = round(fukusho_tekityuKaisu[JyoCD][Year][Ninki] / b_tyakuKaisu * 100, 1)
			fukusho_kaishuritsu = round(fukusho_haraimodoshi_sum[JyoCD][Year][Ninki] / b_tyakuKaisu, 1)

			text += "【" + str(int(Ninki)) +  "人気】"
			text += "1着-2着-3着-着外|該当レース数 ： "
			text += str(tyakuKaisu[JyoCD][Year][Ninki][1]) + "-" + str(tyakuKaisu[JyoCD][Year][Ninki][2]) + "-" + str(tyakuKaisu[JyoCD][Year][Ninki][3]) + "-" + str(kyakugai) + "|" + str(tyakuKaisu[JyoCD][Year][Ninki][0]) + "\n"
			text += "単勝率：" + str(tanshou_ritsu) + "%  回収率：" +str(tanshou_kaishuritsu) + "\n"
			text += "複勝率：" + str(fukusho_ritsu) + "%  回収率：" +str(fukusho_kaishuritsu) + "\n"

		#ターミナルへ出力
		print(text)

	#ファイルオープン
	fout = open( dir_path + JyoCD  + ".txt", "w")
	fout.write( U.getCodeValue( "2001", JyoCD, 1 ) + "　人気別成績（10年間）\n" )
	fout.write( "人気\t単勝率\t（回収率）\t複勝率\t（回収率）\t着回数\n" )

	#文字列整形
	text = "----------------１０年間（2010-2019）----------------------\n"
	#人気ごと
	for Ninki in Ninkis:
		text += "【" + str(int(Ninki)) +  "人気】"
		total_tyakuKaisu = [0] * 4
		total_tansho_tekityuKaisu = 0
		total_fukusho_tekityuKaisu = 0
		total_tansho_haraimodoshi_sum = 0
		total_fukusho_haraimodoshi_sum = 0
		#年度ごと
		for Year in Years:
			#レース結果格納する配列：総数, １着, ２着, ３着
			total_tyakuKaisu[0] += tyakuKaisu[JyoCD][Year][Ninki][0]
			total_tyakuKaisu[1] += tyakuKaisu[JyoCD][Year][Ninki][1]
			total_tyakuKaisu[2] += tyakuKaisu[JyoCD][Year][Ninki][2]
			total_tyakuKaisu[3] += tyakuKaisu[JyoCD][Year][Ninki][3]
			#単勝・複勝の的中回数
			total_tansho_tekityuKaisu += tansho_tekityuKaisu[JyoCD][Year][Ninki]
			total_fukusho_tekityuKaisu += fukusho_tekityuKaisu[JyoCD][Year][Ninki]
			#単勝・複勝の払戻総額
			total_tansho_haraimodoshi_sum += tansho_haraimodoshi_sum[JyoCD][Year][Ninki]
			total_fukusho_haraimodoshi_sum += fukusho_haraimodoshi_sum[JyoCD][Year][Ninki]

		#着外の回数
		total_kyakugai = total_tyakuKaisu[0] - total_tyakuKaisu[1] - total_tyakuKaisu[2]- total_tyakuKaisu[3]
		#分母
		b_total_tyakuKaisu = total_tyakuKaisu[0] if(total_tyakuKaisu[0]>0) else 1
		#単勝の的中率と回収率
		total_tanshou_ritsu = round(total_tyakuKaisu[1] / b_total_tyakuKaisu * 100, 1)
		total_tanshou_kaishuritsu = round(total_tansho_haraimodoshi_sum / b_total_tyakuKaisu, 1)
		#複勝の的中率と回収率
		total_fukusho_ritsu = round(total_fukusho_tekityuKaisu / b_total_tyakuKaisu * 100, 1)
		total_fukusho_kaishuritsu = round(total_fukusho_haraimodoshi_sum /b_total_tyakuKaisu, 1)
		#着回数
		tyaku = str(total_tyakuKaisu[1]) + "-" + str(total_tyakuKaisu[2]) + "-" + str(total_tyakuKaisu[3]) + "-" + str(total_kyakugai) + "|" + str(total_tyakuKaisu[0])
		text += "1着-2着-3着-着外|該当レース数 ： "
		text += tyaku + "\n"
		text += "単勝率：" + str(total_tanshou_ritsu) + "%  回収率：" +str(total_tanshou_kaishuritsu) + "\n"
		text += "複勝率：" + str(total_fukusho_ritsu) + "%  回収率：" +str(total_fukusho_kaishuritsu) + "\n"
		#ファイルへ書き出し
		fout.write( str(int(Ninki)) + "\t")  
		fout.write( str(total_tanshou_ritsu) + "\t" + str(total_tanshou_kaishuritsu)  + "\t" )
		fout.write( str(total_fukusho_ritsu) + "\t" + str(total_fukusho_kaishuritsu)  + "\t" )
		fout.write( tyaku + "\n" )

	#ターミナルへ出力
	print(text)
	#ファイルクローズ
	fout.close()

#################################################
# 全競馬場の単勝回収率を集計したファイル生成
#################################################
#ファイルオープン
fout = open( dir_path + "all.txt", "w")
fout.write( "全競馬場　人気別 単勝回収率（10年間平均）\n" )
fout.write( "人気" )
for JyoCD in JyoCDs:
	fout.write( "\t" + U.getCodeValue( "2001", JyoCD, 3 ) )
fout.write( "\t全体")
fout.write( "\n" )

#人気ごと
for Ninki in Ninkis:
	fout.write( str(int(Ninki)) )
	#出走頭数を格納する辞書型
	shusotosu = {}
	#全競馬場の払戻総額
	tansho_haraimodoshi_sum_year_all = 0
	#競馬場ごと
	for JyoCD in JyoCDs:
		#初期化
		shusotosu[JyoCD] = 0 
		#10年間払戻額の合計
		tansho_haraimodoshi_sum_year = 0
		#年度ごと
		for Year in Years:
			shusotosu[JyoCD] += tyakuKaisu[JyoCD][Year][Ninki][0]
			tansho_haraimodoshi_sum_year += tansho_haraimodoshi_sum[JyoCD][Year][Ninki]
		#分母（出走頭数）
		b_shusotosu = shusotosu[JyoCD] if(shusotosu[JyoCD]>0) else 1
		fout.write( "\t" + str(round(tansho_haraimodoshi_sum_year/b_shusotosu,1)) )
		#全競馬場の払戻総額の加算
		tansho_haraimodoshi_sum_year_all += tansho_haraimodoshi_sum_year

	#ここから右端列
	#全競馬場の出走頭数
	shusotosu_all = 0
	for JyoCD in JyoCDs:
		shusotosu_all += shusotosu[JyoCD]
	#分母（全競馬場の出走頭数）
	b_shusotosu_all = shusotosu_all if(shusotosu_all>0) else 1
	fout.write( "\t" + str(round(tansho_haraimodoshi_sum_year_all/b_shusotosu_all,1)) )
	fout.write( "\n" )

#ファイルクローズ
fout.close()