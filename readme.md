# Shinshu Mirai App-contest 2020

### 大元の変更をローカルに反映
git pull origin main

作業

### 変更を登録
git add <変更したファイル>

### 変更をコミット
git commit -m "変更情報コメント"

### 変更をプッシュ
git push origin main

### プルリクエストをする
githubのwebページに行って，緑の"pull request"ボタンを押す．
コメントを書いて送信，

### プルリクを承認
管理人がプルリクを承認することで，大元に変更が反映される，

### ローカルに変更情報を取り込む
git fetch true_origin

### ローカルのブランチに移動し，変更を反映させる
git checkout main  
git pull true_origin main

### 最新になったローカルの main ブランチの内容を リモートの origin の main にも反映しておく
git push origin main
