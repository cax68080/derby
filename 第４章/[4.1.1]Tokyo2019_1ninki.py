#独自ライブラリのインポート
import utility as U

#2022年東京競馬場１番人気
Year = "2023"
JyoCD1 = "05"
JyoCD2 = "06"
Ninki = "01"

#SQL文
strSQL_SELECT = "SELECT * FROM N_RACE"
strSQL_WHERE  = " WHERE DataKubun = '7'"
strSQL_WHERE += " AND Year = '" + Year + "'" 
strSQL_WHERE += " AND JyoCD = '" + JyoCD1  + "'"
strSQL_ORDER = " ORDER BY MonthDay ASC"
#SQL文の連結
strSQL = strSQL_SELECT + strSQL_WHERE + strSQL_ORDER
#該当レースを取得
RACEs = U.getRACEs(strSQL)

#レース結果格納する配列：総数, １着, ２着, ３着
tyakuKaisu = [0] * 4
#単勝・複勝の的中回数
tansho_tekityuKaisu = 0
fukusho_tekityuKaisu = 0
#単勝・複勝の払戻総額
tansho_haraimodoshi_sum = 0
fukusho_haraimodoshi_sum = 0

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
	tyakuKaisu[0] += 1
	if( int(UMA_RACE["KakuteiJyuni"]) <= 3):
		tyakuKaisu[int(UMA_RACE["KakuteiJyuni"])] += 1
	#単勝的中の場合
	for i in range(3):
		n = str(i + 1)
		if(HARAI["PayTansyoUmaban" + n] == UMA_RACE["Umaban"]):
			tansho_haraimodoshi_sum += int(HARAI["PayTansyoPay" + n])
			tansho_tekityuKaisu += 1
	#複勝的中の場合
	for i in range(5):
		n = str(i + 1)
		if(HARAI["PayFukusyoUmaban" + n] == UMA_RACE["Umaban"]):
			fukusho_haraimodoshi_sum += int(HARAI["PayFukusyoPay" + n])
			fukusho_tekityuKaisu += 1
	#ターミナルへ出力
	print(text)

#着外の回数
kyakugai = tyakuKaisu[0] - tyakuKaisu[1] - tyakuKaisu[2]- tyakuKaisu[3]
#単勝の的中率と回収率
tanshou_ritsu = round(tyakuKaisu[1] / tyakuKaisu[0] * 100, 1)
tanshou_kaishuritsu = round(tansho_haraimodoshi_sum/ tyakuKaisu[0], 1)
#複勝の的中率と回収率
fukusho_ritsu = round(fukusho_tekityuKaisu / tyakuKaisu[0] * 100, 1)
fukusho_kaishuritsu = round(fukusho_haraimodoshi_sum/ tyakuKaisu[0], 1)

#文字列整形
text = "--------------------------------------\n"
text += "1着-2着-3着-着外|該当レース数 ： "
text += str(tyakuKaisu[1]) + "-" + str(tyakuKaisu[2]) + "-" + str(tyakuKaisu[3]) + "-" + str(kyakugai) + "|" + str(tyakuKaisu[0]) + "\n"
text += "単勝率：" + str(tanshou_ritsu) + "%  回収率：" +str(tanshou_kaishuritsu) + "\n"
text += "複勝率：" + str(fukusho_ritsu) + "%  回収率：" +str(fukusho_kaishuritsu) + "\n"

#着回数
print(text)
