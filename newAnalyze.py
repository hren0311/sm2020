import pandas as pd

class NewAnalyze:
    def __init__(self):
        self.pn_dict = None
        self.sep = None
        self.encoding= None
        self.names = None

    def loadPnDict(filename="./data/pn_ja.dic"):
        """ loadPnDictionary
        単語感情極性対応表から{単語:pnスコア}のdictを返す

        arg:
        filename(string): 単語感情極性対応表のパス
        return:
        pn_dict(dict): {単語:pnスコア, ...}
        """