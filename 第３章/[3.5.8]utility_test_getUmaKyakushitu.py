#独自ライブラリのインポート
import utility as U

#リスグラシュー
KettoNum = "2014106220"
#有馬記念（引退レース）
Year = "2019"
MonthDay = "1222"

#脚質判定
UmaKyakushitu = U.getUmaKyakushitu( KettoNum, Year, MonthDay)

if(UmaKyakushitu == 1): text = "逃"
if(UmaKyakushitu == 2): text = "先"
if(UmaKyakushitu == 3): text = "差"
if(UmaKyakushitu == 4): text = "追"
if(UmaKyakushitu == False): text = "−"

#ターミナルへ出力
print(text)
