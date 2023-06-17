#時刻関連モジュールのインポート
import datetime
#現在日付のオブジェクトを取得
today = datetime.date.today()
#指定日付のオブジェクトを取得
birthday = datetime.date(1978, 11, 28) 
#経過日数を計算
nenrei = today - birthday
#経過日数を取得
nenrei_day = nenrei.days
#経過日数を取得
nenrei_year = int(nenrei_day/365)
#年齢をコンソールへ表示
print( nenrei_year )