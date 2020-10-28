import pandas as pd
import MeCab
import account 

class Analyzer:

    def __init__(self):
        #コンストラクタ
        self.pn_dict = None
        self.tagger = MeCab.Tagger()


    def loadPnDict(self, filename="./data/pn_ja.dic"):
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
                word_pn_score = self.pn_dict[morpheme]

                if word_pn_score < 0:
                    word_pn_score = word_pn_score * 0.2
                else:
                    word_pn_score = word_pn_score * 1
                
                score += word_pn_score

        return score


def main():
    import sys

    user = account.Account(sys.argv[1])
    ana = Analyzer()
    ana.loadSetting()
    for id_, timeline in user.getTimeline(100, 1).items():
        text=timeline["tweet"]
        print("tweet:\n", text)
        score = ana.textToPnScore(text)
        print("score:", score)


if __name__ == "__main__":
    main()