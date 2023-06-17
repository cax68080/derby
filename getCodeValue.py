# コード表リスト
CodeTable = []
# 外部ファイルの読み込み
f_in = open("./CodeTable.csv")
# コード表リストの生成
for line in f_in.readlines():
    values = line.split(",")
    #print(values)
    CodeTable.append(values)
# ファイルクローズ
f_in.close()
# 「コード」⇒「値」変換関数「getCodeValue」の定義
def getCodeValue(code,key,type):
    for c in CodeTable:
        if(c[0] == code and c[1] == key): return c[type + 1]
# 実行結果の確認
#value = getCodeValue("2001","01",1)
#print(value)