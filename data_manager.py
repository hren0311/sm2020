#-*- coding: utf-8 -*-

import os
import codecs
import json
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
import random

def loadJSON(json_name):
    """ loadJSON
    JSONを読み込む．

    arg:
        json_name(string): JSONファイル名
    return:
        json_data(list(jsondict)): 読み込んだデータ
    """
    if os.path.exists(json_name):
        json_data = []
        with codecs.open(json_name, "r", "utf-8") as f:
            json_data = json.load(f)
        #print("json:", json_data)
        return json_data
    else:
        return []


def loadCSV(csv_name):
    """ loadCsv
    csvを読み込む．

    arg:
        csv_name(string): csvファイル名
    return:
        score_list(list(float)): pnスコアのリスト
    """
    score_list = []
    with open(csv_name, "r") as f:
        score_list = f.readline()
        if len(score_list) != 0:
            score_list = list(map(float, score_list.split(",")))
    return score_list


def appendData(json_name, csv_name, data_dict):
    """ appendData
    jsonとcsvにデータを追記する．
    json dump時に文字コードに注意．

    args:
        json_name(string): jsonファイル名
        csv_name(string): csvファイル名
        data_dict(OrderedDict): json書き込み用データ
            ["ID"](string): tweetID
            ["date"](string): ツイートした日時(yyyymmdd_hhmmss)
            ["tweet"](string): ツイート内容
            ["mentions"](list(string)): メンション相手
            ["score"](float): pnスコア
            ["sum_score"](float): 累積pnスコア
            ["high_score_words"](list(string)): 絶対値でスコアの高かった単語3つ（仮）
    """
    #csv用にscoreだけ抽出
    score = data_dict["score"]
    
    #jsonは一度データを読み取ってから追記
    json_data = loadJSON(json_name)
    json_data.append(data_dict)

    #json書き込み
    try:
        json_f = codecs.open(json_name, "w", "utf-8")
    except OSError as e:
        print("json-", e)
    else:
        text = json.dumps(json_data, indent=4, ensure_ascii=False)
        json_f.write(text)
        json_f.close()

    #csv書き込み
    try:
        csv_f = open(csv_name, "a")
    except OSError as e:
        print("csv-", e)
    else:
        csv_f.write(","+str(score))
        csv_f.close() 


def makeScoreListCSV(csv_name):
    """ makeScoreListCSV
    csvファイルがないときに，初期値0を入れて作成．

    arg:
        csv_name(string): csvファイル名
    """
    if not os.path.exists(csv_name):
        with open(csv_name, "w") as f:
            f.write("0")


def plotDecision(data):
    """ plotDecision
    第六感グラフを作成，プロット

    arg:
        data(list(float)): 第六感値の遍歴
    """
    x = np.linspace(0, 10, len(data))
    plt.plot(x, data, label="decision")
    plt.legend()
    plt.show()


def main():
    data_file_name = "./data/pn_data.dat"
    json_name = "./data/data.json"
    csv_name = "./data/score_list.csv"

    #ファイル存在チェック おいておく
    makeScoreListCSV(csv_name)

    json_data = loadJSON(json_name)
    score_list = loadCSV(csv_name)

    #plotDecision(score_list)

    #print(json_data[0]["tweet"])
    #print(type(json_data[0]["tweet"]))

    tmp_data = OrderedDict({"ID": "89384573879258723",
                            "date": "20301023_235959",
                            "tweet": "やったーーー！!!!!！！！！",
                            "mentions": ["@sgawitter", "@hikakin"],
                            "score": 999,
                            "sum_score": 9999999,
                            "high_score_words": ["たかい", "is", "sad"]
                            })
    appendData(json_name, csv_name, tmp_data)



if __name__ == "__main__":
    main()
