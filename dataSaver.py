import os
import codecs
import json
import csv
import pandas as pd
import datetime as dt

import dataManager

class DataSaver:
    def __init__(self, tweets_name, days_name, weeks_name):
        self.tweets_json = tweets_name
        self.days_json = days_name
        self.weeks_json = weeks_name

    
    def updateSubTotalJsons(self, date_score_list, data_num=7):
        sorted_pdata = self._sortDateScoreList_(date_score_list)
        self._make7tweetsJSON_(sorted_pdata, n=data_num)
        self._make7daysJSON_(sorted_pdata, n=data_num)
        self._make7weeksJSON_(sorted_pdata, n=data_num)
    

    def _make7tweetsJSON_(self, sorted_pdata, n=7):
        """ make7tweetsJSON
        直近ツイートから7ツイートのスコアを記入したjsonファイルを作成する．

        arg:
            data_score_list(list([string, float])): score_list.csvのデータ．
                                                    dataManager.date_score_listと同等．
            n(int): 隠し引数．デフォルトで7ツイートのデータ取得，nツイートに変更可能．
        """
        date_list = ["-"] * n
        score_list = [0] * n

        get_tweet_num = min(n, len(sorted_pdata))
        extract_pdata = sorted_pdata.tail(get_tweet_num)
        
        base = 0
        if n > get_tweet_num:
            base = n - get_tweet_num
        
        for i, epd in enumerate(zip(extract_pdata["date"], extract_pdata["score"])):
            date_list[i+base] = epd[0].strftime("%m/%d %H:%M")
            score_list[i+base] = epd[1]

        json_dict = {"data":score_list,"labels":date_list}

        try:
            f = codecs.open(self.tweets_json, "w", "utf-8")
        except OSError as e:
            print("json-", e)
        else:
            text = json.dumps(json_dict, indent=4, ensure_ascii=False)
            f.write(text)
            f.close()

    
    def _make7daysJSON_(self, sorted_pdata, n=7):
        """ make7daysJSON
        直近ツイートから7日分のスコアを記入したjsonファイルを作成する．

        arg:
            data_score_list(list([string, float])): score_list.csvのデータ．
                                                    dataManager.date_score_listと同等．
            n(int): 隠し引数．デフォルトで7日間のデータ取得，n日間に変更可能．
        """
        date_list = []
        score_list = []

        #今日の現在時刻までのデータ
        now_dt = dt.datetime.now() #現在日時
        today_dt = dt.datetime(now_dt.year, now_dt.month, now_dt.day) #今日の0時0分0秒
        extracted_dates = (today_dt <= sorted_pdata["date"]) & (sorted_pdata["date"] <= now_dt)
        day_sum_score = sorted_pdata[extracted_dates]["score"].sum()
        date_list.append(today_dt.strftime("%m/%d"))
        score_list.append(day_sum_score)

        #昨日以前
        day_start_dt = today_dt - dt.timedelta(days=1)
        day_end_dt = today_dt
        for i in range(n-1):
            extracted_dates = (day_start_dt <= sorted_pdata["date"]) & (sorted_pdata["date"] < day_end_dt)
            day_sum_score = sorted_pdata[extracted_dates]["score"].sum()
            date_list.append(day_start_dt.strftime("%m/%d"))
            score_list.append(day_sum_score)
            
            day_end_dt = day_start_dt
            day_start_dt = day_start_dt - dt.timedelta(days=1)

        #json用に辞書型にする
        date_list.reverse()
        score_list.reverse()
        json_dict = {"data": score_list, "labels": date_list}

        #jsonに書き込む
        try:
            f = codecs.open(self.days_json, "w", "utf-8")
        except OSError as e:
            print("make7daysJSON-", e)
        else:
            text = json.dumps(json_dict, indent=4, ensure_ascii=False)
            f.write(text)
            f.close()


    def _make7weeksJSON_(self, sorted_pdata, n=7):
        """ make7weeksJSON
        直近ツイートから7日分のスコアを記入したjsonファイルを作成する．

        arg:
            data_score_list(list([string, float])): score_list.csvのデータ．
                                                    dataManager.date_score_listと同等．
            n(int): 隠し引数．デフォルトで7日間のデータ取得，n日間に変更可能．
        """
        date_list = []
        score_list = []

        now_dt = dt.datetime.now()
        today_dt = dt.datetime(now_dt.year, now_dt.month, now_dt.day)

        #今週(6日前〜現在)の合計スコア
        week_end_dt = now_dt
        week_start_dt = today_dt - dt.timedelta(days=6)
        extract_dates = (week_start_dt <= sorted_pdata["date"]) & (sorted_pdata["date"] <= week_end_dt)
        week_sum = sorted_pdata[extract_dates]['score'].sum()
        score_list.append(week_sum)
        date_list.append(week_start_dt.strftime("%m/%d~"))

        #先週(〜7日前)の合計スコア, ...., n週前の合計スコア
        for i in range(1, n):
            week_end_dt = today_dt - dt.timedelta(days=7*i-1)
            week_start_dt = week_end_dt - dt.timedelta(days=7)
            
            extract_dates = (week_start_dt <= sorted_pdata["date"]) & (sorted_pdata["date"] <= week_end_dt)
            week_sum = sorted_pdata[extract_dates]['score'].sum()
            score_list.append(week_sum)
            date_list.append(week_start_dt.strftime("%m/%d~"))

        json_dict = {"data": score_list, "labels": date_list}
        try:
            f = codecs.open(self.weeks_json, "w", "utf-8")
        except OSError as e:
            print("json-", e)
        else:
            text = json.dumps(json_dict, indent=4, ensure_ascii=False)
            f.write(text)
            f.close()


    def _sortDateScoreList_(self, date_score_list):
        """ _sortDateScoreList_
        data_score_listを受け取って日時について昇順にソートして返す（pd.DataFrameオブジェクト）

        arg:
            date_score_list(list([string, float])): csvファイルにある全データ
        return:
            sorted_pdata(pd.DataFrame([datetime, float])): pd.DataFrameでソートした全データ
        """
        pdata = pd.DataFrame(date_score_list)
        pdata.columns = ["date", "score"]
        pdata["date"] = pd.to_datetime(pdata["date"], format="%Y%m%d_%H%M%S")
        sorted_pdata = pdata.sort_values("date")
        return sorted_pdata


if __name__ == "__main__":
    csv_name = "./data/score_list.csv"
    tweets_name = "./data/seven_tweets_scores.json"
    days_name = "./data/seven_days_scores.json"
    weeks_name= "./data/seven_weeks_scores.json"

    import dataManager
    dm = dataManager.DataManager()
    dm.setCSV(csv_name)
    dm.loadCSV()
    date_score_list = dm.getCSV()


    ds = DataSaver(tweets_name, days_name, weeks_name)
    ds.updateSubTotalJsons(date_score_list, data_num=7)
