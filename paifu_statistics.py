import json,sys
import pathlib,glob

'''牌譜の構成
'log':[[ [1局目,本場,積棒],
        [点数状況]
        [表ドラ]
        [裏ドラ]
        [起家配牌]
        [起家ツモ(鳴き)]
        [起家河(リーチ)]
        [南家配牌]
        [南家ツモ(鳴き)]
        …
        [北家河(リーチ)]
        [[和了or流局],[点数移動],[和了者,放縦者(一緒の場合はツモ),パオ,点数,アガリ役]] ],
        [[2局目,本場,積棒],
         …],
    ] 
'''
player_data = {}

def inStr(arr):
    for a in arr:
        if type(a) is str:
            return True
    return False

for File in glob.glob("*.json"):
    Json = json.load(open(File,'r',encoding="utf-8_sig"))
    paifu, name, score = Json['log'], Json['name'], Json['sc']
    
    result = [round[-1] for round in paifu]
    kyokusu = len(paifu)
    agari = [0,0,0,0]
    agari_total = [0,0,0,0]
    tsumo = [0,0,0,0]
    houju = [0,0,0,0]
    houju_total = [0,0,0,0]
    riichi = [0,0,0,0]
    fuuro = [0,0,0,0]


    for round in paifu:
        [kyoku,honba,tusmibou] = round[0]
        result = round[-1]
        draw = round[5:-2:3]
        kawa = round[6:-1:3]
        riibou = 0

        for i in range(4):
            if inStr(draw[i]): fuuro[i]+=1
            if inStr(kawa[i]): riichi[i]+=1; riibou+=1

        if result[0] != "和了": continue
        [who,fromWhere] = [result[2][0],result[2][1]]
        agari[who] += 1
        point = (result[1][who] - honba*300 - tusmibou*1000 - riibou*1000)
        agari_total[who] += point

        if who == fromWhere:
            tsumo[who]+=1
        else:
            houju[fromWhere]+=1
            houju_total[fromWhere] += point

    for i in range(4):
        if name[i] not in player_data: player_data[name[i]] = [kyokusu,agari[i],agari_total[i],tsumo[i],houju[i],houju_total[i],riichi[i],fuuro[i]]
        else: 
            data = player_data[name[i]]
            player_data[name[i]] = [x[0]+x[1] for x in zip(data,[kyokusu,agari[i],agari_total[i],tsumo[i],houju[i],houju_total[i],riichi[i],fuuro[i]]) ]
    
for p in player_data.keys():
    player_data[p] = [player_data[p][0],
                        player_data[p][1]/player_data[p][0]*100,
                        0 if player_data[p][1]==0 else (player_data[p][2]/player_data[p][1]),
                        player_data[p][3]/player_data[p][0]*100,
                        player_data[p][4]/player_data[p][0]*100,
                        0 if player_data[p][4]==0 else (player_data[p][5]/player_data[p][4]),
                        player_data[p][6]/player_data[p][0]*100,
                        player_data[p][7]/player_data[p][0]*100]
    ##print(player_data[p])

print("プレイヤ名、局数、和了率、平均和了点、ツモ率、放縦率、平均放銃点、リーチ率、副露率")
for i in player_data.items():
    print(i)


'''
print("局数:",kyokusu)
    print(name)
    print("和了率",[a/kyokusu for a in agari])
    print("平均和了",[0 if a[1]==0 else a[0]/a[1] for a in zip(agari_total,agari)])
    print("ツモ率",[a/kyokusu for a in tsumo])
    print("放銃率",[a/kyokusu for a in houju])
    print("平均放銃",[0 if a[1]==0 else a[0]/a[1] for a in zip(houju_total,houju)])
    print("リーチ率",[a/kyokusu for a in riichi])
    print("副露率",[a/kyokusu for a in fuuro])
    '''
    