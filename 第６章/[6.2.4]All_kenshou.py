import math
import os
#独自ライブラリのインポート
import utility as U

#競馬場配列
#JyoCDs = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]
JyoCDs = ["05"]

#フォルダ指定
dir_path = "results/"

#レース数を格納する辞書型
race_num = {}
race_num_r = {}
#単勝・複勝の的中回数を格納する辞書型
tansho_tekityuKaisu = {}
tansho_tekityuKaisu_r = {}
fukusho_tekityuKaisu = {}
fukusho_tekityuKaisu_r = {}
#単勝・複勝の払戻総額を格納する辞書型
tansho_haraimodoshi_sum = {}
tansho_haraimodoshi_sum_r = {}
fukusho_haraimodoshi_sum = {}
fukusho_haraimodoshi_sum_r = {}

#年度配列
Years = [0] * 11
for n in range(len(Years)):
	Year = str(2010 + n)
	Years[n] = Year
	#レース数を格納する辞書型
	race_num[Year] = 0
	race_num_r[Year] = 0
	#単勝・複勝の的中回数を格納する辞書型
	tansho_tekityuKaisu[Year] = 0
	tansho_tekityuKaisu_r[Year] = 0
	fukusho_tekityuKaisu[Year] = 0
	fukusho_tekityuKaisu_r[Year] = 0
	#単勝・複勝の払戻総額を格納する辞書型
	tansho_haraimodoshi_sum[Year] = 0
	tansho_haraimodoshi_sum_r[Year] = 0
	fukusho_haraimodoshi_sum[Year] = 0
	fukusho_haraimodoshi_sum_r[Year] = 0

#Years = ["2020"]
Ninkis = ["01"]

#競馬場ごと
for JyoCD in JyoCDs:
	print ("#############################################################")
	print ("　" +  U.getCodeValue( "2001", JyoCD, 1 ) )
	print ("#############################################################")
	#フォルダ生成
	os.makedirs(dir_path + JyoCD, exist_ok = True)

	#全コース情報を取得
	Courses = U.Courses[JyoCD]
	#############################################################
	# データ集計
	#############################################################
	#人気ごと
	for Ninki in Ninkis:
		#コースごとに
		for Course in Courses:
			#トラックコードと距離を取得
			TrackCD = Course["TrackCD"]
			Kyori = Course["Kyori"]

			if( (TrackCD == "11" and Kyori == "1400") == False): continue 

			print ("【" + U.getCodeValue( "2009", TrackCD, 2 ) + " " + Kyori + "m（"+ str(int(Ninki)) + "人気）】"  )

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
						if( UMA_RACE["Ninki"] != Ninki ): continue

						#文字列整形
						text = ""
						text += UMA_RACE["Year"] + UMA_RACE["MonthDay"] + " "
						text += UMA_RACE["RaceNum"] + "R "
						text += UMA_RACE["Bamei"] + " \t\t"
						text += str(int(UMA_RACE["Ninki"])) + "番人気 "
						text += "（" + str(int(UMA_RACE["Odds"])/10) + "倍）" 
						text += str(int(UMA_RACE["KakuteiJyuni"])) + "位 "

						#前走馬毎レース情報
						zensoUMA_RACE = U.getZensoUMA_RACE( UMA_RACE["KettoNum"], UMA_RACE["Year"], UMA_RACE["MonthDay"])
						if( zensoUMA_RACE == False ): continue
						#前走レース情報
						zensoRACE = U.getZensoRACE( UMA_RACE["KettoNum"], zensoUMA_RACE)
						if( zensoRACE == False ): continue

						#脚質取得
						Kyakushitu = U.getUmaKyakushitu( UMA_RACE["KettoNum"], UMA_RACE["Year"], UMA_RACE["MonthDay"])
						#レース間隔取得
						Interval = U.getRaceInterval( UMA_RACE["KettoNum"], UMA_RACE["Year"], UMA_RACE["MonthDay"])
						#前走上がり順位取得
						zensoAgariJyuni = U.getZensoAgariJyuni( UMA_RACE["KettoNum"], zensoUMA_RACE )
						#整数化オッズ取得
						Odds_int = int(int(UMA_RACE["Odds"])/10)
						#馬体重増減取得
						if( (UMA_RACE["ZogenSa"] == "999" or UMA_RACE["ZogenSa"] == "") ): continue
						ZogenSa = int(UMA_RACE["ZogenSa"])
						if(UMA_RACE["ZogenFugo"] == "-"): ZogenSa = - ZogenSa
						#前走距離差取得
						zensoKyoriSa = int(RACE["Kyori"]) - int(zensoRACE["Kyori"])
						#牝馬限定フラグ取得
						KigoCD = RACE["KigoCD"]
						HinbaGentei = True if(KigoCD[1] == "2") else False
						#馬場状態取得
						BabaCD = RACE["SibaBabaCD"] if(int(RACE["TrackCD"]) <= 22) else RACE["DirtBabaCD"]
						#前走競馬場取得
						zensoJyoCD = zensoRACE["JyoCD"]
						#前走オッズ
						zensoOdds_int = int(int(zensoUMA_RACE["Odds"])/10)
						#前走順位
						zensoJyuni = int(zensoUMA_RACE["KakuteiJyuni"])

						m = 0
						if(UMA_RACE["Ninki"] == "01"):

							#141/424 85.6
							if(RACE["JyuryoCD"] != "1"):
								#137/404 86.9
								if(RACE["GradeCD"] != "B"):
									#137/404 86.9
									if(int(UMA_RACE["Barei"]) <=6):
										#110/294 97.0
										if(int(UMA_RACE["Wakuban"])<=6):
											#102/267 99.3
											if( (440 <= int(UMA_RACE["BaTaijyu"]) < 450) == False ):
												#99/255 100.3
												if( ( 8 < ZogenSa <= 16) == False ):
													#96/233 105.8
													if( -400 <= zensoKyoriSa <= 0):

														if(RACE["SyubetuCD"] == "13"):
															m += 1															
														if(RACE["SyubetuCD"] == "14"):
															m += 1
														if(HinbaGentei):
															m += 1
														if(RACE["JyuryoCD"] == "4"):
															m += 1
														if(RACE["JyokenCD5"] == "010"):
															m += 1
														if(RACE["JyokenCD5"] == "016"):
															m += 1
														if(BabaCD == "3"):
															m += 1
														if(BabaCD == "4"):
															m += 1																
														if(int(UMA_RACE["Barei"]) == 5):
															m += 1
														if(int(UMA_RACE["Barei"]) == 6):
															m += 1
														if(UMA_RACE["SexCD"] == "2" ):
															m += 1
														if(UMA_RACE["SexCD"] == "3" ):
															m += 1
														if(Odds_int == 3):
															m += 1
														if(Odds_int == 5):
															m += 1
														if( (450 <= int(UMA_RACE["BaTaijyu"]) < 460)):
															m += 1
														if( (500 <= int(UMA_RACE["BaTaijyu"]) < 510)):
															m += 1
														if( (520 <= int(UMA_RACE["BaTaijyu"]) )):
															m += 1
														if( Interval == 3 ):
															m += 1
														if( 9 <= Interval <= 12 ):
															m += 1
														if( zensoJyoCD == "08" ):
															m += 1
														if( zensoJyoCD == "09" ):
															m += 1
														if( zensoOdds_int == 1 or  zensoOdds_int == 8 or zensoOdds_int == 9 or zensoOdds_int == 11 or zensoOdds_int == 13 or zensoOdds_int >= 15):
															m += 1
														if( zensoJyuni == 4 or zensoJyuni == 6 or zensoJyuni == 8 or zensoJyuni == 9 ):
															m += 1
														if( zensoAgariJyuni == 2 or zensoAgariJyuni == 5 or zensoAgariJyuni == 9):
															m += 1


						if(m == 0): continue

						race_num[Year] += 1
						race_num_r[Year] += m

						#単勝的中の場合
						for i in range(3):
							n = str(i + 1)
							if(HARAI["PayTansyoUmaban" + n] == UMA_RACE["Umaban"]):
								tansho_tekityuKaisu[Year] += 1
								tansho_tekityuKaisu_r[Year] += m
								tansho_haraimodoshi_sum[Year] += int(HARAI["PayTansyoPay" + n])
								tansho_haraimodoshi_sum_r[Year] += int(HARAI["PayTansyoPay" + n]) * m

						#複勝的中の場合
						for i in range(5):
							n = str(i + 1)
							if(HARAI["PayFukusyoUmaban" + n] == UMA_RACE["Umaban"]):
								fukusho_tekityuKaisu[Year] += 1
								fukusho_tekityuKaisu_r[Year] += m
								fukusho_haraimodoshi_sum[Year] += int(HARAI["PayFukusyoPay" + n])
								fukusho_haraimodoshi_sum_r[Year] += int(HARAI["PayFukusyoPay" + n]) * m

						text += "投票数：" + str(m)

						#ターミナルへ出力
						print(text)



