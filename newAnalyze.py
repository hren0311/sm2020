import pandas as pd
import MeCab
import account 

class NewAnalyze:

    def __init__(self):
        #コンストラクタ
        self.pn_dict = None
        self.tagger = None

    def loadSetting(self, filename="./data/pn_ja.dic"):
        """ loadSetting

        arg:
           filename(string):辞書ファイルのパス
        形態素解析モジュールを設定
        {単語:pnスコア}のdictを読み込む
        """
        self.tagger = MeCab.Tagger("")
        self._loadPnDict_(filename)


    def _loadPnDict_(self, filename="./data/pn_ja.dic"):
        """ _loadPnDict_
        単語感情極性対応表から{単語:pnスコア}のdictをself.pn_dictに保存

        arg:
            filename(string): 単語感情極性対応表のパス

        """
        pnja = pd.read_csv(filename,
                        sep=":",
                        encoding="shift-jis",
                        names=("Word", "Read", "Hinshi", "Score"))
        self.pn_dict = dict(zip(pnja["Word"], pnja["Score"]))



    def _morphologicalAnalyze_(self, text):
        """morphologicalAnalyze
        形態素解析関数

        args:
            text(string): 解析する文章
        return:
            morpheme_list(list(string)): 分解した形態素のリスト
        """
        if self.tagger is None:
            print("please run self.loadSetting()")
            return []

        #形態素解析
        morphemes = self.tagger.parse(str(text))
        morphemes = morphemes.splitlines()

        morpheme_list = []
        
        for morpheme in morphemes:
            splited_morpheme = morpheme.split("\t")
            morpheme_list.append(splited_morpheme[0])

        return morpheme_list


    def textToPnScore(self, text):
        """ textToPnScore
        1文章のPNを計算．（加算）

        args:
            text(string): tweet
        return:
            score(float): pnスコア
        """
        score = 0
        morpheme_list = self._morphologicalAnalyze_(text)
        for morpheme in morpheme_list:
            if self.pn_dict.get(morpheme) is not None:
                score += self.pn_dict[morpheme]

        return score


def main():
    suga = account.Account("yousuck2020")
    ana = NewAnalyze()
    ana.loadSetting()
    for id_, timeline in suga.getTimeline(10, 1).items():
        print("id", id_,end=" : ")

        text=timeline["tweet"]
        
        score = ana.textToPnScore(text)
        print(score)

main()