import tweepy
import re
from datetime import datetime as dt

import config

class Account:
    """ Account class
    twitterアカウントのオブジェクト．
    """
    def __init__(self, account):
        """__init__
        Twitter API, アカウントの設定

        arg:
            account(string): TwitterID
        """
        #twitterAPI
        self.consumer_key = config.CONSUMER_KEY
        self.consumer_sercret = config.CONSUMER_SERCRET
        self.access_token = config.ACCESS_TOKEN
        self.access_token_sercret = config.ACCESS_TOKEN_SERCRET

        #認証
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_sercret)
        self.auth.set_access_token(self.access_token, self.access_token_sercret)
        self.api = tweepy.API(self.auth)

        #TwitterID
        self.account = account


    def getTimeline(self, count, page=1):
        """ getTimeline
        TwitterタイムラインからID，日時，テキストを取得する

        args:
            count(int): 取得するツイート数
            page(int): 取得するページ数(よくわからない．デフォルトでOKかも)
        return:
            simply_timeline(dict(dict)): ツイートIDをキーとした辞書型
                ["date"](string): ツイート日時
                ["tweet"](string): ツイート内容
                ["mentions"](list(string)): メンション相手
        """
        timeline = self.api.user_timeline(self.account, count=count, page=page)
        simply_timeline = {}

        for tweet in timeline:
            id_ = tweet.id_str
            date = tweet.created_at.strftime("%Y%m%d_%H%M%S")
            text, mentions = self._cleanseText_(tweet.text)
            simply_timeline[id_] = {"date": date,
                                    "tweet": text,
                                    "mentions": mentions}
        return simply_timeline


    def existsAccount(self):
        """  _existsAccount_
        指定されたtwitterIDのアカウントが存在するか確認する．
        """
        try:
            self.api.get_user(self, screen_name=self.account)
        except tweepy.error.TweepError:
            print(f"account Error: User {[self.account]} not exist.")
            return False
        else:
            return True
    

    def _cleanseText_(self, text):
        """ _cleanseText_
        ツイート内容の整形．メンションの取得，改行文字，URL，リツイート表記の削除

        arg:
            text(string): ツイート内容
        returns:
            text(string): 整形後のツイート内容
            mentions(list(string)): メンション相手
        """
        #メンションの取得
        mentions = re.findall(r"@\w+", text)
        #改行文字の削除
        text = str(text.replace("\n", ""))
        #リツイート表記の削除
        text = re.sub(r"RT @\w+:", "" ,text)
        #文字制限による末尾の「…」の削除
        if text[-1] == "…":
            text = text[:-1]
        #URLの削除
        text = re.sub(r"(https?|ftp)(:[\/-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+$,%#…]+)", "" ,text)
        return text, mentions


if __name__ == "__main__":
    #菅総理をサンプルにしてツイート抽出
    suga = Account("sugawitter")
    print(suga.getTimeline(10, 1))
