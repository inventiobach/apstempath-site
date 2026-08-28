import os
import json
import time
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

def post_thread():
    posts = load_posts()
    
    # 未投稿のスレッドを1件取得
    target = None
    for item in posts:
        if not item.get("posted", False):
            target = item
            break

    if not target:
        print("No pending threads left in queue.")
        return

    thread_texts = target.get("thread", [])
    if not thread_texts:
        print("Thread is empty.")
        return

    print(f"Posting Thread for: {target.get('university')} - {target.get('subject')}")

    # X API クライアント初期化
    client = tweepy.Client(
        consumer_key=os.environ.get("X_API_KEY"),
        consumer_secret=os.environ.get("X_API_KEY_SECRET"),
        access_token=os.environ.get("X_ACCESS_TOKEN"),
        access_token_secret=os.environ.get("X_ACCESS_TOKEN_SECRET"),
    )

    previous_tweet_id = None
    first_tweet_id = None

    for idx, text in enumerate(thread_texts):
        if previous_tweet_id is None:
            # 1投目（親ツイート）
            response = client.create_tweet(text=text)
            first_tweet_id = response.data["id"]
            previous_tweet_id = first_tweet_id
            print(f"[{idx + 1}/{len(thread_texts)}] Parent Tweet posted: {first_tweet_id}")
        else:
            # 2投目以降（ツリー返信）
            response = client.create_tweet(
                text=text,
                in_reply_to_tweet_id=previous_tweet_id
            )
            previous_tweet_id = response.data["id"]
            print(f"[{idx + 1}/{len(thread_texts)}] Reply posted: {previous_tweet_id}")
        
        time.sleep(2) # 投稿間隔を少し空ける

    # 投稿完了のステータス更新
    jst = timezone(timedelta(hours=9))
    target["posted"] = True
    target["posted_at"] = datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S JST")
    target["first_tweet_id"] = first_tweet_id

    save_posts(posts)
    print("Thread completely posted and posts.json updated.")

if __name__ == "__main__":
    post_thread()