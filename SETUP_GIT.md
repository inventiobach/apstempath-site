@'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# 仮想環境 (venv)
.venv/
venv/
ENV/
env/

# VS Code / エディタ設定
.vscode/
.idea/

# 学習データ・ログ・モデル重みファイル
*.log
*.pt
*.pth
*.bin
checkpoints/
data/
corpus/

# OS固有ファイル
.DS_Store
Thumbs.db
'@ | Out-File -Encoding utf8 .gitignore



---

github：git@github-usuninav
アカウント：inventiobach
リポジトリ：apstempath-site
です。


ssh -T git@github-usuninav

git init
git remote add origin git@github-usuninav:inventiobach/apstempath-site.git

git add .

git status

git commit -m "Reorganize project structure"

git branch -M main
git push -u origin main --force

---

日常業務

# 1. 作業開始前：リモートの最新状態を取り込む（習慣化）
git pull origin main

# 2. ファイル編集後：変更点を確認
git status

# 3. 変更をステージング
git add .

# 4. コミット（わかりやすいメッセージ）
git commit -m "post to x"

# 5. リモートへ送信
git push origin main