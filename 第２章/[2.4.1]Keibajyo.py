###########################################################################
# 競馬場ごとのコース情報が格納された辞書型
Courses = {}
#札幌競馬場
Courses["01"] = [] 
Courses["01"].append( { "TrackCD" : "17" , "Kyori" : "1200" } ) #芝・右
Courses["01"].append( { "TrackCD" : "17" , "Kyori" : "1500" } ) #芝・右
Courses["01"].append( { "TrackCD" : "17" , "Kyori" : "1800" } ) #芝・右
Courses["01"].append( { "TrackCD" : "17" , "Kyori" : "2000" } ) #芝・右
Courses["01"].append( { "TrackCD" : "17" , "Kyori" : "2600" } ) #芝・右
Courses["01"].append( { "TrackCD" : "24" , "Kyori" : "1000" } ) #ダート・右
Courses["01"].append( { "TrackCD" : "24" , "Kyori" : "1700" } ) #ダート・右
Courses["01"].append( { "TrackCD" : "24" , "Kyori" : "2400" } ) #ダート・右
#函館競馬場
Courses["02"] = [] 
Courses["02"].append( { "TrackCD" : "17" , "Kyori" : "1000" } ) #芝・右（殆どなし）
Courses["02"].append( { "TrackCD" : "17" , "Kyori" : "1200" } ) #芝・右
Courses["02"].append( { "TrackCD" : "17" , "Kyori" : "1800" } ) #芝・右
Courses["02"].append( { "TrackCD" : "17" , "Kyori" : "2000" } ) #芝・右
Courses["02"].append( { "TrackCD" : "17" , "Kyori" : "2600" } ) #芝・右
Courses["02"].append( { "TrackCD" : "24" , "Kyori" : "1000" } ) #ダート・右
Courses["02"].append( { "TrackCD" : "24" , "Kyori" : "1700" } ) #ダート・右
Courses["02"].append( { "TrackCD" : "24" , "Kyori" : "2400" } ) #ダート・右
#福島競馬場
Courses["03"] = [] 
Courses["03"].append( { "TrackCD" : "17" , "Kyori" : "1200" } ) #芝・右
Courses["03"].append( { "TrackCD" : "17" , "Kyori" : "1800" } ) #芝・右
Courses["03"].append( { "TrackCD" : "17" , "Kyori" : "2000" } ) #芝・右
Courses["03"].append( { "TrackCD" : "17" , "Kyori" : "2600" } ) #芝・右
Courses["03"].append( { "TrackCD" : "24" , "Kyori" : "1150" } ) #ダート・右
Courses["03"].append( { "TrackCD" : "24" , "Kyori" : "1700" } ) #ダート・右
Courses["03"].append( { "TrackCD" : "24" , "Kyori" : "2400" } ) #ダート・右（殆どなし）
#新潟競馬場
Courses["04"] = [] 
Courses["04"].append( { "TrackCD" : "10" , "Kyori" : "1000" } ) #直線
Courses["04"].append( { "TrackCD" : "11" , "Kyori" : "1200" } ) #芝・左・内回り
Courses["04"].append( { "TrackCD" : "11" , "Kyori" : "1400" } ) #芝・左・内回り
Courses["04"].append( { "TrackCD" : "11" , "Kyori" : "2000" } ) #芝・左・内回り
Courses["04"].append( { "TrackCD" : "11" , "Kyori" : "2200" } ) #芝・左・内回り
Courses["04"].append( { "TrackCD" : "11" , "Kyori" : "2400" } ) #芝・左・内回り
Courses["04"].append( { "TrackCD" : "12" , "Kyori" : "1600" } ) #芝・左・外回り
Courses["04"].append( { "TrackCD" : "12" , "Kyori" : "1800" } ) #芝・左・外回り
Courses["04"].append( { "TrackCD" : "12" , "Kyori" : "2000" } ) #芝・左・外回り
Courses["04"].append( { "TrackCD" : "23" , "Kyori" : "1200" } ) #ダート・左
Courses["04"].append( { "TrackCD" : "23" , "Kyori" : "1800" } ) #ダート・左
Courses["04"].append( { "TrackCD" : "23" , "Kyori" : "2500" } ) #ダート・左（殆どなし）
#東京競馬場
Courses["05"] = [] 
Courses["05"].append( { "TrackCD" : "11" , "Kyori" : "1400" } ) #芝・左
Courses["05"].append( { "TrackCD" : "11" , "Kyori" : "1600" } ) #芝・左
Courses["05"].append( { "TrackCD" : "11" , "Kyori" : "1800" } ) #芝・左
Courses["05"].append( { "TrackCD" : "11" , "Kyori" : "2000" } ) #芝・左
Courses["05"].append( { "TrackCD" : "11" , "Kyori" : "2300" } ) #芝・左（殆どなし）
Courses["05"].append( { "TrackCD" : "11" , "Kyori" : "2400" } ) #芝・左
Courses["05"].append( { "TrackCD" : "11" , "Kyori" : "2500" } ) #芝・左（殆どなし）
Courses["05"].append( { "TrackCD" : "11" , "Kyori" : "3400" } ) #芝・左（殆どなし）
Courses["05"].append( { "TrackCD" : "23" , "Kyori" : "1300" } ) #ダート・左
Courses["05"].append( { "TrackCD" : "23" , "Kyori" : "1400" } ) #ダート・左
Courses["05"].append( { "TrackCD" : "23" , "Kyori" : "1600" } ) #ダート・左
Courses["05"].append( { "TrackCD" : "23" , "Kyori" : "2100" } ) #ダート・左
Courses["05"].append( { "TrackCD" : "23" , "Kyori" : "2400" } ) #ダート・左（殆どなし）
#中山競馬場
Courses["06"] = [] 
Courses["06"].append( { "TrackCD" : "17" , "Kyori" : "1800" } ) #芝・右
Courses["06"].append( { "TrackCD" : "17" , "Kyori" : "2000" } ) #芝・右
Courses["06"].append( { "TrackCD" : "17" , "Kyori" : "2500" } ) #芝・右
Courses["06"].append( { "TrackCD" : "18" , "Kyori" : "1200" } ) #芝・右・外回り
Courses["06"].append( { "TrackCD" : "18" , "Kyori" : "1600" } ) #芝・右・外回り
Courses["06"].append( { "TrackCD" : "18" , "Kyori" : "2200" } ) #芝・右・外回り
Courses["06"].append( { "TrackCD" : "21" , "Kyori" : "3600" } ) #芝・右・２周
Courses["06"].append( { "TrackCD" : "24" , "Kyori" : "1200" } ) #ダート・右
Courses["06"].append( { "TrackCD" : "24" , "Kyori" : "1800" } ) #ダート・右
Courses["06"].append( { "TrackCD" : "24" , "Kyori" : "2400" } ) #ダート・右
Courses["06"].append( { "TrackCD" : "24" , "Kyori" : "2500" } ) #ダート・右（殆どなし）
#中京競馬場
Courses["07"] = [] 
Courses["07"].append( { "TrackCD" : "11" , "Kyori" : "1200" } ) #芝・左
Courses["07"].append( { "TrackCD" : "11" , "Kyori" : "1400" } ) #芝・左
Courses["07"].append( { "TrackCD" : "11" , "Kyori" : "1600" } ) #芝・左
Courses["07"].append( { "TrackCD" : "11" , "Kyori" : "2000" } ) #芝・左
Courses["07"].append( { "TrackCD" : "11" , "Kyori" : "2200" } ) #芝・左
Courses["07"].append( { "TrackCD" : "23" , "Kyori" : "1200" } ) #ダート・左
Courses["07"].append( { "TrackCD" : "23" , "Kyori" : "1400" } ) #ダート・左
Courses["07"].append( { "TrackCD" : "23" , "Kyori" : "1800" } ) #ダート・左
Courses["07"].append( { "TrackCD" : "23" , "Kyori" : "1900" } ) #ダート・左
#京都競馬場
Courses["08"] = [] 
Courses["08"].append( { "TrackCD" : "17" , "Kyori" : "1200" } ) #芝・右・内回り
Courses["08"].append( { "TrackCD" : "17" , "Kyori" : "1400" } ) #芝・右・内回り
Courses["08"].append( { "TrackCD" : "17" , "Kyori" : "1600" } ) #芝・右・内回り
Courses["08"].append( { "TrackCD" : "17" , "Kyori" : "2000" } ) #芝・右・内回り
Courses["08"].append( { "TrackCD" : "18" , "Kyori" : "1400" } ) #芝・右・外回り
Courses["08"].append( { "TrackCD" : "18" , "Kyori" : "1600" } ) #芝・右・外回り
Courses["08"].append( { "TrackCD" : "18" , "Kyori" : "1800" } ) #芝・右・外回り
Courses["08"].append( { "TrackCD" : "18" , "Kyori" : "2200" } ) #芝・右・外回り
Courses["08"].append( { "TrackCD" : "18" , "Kyori" : "2400" } ) #芝・右・外回り
Courses["08"].append( { "TrackCD" : "18" , "Kyori" : "3000" } ) #芝・右・外回り（殆どなし）
Courses["08"].append( { "TrackCD" : "18" , "Kyori" : "3200" } ) #芝・右・外回り（殆どなし）
Courses["08"].append( { "TrackCD" : "24" , "Kyori" : "1200" } ) #ダート・右
Courses["08"].append( { "TrackCD" : "24" , "Kyori" : "1400" } ) #ダート・右
Courses["08"].append( { "TrackCD" : "24" , "Kyori" : "1800" } ) #ダート・右
Courses["08"].append( { "TrackCD" : "24" , "Kyori" : "1900" } ) #ダート・右
#阪神競馬場
Courses["09"] = [] 
Courses["09"].append( { "TrackCD" : "17" , "Kyori" : "1200" } ) #芝・右・内回り
Courses["09"].append( { "TrackCD" : "17" , "Kyori" : "1400" } ) #芝・右・内回り
Courses["09"].append( { "TrackCD" : "17" , "Kyori" : "2000" } ) #芝・右・内回り
Courses["09"].append( { "TrackCD" : "17" , "Kyori" : "2200" } ) #芝・右・内回り
Courses["09"].append( { "TrackCD" : "17" , "Kyori" : "3000" } ) #芝・右（殆どなし）
Courses["09"].append( { "TrackCD" : "18" , "Kyori" : "1600" } ) #芝・右・外回り
Courses["09"].append( { "TrackCD" : "18" , "Kyori" : "1800" } ) #芝・右・外回り
Courses["09"].append( { "TrackCD" : "18" , "Kyori" : "2400" } ) #芝・右・外回り
Courses["09"].append( { "TrackCD" : "18" , "Kyori" : "2600" } ) #芝・右・外回り（殆どなし）
Courses["09"].append( { "TrackCD" : "24" , "Kyori" : "1200" } ) #ダート・右
Courses["09"].append( { "TrackCD" : "24" , "Kyori" : "1400" } ) #ダート・右
Courses["09"].append( { "TrackCD" : "24" , "Kyori" : "1800" } ) #ダート・右
Courses["09"].append( { "TrackCD" : "24" , "Kyori" : "2000" } ) #ダート・右
#小倉競馬場
Courses["10"] = [] 
Courses["10"].append( { "TrackCD" : "17" , "Kyori" : "1200" } ) #芝・右
Courses["10"].append( { "TrackCD" : "17" , "Kyori" : "1700" } ) #芝・右（殆どなし）
Courses["10"].append( { "TrackCD" : "17" , "Kyori" : "1800" } ) #芝・右
Courses["10"].append( { "TrackCD" : "17" , "Kyori" : "2000" } ) #芝・右
Courses["10"].append( { "TrackCD" : "17" , "Kyori" : "2600" } ) #芝・右
Courses["10"].append( { "TrackCD" : "24" , "Kyori" : "1000" } ) #ダート・右
Courses["10"].append( { "TrackCD" : "24" , "Kyori" : "1700" } ) #ダート・右
Courses["10"].append( { "TrackCD" : "24" , "Kyori" : "2400" } ) #ダート・右（殆どなし）
