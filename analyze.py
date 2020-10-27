#codnig:utf-8

import pandas as pd
import MeCab
import tweepy
import re
import time

import account
import dataManager

def loadPnDictionary(filename):
    """ loadPnDictionary
    単語感情極性対応表から{単語:pnスコア}のdictを返す
    
    arg:
        filename(string): 単語感情極性対応表のパス
    return:
        pn_dict(dict): {単語:pnスコア, ...}
    """
    pnja = pd.read_csv(filename,
                       sep=":",
                       encoding="shift-jis",
                       names=("Word", "Read", "Hinshi", "Score"))
    pn_dict = dict(zip(pnja["Word"], pnja["Score"]))
    return pn_dict


def morphological_analyze(text, rt=False):
    """morphological_analyze
    形態素解析関数

    args:
        text(string): 解析する文章
        rt(boolean): RTも解析するか．Trueで解析
    return:
        morpheme_list(list(string)): 分解した形態素のリスト
    """
    #形態素解析モジュール(?)
    tagger = MeCab.Tagger("")

    #形態素解析
    morphemes = tagger.parse(str(text))
    morphemes = morphemes.splitlines() #文字列のリスト
 
    #rt==FalseならRTは除いて表示
    morpheme_list = []
    if not (not rt and morphemes[0][:2] == "RT"):
        for morpheme in morphemes:
            splited_morpheme = morpheme.split("\t")
            morpheme_list.append(splited_morpheme[0])
            #print(splited_morpheme)
        #print(morpheme_list)

    return morpheme_list


def pnScore(pn_dict, morpheme_list):
    """ pnScore
    1文章のPNを計算．（加算）

    args:
        pn_dict(dict): 単語感情極性対応辞書
        morpheme_list(string): 形態素のリスト
    return:
        score(float): pnスコア
    """
    score = 0
    for morpheme in morpheme_list:
        if pn_dict.get(morpheme) is not None:
            score += pn_dict[morpheme]
            #print(f"{morpheme} : {pn_dict[morpheme]}")
        else:
            #print(f"{morpheme} : not in pn_dict")
            pass
    
    return score
 

def main():
    #単語感情極性対応表
    filename = "./data/pn_ja.dic"
    pn_dict = loadPnDictionary(filename)

    #dataManager
    json_name = "./data/data.json"
    csv_name = "./data/score_list.csv"
    dm = dataManager.DataManager()
    dm.setJSON(json_name)
    dm.setCSV(csv_name)
    dm.loadJSON()
    dm.loadCSV()
    pre_sum_score = 0
    i = 1
    
    suga = account.Account("yousuck2020")
    for id_, timeline in suga.getTimeline(200, 1).items():
        print("tweet:", i)
        i += 1

        #print("id: ", id_)
        #print("timeline: ", timeline)
        text = timeline["tweet"]
        #print("tweet:\n", text, "\n")
        
        morpheme_list = morphological_analyze(text)
        score = pnScore(pn_dict, morpheme_list)
        #print("PN score: ", score)

        data = {id_: {
                      "date": timeline["date"],
                      "tweet": timeline["tweet"],
                      "mentions": timeline["mentions"],
                      "score": score,
                      "sum_score": score + pre_sum_score,
                      "high_score_words": []
                }}
        pre_sum_score += score
        dm.updateDatabase(data)
        time.sleep(0.5)






if __name__ == "__main__":
    main()
