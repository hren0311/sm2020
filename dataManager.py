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
        self.date_score_list = None #変更点


    def setJSON(self, json_name):
        """ setJSON
        jsonファイル名をメンバ変数に格納

        arg:
            json_name(string): jsonファイル名
        """
        self.json_name = json_name


    def setCSV(self, csv_name):
        """ setCSV
        csvファイル名をメンバ変数に格納

        arg:
            csv_name(string): csvファイル名
        """
        self.csv_name = csv_name
    
    def getCSV(self):
        """ getCSV
        csvファイルの内容を返す．

        return:
            self.data_score_list(list([string, float]): csvファイルにある全データ
        """
        return self.date_score_list


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

    #変更点 csvを行ごとに読み込む，Noneの場合,空のリストを作成
    #ファイルが存在しない場合，空のファイルを作成
    def loadCSV(self):
        """ loadCsv
        csvを読み込み，書き込まれたデータ全てを返す．
        csvファイルが存在しない場合は，ファイルを作成する．
        """
        if os.path.exists(self.csv_name):
            with open(self.csv_name, "r") as f:
                reader = csv.reader(f)
                self.date_score_list = [[row[0], float(row[1])] for row in reader]
            if self.date_score_list is None:
                self.date_score_list = []
        else:
            try:
                f = open(self.csv_name, "w")
            except OSError as e:
                print("csv-", e)
            else:
                f.close()
                self.date_score_list = []
    

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
    
    #変更点 ツイート時間，スコアを1行ごとに追加
    def _updateCSV_(self, new_date, new_score):
        """ _updateCSV_
        既存のcsvファイルに1ツイート分のツイート日時，pnスコアを追加
        
        args:
            new_date(string): ツイート日時
            new_score(float): pnスコア
        """
        self.date_score_list.append([new_date,new_score])
        try:
            f = open(self.csv_name, "a", newline="")
        except OSError as e:
            print("csv-", e)
        else:
            writer = csv.writer(f)
            writer.writerow([new_date, new_score])
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

    tmp = {"123456789": {
                "date": "20201031_141923",
                "tweet": "hello, world",
                "mentions": ["sugawara", "abe"],
                "score": 1.0,
                "sum_score": 124.23587532,
                "high_score_words": ["happy", "friends", "omoroi"]
                }
          }
    tmp2 = {"123456922": {
        "date": "20201031_141931",
        "tweet": "hello, world2",
        "mentions": ["sugawara2", "abe2"],
        "score": 2.0,
        "sum_score": 12.2,
        "high_score_words": ["hap", "hey", "suki"]
        }
    }
    dm.updateDatabase(tmp)
    dm.updateDatabase(tmp2)
    print(dm.date_score_list)
