import os
import csv
import datetime as dt
import pandas as pd
import json

import dataManager

def nDaysAgo(today_str, n):
    """ nDaysAgo
    文字列"yyyymmdd_hhmmss"からn日前の"yymmdd"を返す．

    args:
        today_str(string): 日時を表す文字列．yyyymmdd_hhmmss．
        n(int): n日前のn
    return:
        n_days_ago_str(string): n日前の日時を表す文字列．yyyymmdd．
    """
    today_datetime = datetime.datetime.strptime(today_str, '%Y%m%d_%H%M%S')
    n_days_ago_datetime = today_datetime - datetime.timedelta(days=n)
    n_days_ago_str = n_days_ago_datetime.strftime('%Y%m%d')
    return n_days_ago_str


def make7daysJSON(date_score_list, n=7):
    """ make7daysJSON
    直近ツイートから7日分のスコアを記入したjsonファイルを作成する．

    arg:
        data_score_list(list([string, float])): score_list.csvのデータ．
                                                dataManager.date_score_listと同等．
        n(int): 隠し引数．デフォルトで7日間のデータ取得，n日間に変更可能．
    """
    dates = []
    sum_scores = []

    #pandasのDataFrameで扱う
    pdata = pd.DataFrame(date_score_list)
    pdata.columns = ["date", "score"]
    pdata["date"] = pd.to_datetime(pdata["date"], format="%Y%m%d_%H%M%S")

    #日時に対して昇順にソート
    pdata = pdata.sort_values("date")

    #今日の現在時刻までのデータ
    now_dt = dt.datetime.now() #現在日時
    today_dt = dt.datetime(now_dt.year, now_dt.month, now_dt.day) #今日の0時0分0秒
    extracted_dates = (today_dt <= pdata["date"]) & (pdata["date"] <= now_dt)
    day_sum_score = pdata[extracted_dates]["score"].sum()
    dates.append(today_dt.strftime("%m/%d"))
    sum_scores.append(day_sum_score)

    #昨日以前
    day_start_dt = today_dt - dt.timedelta(days=1)
    day_end_dt = today_dt
    for i in range(n-1):
        extracted_dates = (day_start_dt <= pdata["date"]) & (pdata["date"] < day_end_dt)
        day_sum_score = pdata[extracted_dates]["score"].sum()
        dates.append(day_start_dt.strftime("%m/%d"))
        sum_scores.append(day_sum_score)
        
        day_end_dt = day_start_dt
        day_start_dt = day_start_dt - dt.timedelta(days=1)

    #json用に辞書型にする
    dates.reverse()
    sum_scores.reverse()
    json_data = {"data": sum_scores, "labels": dates}

    #jsonに書き込む
    try:
        f = open(json_name, "w")
    except OSError as e:
        print("make7daysJSON-", e)
    else:
        text = json.dumps(json_data, indent=4, ensure_ascii=False)
        f.write(text)
        f.close()



if __name__ == "__main__":
    csv_name = "./data/score_list.csv"
    json_name = "./data/seven_days_scores.json"
    dm = dataManager.DataManager()
    dm.setCSV(csv_name)
    dm.loadCSV()
    date_score_list = dm.getCSV()

    make7daysJSON(date_score_list)
