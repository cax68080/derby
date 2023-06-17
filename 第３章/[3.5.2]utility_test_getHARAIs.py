#独自ライブラリのインポート
import utility as U

#SQL文
strSQL_SELECT = "SELECT * FROM N_HARAI"
strSQL_WHERE  = " WHERE DataKubun = '2'"
strSQL_WHERE += " AND Year = '2019'"
strSQL_WHERE += " AND MonthDay = '1222'"
strSQL_WHERE += " AND JyoCD ='06'"
strSQL_WHERE += " AND RaceNum ='11'"
#SQL文の連結
strSQL = strSQL_SELECT + strSQL_WHERE

#該当払戻情報を取得
HARAIs = U.getHARAIs(strSQL)
HARAI = HARAIs[0]

#文字列整形
text = ""
text += "単勝："
for i in range(3):
	n = str(i + 1)
	if(HARAI["PayTansyoUmaban" + n] !=""):
		text += str(int(HARAI["PayTansyoUmaban" + n])) + "番 " + str(int(HARAI["PayTansyoPay" + n])) + "円（" + str(int(HARAI["PayTansyoNinki" + n])) + "人気） "
text += "\n"
text += "複勝："
for i in range(5):
	n = str(i + 1)
	if(HARAI["PayFukusyoUmaban" + n] !=""):
		text += str(int(HARAI["PayFukusyoUmaban" + n])) + "番 " + str(int(HARAI["PayFukusyoPay" + n])) + "円（" + str(int(HARAI["PayFukusyoNinki" + n])) + "人気） "
text += "\n"
text += "枠連："
for i in range(3):
	n = str(i + 1)
	kumi = HARAI["PayWakurenKumi" + n]
	if(kumi !=""):
		text += kumi[0] + "-" + kumi[1] + "  " + str(int(HARAI["PayWakurenPay" + n])) + "円（" + str(int(HARAI["PayWakurenNinki" + n])) + "人気） "
text += "\n"
text += "馬連："
for i in range(3):
	n = str(i + 1)
	kumi = HARAI["PayUmarenKumi" + n]	
	if( kumi !=""):
		text += str(int(kumi[0] + kumi[1])) + "-" + str(int(kumi[2] + kumi[3])) + "  " + str(int(HARAI["PayUmarenPay" + n])) + "円（" + str(int(HARAI["PayUmarenNinki" + n])) + "人気） "
text += "\n"
text += "ワイド："
for i in range(7):
	n = str(i + 1)
	kumi = HARAI["PayWideKumi" + n]	
	if( kumi !=""):
		text += str(int(kumi[0] + kumi[1])) + "-" + str(int(kumi[2] + kumi[3])) + "  " + str(int(HARAI["PayWidePay" + n])) + "円（" + str(int(HARAI["PayWideNinki" + n])) + "人気） "
text += "\n"
text += "3連複："
for i in range(3):
	n = str(i + 1)
	kumi = HARAI["PaySanrenpukuKumi" + n]	
	if( kumi !=""):	
		text += str(int(kumi[0] + kumi[1])) + "-" + str(int(kumi[2] + kumi[3])) + "-" + str(int(kumi[4] + kumi[5])) + "  " + str(int(HARAI["PaySanrenpukuPay" + n])) + "円（" + str(int(HARAI["PaySanrenpukuNinki" + n])) + "人気） "
text += "\n"
text += "3連単："
for i in range(6):
	n = str(i + 1)
	kumi = HARAI["PaySanrentanKumi" + n]	
	if( kumi !=""):	
		text += str(int(kumi[0] + kumi[1])) + "-" + str(int(kumi[2] + kumi[3])) + "-" + str(int(kumi[4] + kumi[5])) + "  " + str(int(HARAI["PaySanrentanPay" + n])) + "円（" + str(int(HARAI["PaySanrentanNinki" + n])) + "人気） "
text += "\n"

#ターミナルへ出力
print(text)