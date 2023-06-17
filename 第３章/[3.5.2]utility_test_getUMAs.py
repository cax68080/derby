#独自ライブラリのインポート
import utility as U

#SQL文
strSQL_SELECT = "SELECT * FROM N_UMA"
strSQL_WHERE  = " WHERE KettoNum = '2014106220'"
#SQL文の連結
strSQL = strSQL_SELECT + strSQL_WHERE

#該当競走馬を取得
UMAs = U.getUMAs(strSQL)
UMA = UMAs[0]

#時刻関連モジュールのインポート
import datetime
today = datetime.date.today()
#馬齢計算
b = UMA["BirthDate"]
b_year = int(b[0] + b[1] + b[2] + b[3])
barei = today.year - b_year

text ="-----------------------------------------------------------------------------------------------------"+ "\n"
text += "馬名 " + U.getCodeValue( "2204",  UMA["UmaKigoCD"] ,1) + UMA["Bamei"] + " "
text += U.getCodeValue( "2202", UMA["SexCD"], 1) + " " + str(barei) + "歳 " +  U.getCodeValue( "2203", UMA["KeiroCD"], 1) 
if(UMA["DelKubun"] == "0"): text += "（現役）"
if(UMA["DelKubun"] == "1"): text += "（抹消）"
text += "\n"
text +="-----------------------------------------------------------------------------------------------------"+ "\n"

text += "生年月日 " + str(b_year) + "年" + b[4] + b[5] + "月" + b[6] + b[7] + "日\n"
text += "調教師名 " + UMA["ChokyosiRyakusyo"] + "（" +  U.getCodeValue( "2301", UMA["TozaiCD"], 2) +  "）\n"
text += "生産者名 " + UMA["BreederName"] + "\n"
text += "産地名 " + UMA["SanchiName"] + "\n"
text += "馬主名 " + UMA["BanusiName"] + "\n"
text += "父" + UMA["Ketto3InfoBamei1"] + " （父父 "+ UMA["Ketto3InfoBamei3"] + "  父母 "+ UMA["Ketto3InfoBamei4"]  + "）\n"
text += "母 " + UMA["Ketto3InfoBamei2"] + " （母父 "+ UMA["Ketto3InfoBamei5"] + "  母母 " + UMA["Ketto3InfoBamei6"] + "）\n"

s = int(int(UMA["RuikeiHonsyoHeiti"])/100) + int(int(UMA["RuikeiFukaHeichi"])/100)
s1 = int(s / 10000)
s2 = s - s1 * 10000
text += "獲得賞金 " 
if(s1 > 0): text += str(s1) + "億"
text += str(s2) + "万円（中央のみ）\n"

SogoChakukaisu = int(UMA["SogoChakukaisu1"]) + int(UMA["SogoChakukaisu2"]) + int(UMA["SogoChakukaisu3"]) + int(UMA["SogoChakukaisu4"]) + int(UMA["SogoChakukaisu5"]) + int(UMA["SogoChakukaisu6"])

text += "通算成績" + " " + str(SogoChakukaisu) + "戦" + str(int(UMA["SogoChakukaisu1"])) + "勝 "
text += "[" + str(int(UMA["SogoChakukaisu1"])) + "-" + str(int(UMA["SogoChakukaisu2"])) + "-"
text += str(int(UMA["SogoChakukaisu3"])) + "-" + str(int(UMA["SogoChakukaisu4"])) + "-"
text += str(int(UMA["SogoChakukaisu5"])) + "-" + str(int(UMA["SogoChakukaisu6"])) + "]（中央＋地方＋海外)\n"

text += "脚質 [逃-先-差-追]：[" + str(int(UMA["Kyakusitu1"])) + "-" + str(int(UMA["Kyakusitu2"]))
text += "-" + str(int(UMA["Kyakusitu3"])) + "-" + str(int(UMA["Kyakusitu4"])) + "]" + "\n"
text +="-----------------------" + "\n"

#ターミナルへ出力
print(text)
