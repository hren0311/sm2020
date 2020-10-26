import tweepy
import re
import config
from datetime import datetime as dt

class Account:
	def __init__(self, account):
		self.consumer_key = config.CONSUMER_KEY
		self.consumer_sercret = config.CONSUMER_SERCRET
		self.access_token = config.ACCESS_TOKEN
		self.access_token_sercret = config.ACCESS_TOKEN_SERCRET

		self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_sercret)
		self.auth.set_access_token(self.access_token, self.access_token_sercret)
		self.api = tweepy.API(self.auth)

		self.acount = account

	def getTimeline(self, count, page=1):
		""" getTimeline

		arg:
			count(int): 
			page(int): 
		return:
			simply_timeline(list(tuple(string, string, string)): 
		"""
		timeline = self.api.user_timeline(self.acount, count=count, page=page)
		ids, dates, texts = [], [], []

		for tweet in timeline:
			ids.append(tweet.id_str)
			date = self._datetime2ymdhms_(tweet.created_at)
			dates.append(date)
			text = self._cleanseText_(tweet.text)
			texts.append(text)
		simply_timeline = [(id_, date, text) for id_, date, text in zip(ids, dates, texts)]
		return simply_timeline

	def _datetime2ymdhms_(self, date):
		""" _datetime2ymdhms_

		arg:
			date(datetime):  
		return:
			datetime_str(string): 
		"""
		datetime_str = date.strftime('%Y%m%d_%H%M%S')
		return datetime_str

	def _cleanseText_(self, text):
		""" _cleanseText_

		arg:
			text(string): 
		return:

		"""
		mentions = re.findall(r"@\w+", text)
		print(mentions)
		text = str(text.replace("\n", "")) #改行を削除
		text = re.sub(r"(https?|ftp)(:[\/-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+$,%#…]+)", "" ,text)
		text = re.sub(r"RT @\w+:", "" ,text)
		if text[-1] == "…":
			text = text[:-1]
		return text



    

suga = Account("sugawitter")
print(suga.getTimeline(10, 1))
#s = "ierjoifhrofrjffelsfh…"
#print(s[:-1])
#print(suga.auth)
#print(a1.auth, a1.consumer_sercret, a1.access_token, a1.access_token_sercret)

