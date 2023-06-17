#辞書型
D = {"K": 42, "S": 80, "E": 60}
print(D.items())
#昇順
D_sorted1 = sorted(D.items(), key=lambda x:x[1], reverse=False)
#降順
D_sorted2 = sorted(D.items(), key=lambda x:x[1], reverse=True)
#ターミナルへ出力
print(D_sorted1) # [('K', 42), ('E', 60), ('S', 80)]
print(D_sorted2) # [('S', 80), ('E', 60), ('K', 42)]

print(D_sorted1[0][0])
