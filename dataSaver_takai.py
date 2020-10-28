import os
import codecs
import json
import csv
import dataManager
import pandas as pd
import datetime as dt

def make7weeksJSON(date_score_list):
	"""make7weeksJSON
    各週のスコアの合計をJSON形式で出力

    args:
        self.data_score_list(list([string, float]): csvファイルにある全データ
    return:
        
    """
	week_sum_list = []
	week_labels_list = []
	week_range_list = []

	pdata = pd.DataFrame(date_score_list)
	pdata.columns = ["date", "score"]
	pdata["date"] = pd.to_datetime(pdata["date"], format="%Y%m%d_%H%M%S")
	print(pdata)

	pdata = pdata.sort_values("date")

	d = dt.datetime.now()
	today_dt = d - dt.timedelta(hours=d.hour, minutes=d.minute, seconds=d.second, microseconds=d.microsecond)

	#"""
	#今週(6日前〜現在)の合計スコア

	end_dt = d
	start_dt = today_dt - dt.timedelta(days=6)

	extract_dates = (pdata["date"] <= end_dt) & (pdata["date"] >= start_dt)
	print(start_dt, end_dt)
	print(pdata[extract_dates]['score'])
	week_sum = pdata[extract_dates]['score'].sum()
	#print(start_dt, "<= score <=", end_dt, float(week_sum))

	start_str = start_dt.strftime('%Y/%m/%d %H:%M')
	end_str = end_dt.strftime('%Y/%m/%d %H:%M')

	
	week_sum_list.append(float(week_sum))
	week_range_list.append(start_str + " 〜 " + end_str)
	
	#先週(〜7日前)の合計スコア, ...., 7週前の合計スコア

	for n in range(1, 7):
		end_dt = today_dt - dt.timedelta(days=7*n-1)
		start_dt = today_dt - dt.timedelta(days=7*(n+1)-1)
		extract_dates = (pdata["date"] < end_dt) & (pdata["date"] >= start_dt)
		print(start_dt, end_dt)
		print(pdata[extract_dates]['score'])
		week_sum = pdata[extract_dates]['score'].sum()

		start_str = start_dt.strftime('%Y/%m/%d %H:%M')
		end_str = end_dt.strftime('%Y/%m/%d %H:%M')
		#print(start_dt, "<= score <", end_dt, float(week_sum))
		week_sum_list.append(float(week_sum))
		week_range_list.append(start_str + " 〜 " + end_str)

	json_data = {"graphData" : {
	                  "data": week_sum_list,
	                  "labels":week_range_list
	            }}
	print(json_data)
	try:
		f = codecs.open(json_name, "w", "utf-8")
	except OSError as e:
		print("json-", e)
	else:
		text = json.dumps(json_data, indent=4, ensure_ascii=False)
		f.write(text)
		f.close()
	#"""
	"""
	(7日前の現在時刻〜現在時刻)での合計スコア
	for n in range(0, 6):
		end_dt = d - dt.timedelta(days=7*n)
		start_dt = d - dt.timedelta(days=7*(n+1))
		extract_dates = (pdata["date"] <= end_dt) & (pdata["date"] > start_dt)
		week_sum = pdata[extract_dates]['score'].sum()

		print(start_dt, "<= score <=", end_dt, float(week_sum))
	"""
def calc_a_week_sum(start_dt, end_dt):
	pass
	


if __name__ == "__main__":
	csv_name = "/Users/takairyouma/Downloads/sm2020-main/data/score_list.csv"
	json_name = "/Users/takairyouma/Downloads/sm2020-main/data/week_data.json"
	dm = dataManager.DataManager()
	dm.setCSV(csv_name)
	dm.loadCSV()
	date_score_list = dm.getCSV()
	#print(date_score_list)
	make7weeksJSON(date_score_list)
	

