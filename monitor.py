import os
import time
import codecs

import account
import dataManager
import dataSaver
import analyzer

def waitSetting(setting_name):
    """ waitsetting
    設定が完了するまで待つ．

    arg:
        setting_name(string): 設定ファイル名
    """
    def getSetting(setting_name):
        account_id = ""
        goal = ""
        with codecs.open(setting_name, "r", "utf-8") as f:
            goal, account_id = f.readline().split(",")
        if account_id == "" or goal == "":
            print("Setting Error: Account ID or Goal are not set.")
        return account_id, goal

    while True:
        print("waiting setting file created.....")
        time.sleep(1)

        if os.path.exists(setting_name):
            account_id, goal = getSetting(setting_name)
            tmp_user = account.Account(account_id)
            if tmp_user.existsAccount():
                break
            else:
                os.remove(setting_name)
                time.sleep(2)

    print("setting completed.")
    return account_id, goal
    
    
def removeFiles(file_names):
    """ removeFiles
    データファイル，setting.txtを消去する．
    （別ユーザのデータが追記されないように）

    arg:
        file_names(list(string)): 消したいファイルのリスト
    """
    for file_name in file_names:
        if os.path.exists(file_name):
            os.remove(file_name)


def main():
    #各種ファイル名
    data_dir = "./data/"
    json_name = data_dir + "data.json"
    csv_name = data_dir + "score_list.csv"
    tweet7_json = data_dir + "tweet7.json"
    day7_json = data_dir + "day7.json"
    week7_json = data_dir + "week7.json"
    pn_dict = data_dir + "pn_ja.dic"
    setting_name = data_dir + "setting.txt"
    sum_score_file_name = data_dir + "sum_score.txt"

    #変数
    prev_tweet_num = 10
    get_tweet_num_by_time = 3
    sum_score = 0


    #データ関係のファイルを消去
    remove_file_names = [json_name, csv_name, setting_name,
                         tweet7_json, day7_json, week7_json]
    removeFiles(remove_file_names)


    #フロント側の設定完了を待つ
    account_id, goal = waitSetting(setting_name)

    #各種オブジェクトを生成，初期設定
    #account オブジェクト
    user = account.Account(account_id)
    
    #dataManager オブジェクト
    dm = dataManager.DataManager()
    dm.setJson(json_name)
    dm.loadJson()
    dm.setCsv(csv_name)
    dm.loadCsv()

    #dataSaverオブジェクト
    ds = dataSaver.DataSaver(tweet7_json, day7_json, week7_json)

    #analyzer オブジェクト
    anlzr = analyzer.Analyzer()
    anlzr.loadPnDict(pn_dict)


    #監視の前にデータを取得しておく
    for tweet_id, tweet_info in user.getTimeline(prev_tweet_num, 1).items():
        date = tweet_info["date"]
        tweet_text = tweet_info["tweet"]
        mentions = tweet_info["mentions"]

        score = anlzr.pnDictScore(tweet_text)
        score = anlzr.gcnlScore(tweet_text)
        
        sum_score += score
        high_score_words = []

        json_dict = {tweet_id: {
                        "date": date,
                        "tweet": tweet_text,
                        "mentions": mentions,
                        "score": score,
                        "sum_score": sum_score,
                        "high_score_words": high_score_words
                        }
                    }
        dm.updateDatabase(json_dict)
    
    date_score_list = dm.getCsv()
    ds.updateSubTotalJsons(date_score_list)
    ds.sendSumScore(sum_score_file_name, sum_score)


    while True:
        print("monitoring timeline...")
        time.sleep(10)
        for tweet_id, tweet_info in user.getTimeline(get_tweet_num_by_time, 1).items():
            date = tweet_info["date"]
            tweet_text = tweet_info["tweet"]
            mentions = tweet_info["mentions"]

            if dm.hasData(tweet_id):
                continue

            score = anlzr.pnDictScore(tweet_text)
            score = anlzr.gcnlScore(tweet_text)

            sum_score += score
            high_score_words = []

            json_dict = {tweet_id: {
                            "date": date,
                            "tweet": tweet_text,
                            "mentions": mentions,
                            "score": score,
                            "sum_score": sum_score,
                            "high_score_words": high_score_words
                            }
                        }
            dm.updateDatabase(json_dict)
        
        date_score_list = dm.getCsv()
        ds.updateSubTotalJsons(date_score_list)
        ds.sendSumScore(sum_score_file_name, sum_score)



if __name__ == "__main__":
    main()
