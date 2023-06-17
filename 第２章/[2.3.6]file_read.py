#ファイルオープン
file = open('test.txt')
#行の取得
lines = file.readlines()
#行ごとの取得
for line in lines:
	line = line.replace('\n', '')
	print(line)
#ファイルクローズ
file.close()