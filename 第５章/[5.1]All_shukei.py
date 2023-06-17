import math
import os
#独自ライブラリのインポート
import utility as U

#競馬場配列
#JyoCDs = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]
JyoCDs = ["05"]

#フォルダ指定
dir_path = "results/"

#年度配列
Years = [0] * 10
for n in range(len(Years)):
	Years[n] = str(2010 + n)

#Years = ["2020"]

Ninkis = ["01"]

Data = {}

def setData( key, value, RACE, UMA_RACE, zensoRACE, zensoUMA_RACE ):

	#競走種別　11 : サラ２才, 12 : サラ３才, 13 : サラ３上, 14 : サラ４上
	Data["SyubetuCD"][RACE["SyubetuCD"]][key] += value

	#牝馬限定フラグ 
	KigoCD = RACE["KigoCD"]
	if((KigoCD[1] == "2")): 
		Data["HinbaGentei"]["True"][key] += value
	else:
		Data["HinbaGentei"]["False"][key] += value

	#重量　1 : ハンデ, 2 : 別定, 3 : 馬齢, 4 : 定量
	Data["JyuryoCD"][RACE["JyuryoCD"]][key] += value

	#条件  005 : 1勝クラス（500万以下）, 010 : 2勝クラス（1000万以下）, 016 : 3勝クラス（1600万以下）, 701 : 新馬, 703: 未勝利, 999 : オープン（コード：2007）
	Data["JyokenCD5"][RACE["JyokenCD5"]][key] += value

	#グレード　A : G1, B : G2, C : G3, D : グレードのない重賞, E : 重賞以外の特別競走, L:リステッド, なし
	GradeCD = RACE["GradeCD"] if( RACE["GradeCD"] != "") else " "
	Data["GradeCD"][GradeCD][key] += value

	#馬場状態　1 : 良, 2 : 稍重, 3 : 重, 4 : 不良
	if(int(RACE["TrackCD"]) <= 22):
		Data["BabaCD"][RACE["SibaBabaCD"]][key] += value
	else:
		Data["BabaCD"][RACE["DirtBabaCD"]][key] += value

	#馬齢　２歳３歳４歳５歳６歳７歳〜
	Barei = UMA_RACE["Barei"]
	if(int(Barei)<=6):
		Data["Barei"][Barei][key] += value
	else:
		Data["Barei"]["07~"][key] += value

	#オッズ
	Odds_int = int(int(UMA_RACE["Odds"])/10)
	if(Odds_int<=14):
		Data["Odds"][str(Odds_int)][key] += value
	else:
		Data["Odds"]["15~"][key] += value

	#枠番
	Data["Wakuban"][UMA_RACE["Wakuban"]][key] += value

	#牡馬・騙馬・牝馬
	Data["SexCD"][UMA_RACE["SexCD"]][key] += value

	#脚質（逃げ・先行・差し・追込）
	if("Kyakusitu" in UMA_RACE): 
		Kyakusitu = UMA_RACE["Kyakusitu"]
	else:
		Kyakusitu = U.getUmaKyakushitu( UMA_RACE["KettoNum"], UMA_RACE["Year"], UMA_RACE["MonthDay"])
		UMA_RACE["Kyakusitu"] = Kyakusitu

	if(Kyakusitu != 0): Data["Kyakusitu"][str(Kyakusitu)][key] += value

	#馬体重
	BaTaijyu = UMA_RACE["BaTaijyu"] 
	if(int(BaTaijyu) < 430):
		BaTaijyu = "~430"
	elif( 430 <= int(BaTaijyu) < 440 ):
		BaTaijyu = "430"
	elif( 440 <= int(BaTaijyu) < 450 ):
		BaTaijyu = "440"
	elif( 450 <= int(BaTaijyu) < 460 ):
		BaTaijyu = "450"
	elif( 460 <= int(BaTaijyu) < 470 ):
		BaTaijyu = "460"
	elif( 470 <= int(BaTaijyu) < 480 ):
		BaTaijyu = "470"
	elif( 480 <= int(BaTaijyu) < 490 ):
		BaTaijyu = "480"
	elif( 490 <= int(BaTaijyu) < 500 ):
		BaTaijyu = "490"
	elif( 500 <= int(BaTaijyu) < 510 ):
		BaTaijyu = "500"
	elif( 510 <= int(BaTaijyu) < 520 ):
		BaTaijyu = "510"
	elif( 520 <= int(BaTaijyu) ):
		BaTaijyu = "520~"
	Data["BaTaijyu"][BaTaijyu][key] += value


	#馬体重差（"~-24", "-24~-16", "-16~-8", "-8~0", "0", "0~+8", "+8~+16", "+16~+24", "+24~"）
	if( (UMA_RACE["ZogenSa"] == "999" or UMA_RACE["ZogenSa"] == "") == False):

		ZogenSa = int(UMA_RACE["ZogenSa"])

		if(UMA_RACE["ZogenFugo"] == "-"): ZogenSa = - ZogenSa
		if(ZogenSa < -24):
			BaTaijyuSa = "~-24"
		elif( -24 <= ZogenSa < -16 ):
			BaTaijyuSa = "-24"
		elif( -16 <= ZogenSa < -8 ):
			BaTaijyuSa = "-16"
		elif( -8 <= ZogenSa < 0 ):
			BaTaijyuSa = "-8"
		elif( ZogenSa == 0 ):
			BaTaijyuSa = "0"
		elif( 0 < ZogenSa <= 8 ):
			BaTaijyuSa = "+8"
		elif( 8 < ZogenSa <= 16 ):
			BaTaijyuSa = "+16"
		elif( 16 < ZogenSa <= 24 ):
			BaTaijyuSa = "+24"
		elif( 24 < ZogenSa ):
			BaTaijyuSa = "+24~"

		Data["BaTaijyuSa"][BaTaijyuSa][key] += value


	#レース間隔  "0", "1", "2", "3", "4", "5~8", "9~12", "13~16", "17~20", "21~" 
	if("Interval" in UMA_RACE): 
		Interval = UMA_RACE["Interval"]
	else:
		Interval = U.getRaceInterval( UMA_RACE["KettoNum"], UMA_RACE["Year"], UMA_RACE["MonthDay"])
		UMA_RACE["Interval"] = Interval

	if( Interval != False ):
		if( Interval <= 4 ):
			RaceInterval = str(Interval)
		elif( Interval <= 8 ):
			RaceInterval = "5~8"
		elif( Interval <= 12 ):
			RaceInterval = "9~12"
		elif( Interval <= 16 ):
			RaceInterval = "13~16"
		elif( Interval <= 20 ):
			RaceInterval = "17~20"
		else:
			RaceInterval = "21~"
		Data["RaceInterval"][RaceInterval][key] += value


	#前走　競馬場
	zensoJyoCD = zensoRACE["JyoCD"]
	Data["zensoJyoCD"][zensoJyoCD][key] += value

	#前走　芝・ダート
	if(int(zensoRACE["TrackCD"]) <= 22):
		Data["zensoShibaDirt"]["Shiba"][key] += value
	else:
		Data["zensoShibaDirt"]["Dirt"][key] += value

	#前走との距離差（"-1000", "-800", "-600", "-400", "-200", "0", "+200", "+400", "+600", "+800", "+1000"）
	#前走距離
	zensoKyori = zensoRACE["Kyori"]
	#該当レースの距離
	Kyori = RACE["Kyori"]
	if(int(Kyori) - int(zensoKyori) <-800):
		zensoKyoriSa = "~-800"
	elif( -800 <= int(Kyori) - int(zensoKyori) < -600):
		zensoKyoriSa = "-800"
	elif( -600 <= int(Kyori) - int(zensoKyori) < -400):
		zensoKyoriSa = "-600"
	elif( -400 <= int(Kyori) - int(zensoKyori) < -200):
		zensoKyoriSa = "-400"
	elif( -200 <= int(Kyori) - int(zensoKyori) < 0):
		zensoKyoriSa = "-200"
	elif(int(Kyori) - int(zensoKyori) == 0):
		zensoKyoriSa = "0"
	elif( 0 < int(Kyori) - int(zensoKyori) <= 200):
		zensoKyoriSa = "+200"
	elif( 200 < int(Kyori) - int(zensoKyori) <= 400):
		zensoKyoriSa = "+400"
	elif( 400 < int(Kyori) - int(zensoKyori) <= 600):
		zensoKyoriSa = "+600"
	elif( 600 < int(Kyori) - int(zensoKyori) <= 800):
		zensoKyoriSa = "+800"
	elif( 800 < int(Kyori) - int(zensoKyori) ):
		zensoKyoriSa = "+800~"
	Data["zensoKyoriSa"][zensoKyoriSa][key] += value

	#前走　順位（1位2位3位4位5位6位7位8位9位10位以上）
	#確定順位
	zensoJyuni = int(zensoUMA_RACE["KakuteiJyuni"])
	#競走中止を除外
	if( zensoJyuni != 0): 
		if( zensoJyuni <= 9 ):
			zensoJyuni = str(zensoJyuni)
		else:
			zensoJyuni = "10~"
		Data["zensoJyuni"][zensoJyuni][key] += value

	#前走　オッズ
	zensoOdds_int = int(int(zensoUMA_RACE["Odds"])/10)
	if(zensoOdds_int<=14):
		Data["zensoOdds"][str(zensoOdds_int)][key] += value
	else:
		Data["zensoOdds"]["15~"][key] += value


	#前走　上がり順位（1位2位3位4位5位6位7位8位9位10位以上）
	if("zensoAgariJyuni" in UMA_RACE): 
		zensoAgariJyuni = UMA_RACE["zensoAgariJyuni"]
	else:
		zensoAgariJyuni = U.getZensoAgariJyuni( UMA_RACE["KettoNum"], zensoUMA_RACE )
		UMA_RACE["zensoAgariJyuni"] = zensoAgariJyuni

	#競走中止を除外
	if(zensoAgariJyuni != 0): 
		if( zensoAgariJyuni <= 9 ):
			Data["zensoAgariJyuni"][str(zensoAgariJyuni)][key] += value
		else:
			Data["zensoAgariJyuni"]["10~"][key] += value


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

			print ("【" + U.getCodeValue( "2009", TrackCD, 2 ) + " " + Kyori + "m（"+ str(int(Ninki)) + "人気）】"  )

			#競走種別　"11":サラ２才, "12":サラ３才, "13":サラ３上, "14":サラ４上
			SyubetuCDs = ["11", "12", "13", "14"]
			Data["SyubetuCD"] = {}
			for SyubetuCD in SyubetuCDs:
				Data["SyubetuCD"][SyubetuCD] = {"kaime" : 0, "tansho_atari" : 0, "tansho_haraimodoshi" : 0, "fukusho_atari" : 0, "fukusho_haraimodoshi" : 0}

			#牝馬限定フラグ "True", "False" 
			HinbaGenteis = ["True", "False"]
			Data["HinbaGentei"] = {}
			for HinbaGentei in HinbaGenteis:
				Data["HinbaGentei"][HinbaGentei] = {"kaime" : 0, "tansho_atari" : 0, "tansho_haraimodoshi" : 0, "fukusho_atari" : 0, "fukusho_haraimodoshi" : 0}

			#重量種別 "1":ハンデ, "2":別定, "3":馬齢, "4":定量
			JyuryoCDs = ["1", "2", "3", "4"]
			Data["JyuryoCD"] = {}
			for JyuryoCD in JyuryoCDs:
				Data["JyuryoCD"][JyuryoCD] = {"kaime" : 0, "tansho_atari" : 0, "tansho_haraimodoshi" : 0, "fukusho_atari" : 0, "fukusho_haraimodoshi" : 0}

			#競走条件 "701":新馬, "703":未勝利,  "005":1勝クラス（500万以下）, "010":2勝クラス（1000万以下）, "016":3勝クラス（1600万以下）, "999":オープン（コード：2007）
			JyokenCD5s = ["701", "703", "005", "010", "016", "999"]
			Data["JyokenCD5"] = {}
			for JyokenCD5 in JyokenCD5s:
				Data["JyokenCD5"][JyokenCD5] = {"kaime" : 0, "tansho_atari" : 0, "tansho_haraimodoshi" : 0, "fukusho_atari" : 0, "fukusho_haraimodoshi" : 0}

			#グレード " ":条件戦, "L":リステッド競走, "E":特別競走, "D":グレード無し重賞, "C":G3, "B":G2, "A":G1 
			GradeCDs = [" ", "L", "E", "D", "C", "B", "A" ]
			Data["GradeCD"] = {}
			for GradeCD in GradeCDs:
				Data["GradeCD"][GradeCD] = {"kaime" : 0, "tansho_atari" : 0, "tansho_haraimodoshi" : 0, "fukusho_atari" : 0, "fukusho_haraimodoshi" : 0}

			#馬場状態 "1":良, "2":稍重, "3":重, "4":不良
			BabaCDs = ["1", "2", "3", "4"]
			Data["BabaCD"] = {}
			for BabaCD in BabaCDs:
				Data["BabaCD"][BabaCD] = {"kaime" : 0, "tansho_atari" : 0, "tansho_haraimodoshi" : 0, "fukusho_atari" : 0, "fukusho_haraimodoshi" : 0}

			#馬齢 "02":２歳, "03":３歳, "04":４歳, "05":５歳, "06":６歳, "07~":７歳以上
			Bareis = ["02", "03", "04", "05", "06", "07~"]
			Data["Barei"] = {}
			for Barei in Bareis:
				Data["Barei"][Barei] = {"kaime" : 0, "tansho_atari" : 0, "tansho_haraimodoshi" : 0, "fukusho_atari" : 0, "fukusho_haraimodoshi" : 0}

			#性別 "1":牡馬, "2":牝馬, "3":馬
			SexCDs = ["1", "2", "3"]
			Data["SexCD"] = {}
			for SexCD in SexCDs:
				Data["SexCD"][SexCD] = {"kaime" : 0, "tansho_atari" : 0, "tansho_haraimodoshi" : 0, "fukusho_atari" : 0, "fukusho_haraimodoshi" : 0}

			#枠番 "1":１枠, "2":２枠, "3":３枠, "4":４枠, "5":５枠, "6":６枠, "7":７枠, "8":８枠
			Wakubans = ["1", "2", "3", "4", "5", "6", "7", "8"]
			Data["Wakuban"] = {}
			for Wakuban in Wakubans:
				Data["Wakuban"][Wakuban] = {"kaime" : 0, "tansho_atari" : 0, "tansho_haraimodoshi" : 0, "fukusho_atari" : 0, "fukusho_haraimodoshi" : 0}

			#オッズ
			Oddss = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15~"]
			Data["Odds"] = {}
			for Odds in Oddss:
				Data["Odds"][Odds] = {"kaime" : 0, "tansho_atari" : 0, "tansho_haraimodoshi" : 0, "fukusho_atari" : 0, "fukusho_haraimodoshi" : 0}

			#脚質 "1":逃げ, "2":先行, "3":差し, "4":追込
			Kyakusitus = ["1", "2", "3", "4"]
			Data["Kyakusitu"] = {}
			for Kyakusitu in Kyakusitus:
				Data["Kyakusitu"][Kyakusitu] = {"kaime" : 0, "tansho_atari" : 0, "tansho_haraimodoshi" : 0, "fukusho_atari" : 0, "fukusho_haraimodoshi" : 0}

			#馬体重
			BaTaijyus = ["~430", "430", "440", "450", "460", "470", "480", "490", "500", "510", "520~"]
			Data["BaTaijyu"] = {}
			for BaTaijyu in BaTaijyus:
				Data["BaTaijyu"][BaTaijyu] = {"kaime" : 0, "tansho_atari" : 0, "tansho_haraimodoshi" : 0, "fukusho_atari" : 0, "fukusho_haraimodoshi" : 0}

			#馬体重差
			BaTaijyuSas = ["~-24", "-24", "-16", "-8", "0", "+8", "+16", "+24", "+24~"]
			Data["BaTaijyuSa"] = {}
			for BaTaijyuSa in BaTaijyuSas:
				Data["BaTaijyuSa"][BaTaijyuSa] = {"kaime" : 0, "tansho_atari" : 0, "tansho_haraimodoshi" : 0, "fukusho_atari" : 0, "fukusho_haraimodoshi" : 0}

			#レース間隔  "0", "1", "2", "3", "4", "5~8", "9~12", "13~16", "17~20", "21~"  
			RaceIntervals = [ "0", "1", "2", "3", "4", "5~8", "9~12", "13~16", "17~20", "21~" ]
			Data["RaceInterval"] = {}
			for RaceInterval in RaceIntervals:
				Data["RaceInterval"][RaceInterval] = {"kaime" : 0, "tansho_atari" : 0, "tansho_haraimodoshi" : 0, "fukusho_atari" : 0, "fukusho_haraimodoshi" : 0}

			#前走　競馬場
			zensoJyoCDs = [ "01", "02", "03", "04", "05", "06", "07", "08", "09", "10" ]
			Data["zensoJyoCD"] = {}
			for zensoJyoCD in zensoJyoCDs:
				Data["zensoJyoCD"][zensoJyoCD] = {"kaime" : 0, "tansho_atari" : 0, "tansho_haraimodoshi" : 0, "fukusho_atari" : 0, "fukusho_haraimodoshi" : 0}

			#前走　芝・ダート
			zensoShibaDirts = ["Shiba", "Dirt"]
			Data["zensoShibaDirt"] = {}
			for zensoShibaDirt in zensoShibaDirts:
				Data["zensoShibaDirt"][zensoShibaDirt] = {"kaime" : 0, "tansho_atari" : 0, "tansho_haraimodoshi" : 0, "fukusho_atari" : 0, "fukusho_haraimodoshi" : 0}

			#前走との距離差
			zensoKyoriSas = ["~-800", "-800", "-600", "-400", "-200", "0", "+200", "+400", "+600", "+800", "+800~"]
			Data["zensoKyoriSa"] = {}
			for zensoKyoriSa in zensoKyoriSas:
				Data["zensoKyoriSa"][zensoKyoriSa] = {"kaime" : 0, "tansho_atari" : 0, "tansho_haraimodoshi" : 0, "fukusho_atari" : 0, "fukusho_haraimodoshi" : 0}

			#前走　オッズ
			zensoOddss = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15~"]
			Data["zensoOdds"] = {}
			for zensoOdds in zensoOddss:
				Data["zensoOdds"][zensoOdds] = {"kaime" : 0, "tansho_atari" : 0, "tansho_haraimodoshi" : 0, "fukusho_atari" : 0, "fukusho_haraimodoshi" : 0}

			#前走　順位
			zensoJyunis = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10~"]
			Data["zensoJyuni"] = {}
			for zensoJyuni in zensoJyunis:
				Data["zensoJyuni"][zensoJyuni] = {"kaime" : 0, "tansho_atari" : 0, "tansho_haraimodoshi" : 0, "fukusho_atari" : 0, "fukusho_haraimodoshi" : 0}

			#前走　上がり順位
			zensoAgariJyunis = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10~"]
			Data["zensoAgariJyuni"] = {}
			for zensoAgariJyuni in zensoAgariJyunis:
				Data["zensoAgariJyuni"][zensoAgariJyuni] = {"kaime" : 0, "tansho_atari" : 0, "tansho_haraimodoshi" : 0, "fukusho_atari" : 0, "fukusho_haraimodoshi" : 0}

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
						text += UMA_RACE["KakuteiJyuni"] + "位 "

						#前走馬毎レース情報
						zensoUMA_RACE = U.getZensoUMA_RACE( UMA_RACE["KettoNum"], UMA_RACE["Year"], UMA_RACE["MonthDay"])
						if( zensoUMA_RACE == False ): continue
						#前走レース情報
						zensoRACE = U.getZensoRACE( UMA_RACE["KettoNum"], zensoUMA_RACE)
						if( zensoRACE == False ): continue

						#該当馬
						setData( "kaime", 1, RACE, UMA_RACE, zensoRACE, zensoUMA_RACE )

						#単勝的中の場合
						for i in range(3):
							n = str(i + 1)
							if(HARAI["PayTansyoUmaban" + n] == UMA_RACE["Umaban"]):
								setData( "tansho_atari", 1, RACE, UMA_RACE, zensoRACE, zensoUMA_RACE )
								setData( "tansho_haraimodoshi", int(HARAI["PayTansyoPay" + n]), RACE, UMA_RACE, zensoRACE, zensoUMA_RACE )

						#複勝的中の場合
						for i in range(5):
							n = str(i + 1)
							if(HARAI["PayFukusyoUmaban" + n] == UMA_RACE["Umaban"]):
								setData( "fukusho_atari", 1, RACE, UMA_RACE, zensoRACE, zensoUMA_RACE )
								setData( "fukusho_haraimodoshi", int(HARAI["PayFukusyoPay" + n]), RACE, UMA_RACE, zensoRACE, zensoUMA_RACE )

						#ターミナルへ出力
						print(text)

			fout = open(dir_path + JyoCD + "/" + TrackCD + "-" + Kyori + "m" + Ninki + ".txt", "w")
			for k1 in Data:
				fout.write("\n")
				fout.write("買い目\t単勝度数\t単勝配当\t複勝度数\t複勝配当\n")
				for k2 in Data[k1]:
					data = Data[k1][k2]
					fout.write( 
						str(data["kaime"]) + "\t" +  
						str(data["tansho_atari"]) + "\t" +  
						str(data["tansho_haraimodoshi"]) + "\t" +  
						str(data["fukusho_atari"]) + "\t" +  
						str(data["fukusho_haraimodoshi"]) + "\t" +  
					"\n")
				fout.write("\n")
			fout.close()

