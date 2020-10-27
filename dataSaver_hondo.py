import os
import csv
import datetime

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


def make7daysJSON(date_score_list):
    """ make7daysJSON
    直近ツイートから7日分のスコアを記入したjsonファイルを作成する．

    arg:
        data_score_list(list([string, float])): score_list.csvのデータ．
                                                dataManager.date_score_listと同等．
    """
    #日時の降順に並び変える(一時的)
    date_score_list.reverse()

    #直近ツイートの日時を取得
    latest = date_score_list[-1][0]
    
    #直近ツイートから7日間のスコアの日計
    week_scores = {}
    for day in range(7):
        week_scores[nDaysAgo(latest, day)] = 0
    over_week_day = nDaysAgo(latest, 7) #7日前=直近ツイート日から7日間が過ぎた日 yyyymmdd

    #日時の昇順に並び替え
    date_score_list.reverse()
    for date, score in date_score_list:
        only_date = date.split("_")[0] #yyyymmdd
        #昇順を想定しているため，7日前以下の日時になった時点で終了
        if int(only_date) <= int(over_week_day):
            break
        week_scores[only_date] += score
    
    #日時表記を変換してjsonファイル書き込み
        

    

if __name__ == "__main__":
    csv_name = "./data/score_list.csv"
    dm = dataManager.DataManager()
    dm.setCSV(csv_name)
    dm.loadCSV()
    date_score_list = dm.getCSV()

    print(make7daysJSON(date_score_list))