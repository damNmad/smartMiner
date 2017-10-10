#!/usr/bin/env python2.7
import requests;
import json

# Configurable Variables

#Current mining coin path
MINING_COIN_PATH = './smartMiner_Coin.json';
# Default coin
DEFAULT_COIN = {'tag': "DUAL_SOIL_PASC"};
# Avoid switching for small benefits
PERCENTAGE_VARIED = 10;


def refreshTopCoin():
    # Get current mining coin object
    currentCoin = DEFAULT_COIN;
    with open(MINING_COIN_PATH, 'r') as coinFile:
        currentCoin = json.load(coinFile)
        coinFile.close()

    r = requests.get("http://whattomine.com/coins.json");
    coinsData = r.json()['coins'];
    coins = coinsData.keys();
    topRevenue = {};

    includeTags = ['HUSH', 'ZEC', 'ZEN', 'ZCL', 'SIB', 'XDN', 'LBC']

    filterdCoins = {k: v for k, v in coinsData.iteritems() if v['tag'] in includeTags}
    coins = filterdCoins.keys()

    # print len(filterdCoins)


    def findDifficulty(d1, d2):
        return ((d1 - d2) / ((d1 + d2) / 2)) * 100

    for coin in coins:
        coinObj = coinsData[coin]
        coinObj['smartProfitability'] = coinObj['btc_revenue']
        topRevenue[coin] = coinObj

    # for k in topRevenue:
    #     print topRevenue[k]['tag'], ' - ', topRevenue[k]['smartProfitability']

    # print sorted(filterdCoins.values(), key=lambda d: d['smartProfitability']);

    difficultySort = sorted(filterdCoins.values(), key=lambda d: d['smartProfitability'], reverse=True);

    # print difficultySort;

    topCoin = DEFAULT_COIN;

    if (len(difficultySort) > 1):
        topCoin = difficultySort[0]

    # print topCoin['tag'];
    # print 'Current Coin: ', currentCoin['btc_revenue']
    switchingRequired = isSwitchingRequired(currentCoin=currentCoin, topCoin=topCoin)
    if (switchingRequired):
        updateCoinFile = open(MINING_COIN_PATH, 'w')
        json.dump(topCoin, updateCoinFile, indent=4, sort_keys=True)
        updateCoinFile.close()


def isSwitchingRequired(currentCoin, topCoin):
    print '#Coins: ', currentCoin['tag'], topCoin['tag']
    if (currentCoin['tag'] != topCoin['tag']):
        currentRevenue = float(currentCoin['btc_revenue'])
        topRevenue = float(topCoin['btc_revenue'])
        print '#Revenue: ', currentRevenue, topRevenue
        revenueDiff = ((topRevenue - currentRevenue) / topRevenue) * 100
        print "#Difference in Percentage", revenueDiff
        print "#Switch ", revenueDiff > PERCENTAGE_VARIED
        return revenueDiff > PERCENTAGE_VARIED
    return False

refreshTopCoin()
