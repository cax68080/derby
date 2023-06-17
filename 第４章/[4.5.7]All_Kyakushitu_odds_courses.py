import math
import os
#独自ライブラリのインポート
import utility as U

#競馬場配列
JyoCDs = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]
#JyoCDs = ["05"]

#脚質配列
Kyakushitus = ["1", "2", "3", "4"] 

KyakushituNames = {}
KyakushituNames["1"] = "逃げ"
KyakushituNames["2"] = "先行"
KyakushituNames["3"] = "差し"
KyakushituNames["4"] = "追い"

#フォルダ指定
dir_path = "results/kyakushitu/"

#オッズ配列（1,2,3,4,5,6,7,8,9,10,11,12,13,14,15~）
OddsInts = [0] * 5
for n in range(len(OddsInts)):
	OddsInts[n] = str(1 + n)

#年度配列
Years = [0] * 10
for n in range(len(Years)):
	Years[n] = str(2010 + n)

#レース数を格納する辞書型
race_num = {}
#レース結果を格納する辞書型
tyakuKaisu = {}
#単勝・複勝の的中回数を格納する辞書型
tansho_tekityuKaisu = {}
fukusho_tekityuKaisu = {}
#単勝・複勝の払戻総額を格納する辞書型
tansho_haraimodoshi_sum = {}
fukusho_haraimodoshi_sum = {}

