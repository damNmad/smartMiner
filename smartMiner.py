#!/usr/bin/env python2.7
import requests;

DEFAULT_COIN = {'tag': "DUAL_SOIL_PASC"};

r = requests.get("http://whattomine.com/coins.json");
coinsData = r.json()['coins'];
coins = coinsData.keys();
lowDifficulty = {};

excludeTags = ['NICEHASH', 'KRB', 'XDN', 'SIB']

filterdCoins = {k: v for k, v in coinsData.iteritems() if v['tag'] not in excludeTags}
coins = filterdCoins.keys()
# print len(filterdCoins)


def findDifficulty(d1, d2):
    return ((d1 - d2) / ((d1 + d2) / 2)) * 100


for coin in coins:
    coinObj = coinsData[coin]
    coinObj['smartProfitability'] = findDifficulty(coinObj['difficulty'], coinObj['difficulty24'])
    lowDifficulty[coin] = coinObj

# for k in lowDifficulty:
#     print lowDifficulty[k]['tag'], ' - ', lowDifficulty[k]['smartProfitability']

# print sorted(filterdCoins.values(), key=lambda d: d['smartProfitability']);

difficultySort = sorted(filterdCoins.values(), key=lambda d: d['smartProfitability']);

finalCoin = DEFAULT_COIN;

if (len(difficultySort) > 1):
    finalCoin = difficultySort[0]

print finalCoin['tag'];
