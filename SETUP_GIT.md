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

git status
git add .
git commit -m "変更内容を一言で(例: About page修正)"
git push