#競馬場ごと
for JyoCD in JyoCDs:
	print (U.getCodeValue( "2001", JyoCD, 1 ))
	#フォルダ生成
	os.makedirs(dir_path + JyoCD, exist_ok = True)

	#全コース情報を取得
	Courses = U.Courses[JyoCD]

	race_num[JyoCD] = {}
	tyakuKaisu[JyoCD] = {}
	tansho_tekityuKaisu[JyoCD] = {}
	fukusho_tekityuKaisu[JyoCD] = {}
	tansho_haraimodoshi_sum[JyoCD] = {}
	fukusho_haraimodoshi_sum[JyoCD] = {}

	#############################################################
	# データ集計
	#############################################################
	#コースごとに
	for Course in Courses:
		#トラックコードと距離を取得
		TrackCD = Course["TrackCD"]
		Kyori = Course["Kyori"]

		race_num[JyoCD][TrackCD+Kyori] = {}
		tyakuKaisu[JyoCD][TrackCD+Kyori] = {}
		tansho_tekityuKaisu[JyoCD][TrackCD+Kyori] = {}
		fukusho_tekityuKaisu[JyoCD][TrackCD+Kyori] = {}
		tansho_haraimodoshi_sum[JyoCD][TrackCD+Kyori] = {}
		fukusho_haraimodoshi_sum[JyoCD][TrackCD+Kyori] = {}

		#種別ごと
		for Kyakushitu in Kyakushitus:
			race_num[JyoCD][TrackCD+Kyori][Kyakushitu] = 0
			tyakuKaisu[JyoCD][TrackCD+Kyori][Kyakushitu] = {}
			tansho_tekityuKaisu[JyoCD][TrackCD+Kyori][Kyakushitu] = {}
			fukusho_tekityuKaisu[JyoCD][TrackCD+Kyori][Kyakushitu] = {}
			tansho_haraimodoshi_sum[JyoCD][TrackCD+Kyori][Kyakushitu] = {}
			fukusho_haraimodoshi_sum[JyoCD][TrackCD+Kyori][Kyakushitu] = {}

			for OddsInt in OddsInts:
				#レース結果格納する配列：総数, １着, ２着, ３着
				tyakuKaisu[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt] = [0] * 4
				#単勝・複勝の的中回数
				tansho_tekityuKaisu[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt] = 0
				fukusho_tekityuKaisu[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt] = 0
				#単勝・複勝の払戻総額
				tansho_haraimodoshi_sum[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt] = 0
				fukusho_haraimodoshi_sum[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt] = 0

		#年度ごと
		for Year in Years:

			#SQL文
			strSQL_SELECT = "SELECT * FROM N_RACE"
			strSQL_WHERE  = " WHERE DataKubun = '7'"
			strSQL_WHERE += " AND Year = '" + Year + "'" 
			strSQL_WHERE += " AND JyoCD = '" + JyoCD + "'"
			strSQL_WHERE += " AND TrackCD = '" + TrackCD + "'"
			strSQL_WHERE += " AND Kyori = '" + Kyori + "'"
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
					if(Odds_int < len(OddsInts)):
						OddsInt = str(Odds_int)
					else:
						continue
					#脚質を取得
					Kyakushitu = U.getUmaKyakushitu( UMA_RACE["KettoNum"], UMA_RACE["Year"], UMA_RACE["MonthDay"])
					if(Kyakushitu == 0): continue
					Kyakushitu = str(Kyakushitu)

					#出走頭数
					race_num[JyoCD][TrackCD+Kyori][Kyakushitu] += 1

					#レース結果を集計
					tyakuKaisu[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt][0] += 1
					if( int(UMA_RACE["KakuteiJyuni"]) <= 3):
						tyakuKaisu[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt][int(UMA_RACE["KakuteiJyuni"])] += 1
					#単勝的中の場合
					for i in range(3):
						n = str(i + 1)
						if(HARAI["PayTansyoUmaban" + n] == UMA_RACE["Umaban"]):
							tansho_haraimodoshi_sum[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt] += int(HARAI["PayTansyoPay" + n])
							tansho_tekityuKaisu[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt] += 1
					#複勝的中の場合
					for i in range(5):
						n = str(i + 1)
						if(HARAI["PayFukusyoUmaban" + n] == UMA_RACE["Umaban"]):
							fukusho_haraimodoshi_sum[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt] += int(HARAI["PayFukusyoPay" + n])
							fukusho_tekityuKaisu[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt] += 1
					#ターミナルへ出力
					#print(text)

			#文字列整形
			text = "----------------" + Year + "年----------------------\n"
			#種別ごと
			for Kyakushitu in Kyakushitus:
				for OddsInt in OddsInts:
					_tyakuKaisu = tyakuKaisu[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt]
					#着外の回数
					kyakugai = _tyakuKaisu[0] - _tyakuKaisu[1] - _tyakuKaisu[2]- _tyakuKaisu[3]
					#分母
					b_tyakuKaisu = _tyakuKaisu[0] if( _tyakuKaisu[0] > 0 ) else 1
					#単勝の的中率と回収率
					tansho_ritsu = round(_tyakuKaisu[1] / b_tyakuKaisu * 100, 1)
					tansho_kaishuritsu = round(tansho_haraimodoshi_sum[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt] / b_tyakuKaisu, 1)
					#複勝の的中率と回収率
					fukusho_ritsu = round(fukusho_tekityuKaisu[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt] / b_tyakuKaisu * 100, 1)
					fukusho_kaishuritsu = round(fukusho_haraimodoshi_sum[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt] / b_tyakuKaisu, 1)

					text += "【" + str(int(OddsInt)) +  "倍台】"
					text += "1着-2着-3着-着外|該当レース数 ： "
					text += str(_tyakuKaisu[1]) + "-" + str(_tyakuKaisu[2]) + "-" + str(_tyakuKaisu[3]) + "-" + str(kyakugai) + "|" + str(_tyakuKaisu[0]) + "\n"
					text += "単勝率：" + str(tansho_ritsu) + "%  回収率：" +str(tansho_kaishuritsu) + "\n"
					text += "複勝率：" + str(fukusho_ritsu) + "%  回収率：" +str(fukusho_kaishuritsu) + "\n"

				#ターミナルへ出力
				#print(text)

	#############################################################
	# 単勝・複勝の回収率・収支を集計したファイル生成
	#############################################################
	#コースごとに
	for Course in Courses:
		#トラックコードと距離を取得
		TrackCD = Course["TrackCD"]
		Kyori = Course["Kyori"]

		#ファイルオープン
		fout_tansho_kaishuritu = open( dir_path + JyoCD + "/" + TrackCD + "-" + Kyori + "_tansho_kaishuritu.txt", "w")
		fout_fukusho_kaishuritu = open( dir_path + JyoCD + "/" + TrackCD + "-" + Kyori + "_fukusho_kaishuritu.txt", "w")

		shibaDirt = "芝" if(int(TrackCD) < 23) else "ダート"

		#表名出力
		fout_tansho_kaishuritu.write( U.getCodeValue( "2001", JyoCD, 1 ) + "　" + shibaDirt + Kyori + "m 単勝回収率\n" )
		fout_fukusho_kaishuritu.write( U.getCodeValue( "2001", JyoCD, 1 ) + "　" + shibaDirt + Kyori + "m 複勝回収率\n" )

		fout_tansho_kaishuritu.write( "オッズ" )
		fout_fukusho_kaishuritu.write( "オッズ" )

		#１行目
		for Kyakushitu in Kyakushitus:	
			#列カラム名出力
			fout_tansho_kaishuritu.write( "\t" + KyakushituNames[Kyakushitu] )
			fout_fukusho_kaishuritu.write( "\t" + KyakushituNames[Kyakushitu] )

		fout_tansho_kaishuritu.write( "\t着回数\n" )
		fout_fukusho_kaishuritu.write( "\t着回数\n" )

		#２行目以降
		for OddsInt in OddsInts:
			#ファイルへ書き出し
			fout_tansho_kaishuritu.write(  str(int(OddsInt) ) + "〜"  )
			fout_fukusho_kaishuritu.write( str(int(OddsInt) ) + "〜"  )
			#行項目出力
			if(int(OddsInt) < len(OddsInts)): 
				fout_tansho_kaishuritu.write( str(int(OddsInt) + 1) )
				fout_fukusho_kaishuritu.write( str(int(OddsInt) + 1) )
				
			#オッズごとレース結果格納する配列
			tyakuKaisu_odds = [0] * 4

			#値の集計
			for Kyakushitu in Kyakushitus:
				#レース結果格納する配列：[0]:総数, [1]:１着, [2]:２着, [3]:３着
				_tyakuKaisu = tyakuKaisu[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt]

				#レース結果格納する配列：総数, １着, ２着, ３着
				tyakuKaisu_odds[0] += _tyakuKaisu[0]
				tyakuKaisu_odds[1] += _tyakuKaisu[1]
				tyakuKaisu_odds[2] += _tyakuKaisu[2]
				tyakuKaisu_odds[3] += _tyakuKaisu[3]

				#分母
				b_shusokaisu = _tyakuKaisu[0] if( _tyakuKaisu[0] > 0 ) else 1
				#単勝回収率
				tansho_kaishuritsu = round(tansho_haraimodoshi_sum[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt] / b_shusokaisu, 1)
				fout_tansho_kaishuritu.write( "\t" + str(tansho_kaishuritsu) )
				#複勝の回収率
				fukusho_kaishuritsu = round(fukusho_haraimodoshi_sum[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt] / b_shusokaisu, 1)
				fout_fukusho_kaishuritu.write( "\t" + str(fukusho_kaishuritsu) )


			#各オッズごとの着度数集計
			#着外の回数
			total_kyakugai = tyakuKaisu_odds[0] - tyakuKaisu_odds[1] - tyakuKaisu_odds[2]- tyakuKaisu_odds[3]
			#着回数の文字列作成
			tyaku = str(tyakuKaisu_odds[1]) + "-" + str(tyakuKaisu_odds[2]) + "-" + str(tyakuKaisu_odds[3]) + "-" + str(total_kyakugai) + "|" + str(tyakuKaisu_odds[0])
			#着回数出力
			fout_tansho_kaishuritu.write( "\t" + tyaku + "\n" )
			fout_fukusho_kaishuritu.write( "\t" + tyaku + "\n" )

		####################################################
		#全集計
		fout_tansho_kaishuritu.write( "全体" )
		fout_fukusho_kaishuritu.write( "全体" )

		for Kyakushitu in Kyakushitus:
			total_shusokaisu_odds = 0
			total_tansho_haraimodoshi_odds = 0
			total_fukusho_haraimodoshi_odds = 0

			for OddsInt in OddsInts:
				#レース結果格納する配列：[0]:総数, [1]:１着, [2]:２着, [3]:３着
				_tyakuKaisu = tyakuKaisu[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt]

				total_shusokaisu_odds += _tyakuKaisu[0]
				total_tansho_haraimodoshi_odds += tansho_haraimodoshi_sum[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt]
				total_fukusho_haraimodoshi_odds += fukusho_haraimodoshi_sum[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt]

			b_total_shusokaisu = total_shusokaisu_odds if( total_shusokaisu_odds > 0) else 1
			fout_tansho_kaishuritu.write( "\t" + str(round( total_tansho_haraimodoshi_odds/ b_total_shusokaisu, 1)))
			fout_fukusho_kaishuritu.write( "\t" + str(round(total_fukusho_haraimodoshi_odds / b_total_shusokaisu, 1)))


		tyakuKaisu_odds = [0] * 4
		for OddsInt in OddsInts:
			for Kyakushitu in Kyakushitus:
				#レース結果格納する配列：[0]:総数, [1]:１着, [2]:２着, [3]:３着
				_tyakuKaisu = tyakuKaisu[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt]

				#レース結果格納する配列：総数, １着, ２着, ３着
				tyakuKaisu_odds[0] += _tyakuKaisu[0]
				tyakuKaisu_odds[1] += _tyakuKaisu[1]
				tyakuKaisu_odds[2] += _tyakuKaisu[2]
				tyakuKaisu_odds[3] += _tyakuKaisu[3]

		#着外の回数
		total_kyakugai = tyakuKaisu_odds[0] - tyakuKaisu_odds[1] - tyakuKaisu_odds[2]- tyakuKaisu_odds[3]
		#着回数
		tyaku = str(tyakuKaisu_odds[1]) + "-" + str(tyakuKaisu_odds[2]) + "-" + str(tyakuKaisu_odds[3]) + "-" + str(total_kyakugai) + "|" + str(tyakuKaisu_odds[0])

		fout_tansho_kaishuritu.write( "\t" + tyaku + "\n"  )
		fout_fukusho_kaishuritu.write( "\t" + tyaku + "\n"  )
		fout_tansho_kaishuritu.write( "レース数"  )
		fout_fukusho_kaishuritu.write( "レース数" )

		for Kyakushitu in Kyakushitus:
			fout_tansho_kaishuritu.write( "\t" + str(race_num[JyoCD][TrackCD+Kyori][Kyakushitu]) )
			fout_fukusho_kaishuritu.write( "\t" + str(race_num[JyoCD][TrackCD+Kyori][Kyakushitu]) )
		fout_tansho_kaishuritu.write( "\n" )
		fout_fukusho_kaishuritu.write( "\n" )

		#ファイルクローズ
		fout_tansho_kaishuritu.close()
		fout_fukusho_kaishuritu.close()


