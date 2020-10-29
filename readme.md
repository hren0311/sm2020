# 信州未来アプリコンテスト0 2020

### monitor.py  
メインプログラム  
フロント部からtwitterID，迷いの設定を受け取り，twitterの監視，データの保存，フロントに向けたファイルの生成を行う．

### account.py  
twitter API 用クラス  

### dataManager.py  
データベース管理用クラス  

### dataSaver.py
フロントに向けたファイル生成用クラス

### analyzer.py
ツイートを受け，感情・決意分析を行う解析用クラス
