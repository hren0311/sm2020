#-*- coding: utf-8 -*-

import os
import codecs
import json
import csv


class DataManager():
    """ DataManager class
    jsonファイル，csvファイルを扱う責任を持つ．
    """
    def __init__(self):
        """ コンストラクタ
        """
        self.json_name = None
        self.csv_name = None
        self.json_data = None
        self.date_list = None
        self.score_list = None


    def setJSON(self, json_name):
        """ setJSON
        jsonファイル名をメンバ変数に格納

        arg:
            json_name(string): jsonファイル名
        """
        self.json_name = json_name


    def setCSV(self, csv_name):
        """ setcsv
        csvファイル名をメンバ変数に格納

        arg:
            csv_name(string): csvファイル名
        """
        self.csv_name = csv_name


    def loadJSON(self):
        """ loadJSON
        JSONを読み込み，書き込まれたデータ全てを返す．
        JSONファイルが存在しない場合は，初期データを入れてファイルを作成する．
        """
        if os.path.exists(self.json_name):
            json_data = {}
            with codecs.open(self.json_name, "r", "utf-8") as f:
                json_data = json.load(f)
            #print("json:", json_data)
            self.json_data = json_data
        else:
            try:
                f = codecs.open(self.json_name, "w", "utf-8")
            except OSError as e:
                print("json-", e)
            else:
                initial_data = {"0000000000000000000":
                                    {"date": "00000000_000000",
                                     "tweet": "",
                                     "mentions": [],
                                     "score": 0,
                                     "sum_score": 0,
                                     "high_score_words": []
                                    }
                                }
                text = json.dumps(initial_data, indent=4, ensure_ascii=False)
                f.write(text)
                f.close()
                self.json_data = initial_data


    def loadCSV(self):
        """ loadCsv
        csvを読み込み，書き込まれたデータ全てを返す．
        csvファイルが存在しない場合は，空2行書き込んでファイルを作成する．
        """
        if os.path.exists(self.csv_name):
            date_list = []
            score_list = []
            with open(csv_name, "r") as f:
                date_list = f.readline()
                score_list = f.readline()
                if len(score_list) != 0:
                    date_list = date_list.replace("\n", "").split(",")
                    score_list = list(map(float, score_list.split(",")))
            self.date_list = date_list
            self.score_list = score_list
        else:
            try:
                f = open(self.csv_name, "w")
            except OSError as e:
                print("csv-", e)
            else:
                f.write("\n")
                f.close()
                self.date_list = []
                self.score_list = []
    

    def updateDatabase(self, new_data_dict):
        """ updateDatabase
        既存のjson, csvファイルに1ツイート分の情報を追加．
        すでに登録済みのデータは書き込まない．

        arg:
            new_data_dict(dict): 新規データ．ツイートIDをキー，その他ツイート情報を値に持つ．
                ["date"](string): ツイートした日時(yyyymmdd_hhmmss)
                ["tweet"](string): ツイート内容
                ["mentions"](list(string)): メンション相手
                ["score"](float): pnスコア
                ["sum_score"](float): 累積pnスコア
                ["high_score_words"](list(string)): 絶対値でスコアの高かった単語3つ（仮）
        """
        if len(new_data_dict) != 1:
            print("updateJSON error: arg \"new_data_dict\" must be 1 item.")
        #for分だけどnew_tweet_idとnwe_tweet_infoは1つだけ
        for key, val in new_data_dict.items():
            new_id = key
            new_info = val
        new_date = new_info["date"]
        new_score = new_info["score"]

        if new_id not in self.json_data:
            self._updateJSON_(new_id, new_info)
            self._updateCSV_(new_date, new_score)


    def _updateJSON_(self, new_id, new_info):
        """ _updateJSON_
        既存のjsonファイルに1ツイート分の情報を追加

        args:
            new_id(string): ツイートID
            new_info(dict): その他ツイート情報
        """
        self.json_data[new_id] = new_info
        try:
            f = codecs.open(self.json_name, "w", "utf-8")
        except OSError as e:
            print("json-", e)
        else:
            text = json.dumps(self.json_data, indent=4, ensure_ascii=False)
            f.write(text)
            f.close()
    

    def _updateCSV_(self, new_date, new_score):
        """ _updateCSV_
        既存のcsvファイルに1ツイート分のツイート日時，pnスコアを追加
        
        args:
            new_date(string): ツイート日時
            new_score(float): pnスコア
        """
        if type(self.date_list) is str:
            #文字列型のときは何もデータがない状態なので，空リストにしておく．
            self.date_list = []
            self.score_list = []
        self.date_list.append(new_date)
        self.score_list.append(new_score)
        try:
            f = open(self.csv_name, "w", newline="")
        except OSError as e:
            print("csv-", e)
        else:
            writer = csv.writer(f)
            writer.writerow(self.date_list)
            writer.writerow(self.score_list)
            f.close()
    
    def getScoreByTime(self, from_, to, mode="day"):
        """ getScoreByTime
        日時を指定して，その期間のスコアを抽出．

        args:
            from_(string): 期間のスタート日時．yyyymmdd_hhmmss
            to(string): 期間の終了日時．yyyymmdd_hhmmss
            mode(string): 日にちでの期間か，時刻での期間かのモード分け．
                        "day": 日にち
                        "time": 時刻
        """
        pass



if __name__ == "__main__":
    json_name = "./data/data.json"
    csv_name = "./data/score_list.csv"
    
    dm = DataManager()
    dm.setJSON(json_name)
    dm.setCSV(csv_name)
    dm.loadJSON()
    dm.loadCSV()
    print(dm.date_list, dm.score_list)

    tmp = {"123456789": {
                "date": "20201031_141923",
                "tweet": "hello, world",
                "mentions": ["sugawara", "abe"],
                "score": 1.0,
                "sum_score": 124.23587532,
                "high_score_words": ["happy", "friends", "omoroi"]
                }
          }
    dm.updateDatabase(tmp)
    print(dm.date_list, dm.score_list)