#############################################################
#　ランキング集計
#############################################################
#ファイルオープン
fout = open( dir_path + "/ranking.txt", "w")
fout.write( "脚質 回収率ランキング\n")

OddsInts = [0] * 4
for n in range(len(OddsInts)):
	OddsInts[n] = str(1 + n)

#最低該当頭数
MinimumNumber = 30

#区分数
N = 0
#単勝
tansho_average = 0
#複勝
fukusho_average = 0
#合計
total_average = 0
total_ranking = []

#順位作成用変数
ranking = {}
n = 0

#平均の計算
for JyoCD in JyoCDs:
	Courses = U.Courses[JyoCD]
	for Course in Courses:
		TrackCD = Course["TrackCD"]
		Kyori = Course["Kyori"]
		for Kyakushitu in Kyakushitus:
			for OddsInt in OddsInts:
				shusotosu = tyakuKaisu[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt][0]
				if(shusotosu < MinimumNumber):  continue
				N += 1
				tansho_average += tansho_haraimodoshi_sum[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt] / shusotosu
				fukusho_average += fukusho_haraimodoshi_sum[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt] / shusotosu

				ranking[str(n)] = ( tansho_haraimodoshi_sum[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt] / shusotosu + fukusho_haraimodoshi_sum[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt] / shusotosu ) / 2
				n += 1

