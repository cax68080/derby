#ファイルオープン
file = open("write.txt", "w")
for l in range(10):
	#ファイルへの書き込み
	file.write( str(l) + "\n")
#ファイルクローズ
file.close()