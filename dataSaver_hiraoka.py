import csv
import dataManager
from datetime import datetime as dt
import json
import codecs



def make7tweetsJSON(data_score_list):
    seven_date_list = []
    seven_score_list = []
    if(len(data_score_list)>=7):
        data=data_score_list[:7]
        data_num = 7
    else:
        data=data_score_list
        data_num = len(data)
        nodata_num = 7 - data_num
        seven_date_list = ["-" for i in range(nodata_num)]
        seven_score_list = [0 for i in range(nodata_num)]

        for i in range(data_num):
            date,score = data[i]
            seven_date_list.append(changeDateStr(date))
            seven_score_list.append(score)


    json_name = "./data/seven_tweets.json"
    json_dict = {"data":seven_score_list,"labels":seven_date_list}

    try:
        f = codecs.open(json_name, "w", "utf-8")
    except OSError as e:
        print("json-", e)
    else:
        text = json.dumps(json_dict, indent=2, ensure_ascii=False)
        f.write(text)
        f.close()
     
def changeDateStr(date_str):
    tdatetime = dt.strptime(date_str, '%Y%m%d_%H%M%S')
    tstr = tdatetime.strftime('%m/%d %H:%M')
    return tstr




def main():
    csv_name="./data/score_list.csv"
    dm = dataManager.DataManager()
    dm.setCSV(csv_name)
    dm.loadCSV()
    #data_score_list = dm.getCSV()
    data_score_list = [['20200827_085910', -1.7951849000000002], ['20200827_093518', -6.915457], ['20200827_225529', -4.783546]]
    make7tweetsJSON(data_score_list)
    
    

main()