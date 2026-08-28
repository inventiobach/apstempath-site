import os
import json
from datetime import datetime, timezone, timedelta
import tweepy

POSTS_FILE = os.path.join(os.path.dirname(__file__), "posts.json")

def load_posts():
    if not os.path.exists(POSTS_FILE):
        print("posts.json not found.")
        return []
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_posts(posts):
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

def post_next():
    posts = load_posts()
    
    # 未投稿のポストを1件探索
    target_post = None
    for post in posts:
        if not post.get("posted", False):
            target_post = post
            break

    if not target_post:
        print("No pending posts left in queue.")
        return

    text = target_post["text"]
    print(f"Posting ID {target_post['id']}:\n{text}\n")

    # APIクライアント初期化
    client = tweepy.Client(
        consumer_key=os.environ.get("X_API_KEY"),
        consumer_secret=os.environ.get("X_API_KEY_SECRET"),
        access_token=os.environ.get("X_ACCESS_TOKEN"),
        access_token_secret=os.environ.get("X_ACCESS_TOKEN_SECRET"),
    )

    # 投稿実行
    response = client.create_tweet(text=text)
    tweet_id = response.data["id"]
    print(f"Post successful! Tweet ID: {tweet_id}")

    # ステータスを投稿済みに更新（JST時刻を記録）
    jst = timezone(timedelta(hours=9))
    target_post["posted"] = True
    target_post["posted_at"] = datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S JST")
    target_post["tweet_id"] = tweet_id

    save_posts(posts)
    print("posts.json updated.")

if __name__ == "__main__":
    post_next()