tansho_average = round(tansho_average / N, 1)
fukusho_average = round(fukusho_average / N, 1)

print("区分数：" + str(N))

fout.write("単勝回収率 平均：" + str(tansho_average) + "\n")
fout.write("複勝回収率 平均：" + str(fukusho_average) + "\n")


#並び替え
ranking_sorted = sorted(ranking.items(), key=lambda x:x[1], reverse=True)

#ランキングの作成
m = -1
for r in ranking_sorted:
	m += 1
	n = 0
	for JyoCD in JyoCDs:
		Courses = U.Courses[JyoCD]
		for Course in Courses:
			TrackCD = Course["TrackCD"]
			Kyori = Course["Kyori"]
			for Kyakushitu in Kyakushitus:
				for OddsInt in OddsInts:
					shusotosu = tyakuKaisu[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt][0]
					if(shusotosu < MinimumNumber): continue
					if(r[0] == str(n)): 
						total_ranking.append( {
							"JyoCD" : JyoCD,
							"TrackCD" : TrackCD,
							"Kyori" : Kyori,
							"Kyakushitu" : Kyakushitu,
							"OddsInt" : OddsInt,
							"Value" : r[1]
						} )
					n += 1

fout.write("順位\t競馬場\t芝・ダート\t距離\t種別\tオッズ\t単勝\t複勝\t平均\t出走頭数\n")
m = 0
for t in total_ranking:
	m += 1
	JyoCD = t["JyoCD"]
	TrackCD = t["TrackCD"]
	Kyori = t["Kyori"]
	Kyakushitu = t["Kyakushitu"]
	OddsInt = t["OddsInt"]
	Value = t["Value"]

	shibaDirt = "芝" if(int(TrackCD) < 23) else "ダート"
	shusotosu = tyakuKaisu[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt][0]

	text = str( m ) 
	text += "\t" + U.getCodeValue( "2001", JyoCD, 3 )
	text += "\t" + shibaDirt
	text += "\t" + Kyori + "m"
	text += "\t" + KyakushituNames[Kyakushitu]
	text += "\t" + OddsInt + "~" + str( int(OddsInt) + 1 )
	text += "\t" + str(round(tansho_haraimodoshi_sum[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt] / shusotosu, 1))
	text += "\t" + str(round(fukusho_haraimodoshi_sum[JyoCD][TrackCD+Kyori][Kyakushitu][OddsInt] / shusotosu, 1))
	text += "\t" + str(round(Value, 1))
	text += "\t" + str(shusotosu) + "\n"
	fout.write(text)

fout.close()