#結果出力
print("年度別回収率")
race_num_total = 0
tansho_tekityuKaisu_total = 0
tansho_haraimodoshi_sum_total = 0
race_num_r_total = 0
tansho_tekityuKaisu_r_total = 0
tansho_haraimodoshi_sum_r_total = 0

for Year in Years:
	race_num_total += race_num[Year]
	race_num_r_total += race_num_r[Year]
	tansho_tekityuKaisu_total += tansho_tekityuKaisu[Year]
	tansho_tekityuKaisu_r_total += tansho_tekityuKaisu_r[Year]
	tansho_haraimodoshi_sum_total += tansho_haraimodoshi_sum[Year]
	tansho_haraimodoshi_sum_r_total += tansho_haraimodoshi_sum_r[Year]
	b_race_num = race_num[Year] if(race_num[Year]>0) else 1
	b_race_num_r = race_num_r[Year] if(race_num_r[Year]>0) else 1

	print( Year + "\t" + str(tansho_tekityuKaisu[Year]) + "/" + str(race_num[Year]) + "\t" + str( round( tansho_haraimodoshi_sum[Year]/b_race_num  ,1) ) + "\t" + str(tansho_tekityuKaisu_r[Year]) + "/" + str(race_num_r[Year]) + "\t" + str( round( tansho_haraimodoshi_sum_r[Year]/b_race_num_r  ,1) ) )

print("平均回収率")
print( str(tansho_tekityuKaisu_total) + "/" + str(race_num_total) + " " + str( round( tansho_haraimodoshi_sum_total/race_num_total  ,1) ) + "\t" + str(tansho_tekityuKaisu_r_total) + "/" + str(race_num_r_total) + " " + str( round( tansho_haraimodoshi_sum_r_total/race_num_r_total  ,1) ) )
