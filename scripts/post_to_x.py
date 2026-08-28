import os
import tweepy

def post_tweet(text: str):
    # GitHub Secretsから認証情報を取得
    api_key = os.environ.get("X_API_KEY")
    api_key_secret = os.environ.get("X_API_KEY_SECRET")
    access_token = os.environ.get("X_ACCESS_TOKEN")
    access_token_secret = os.environ.get("X_ACCESS_TOKEN_SECRET")

    # X API v2 クライアントの初期化
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_key_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    # ポスト送信
    response = client.create_tweet(text=text)
    print(f"Post successful! Tweet ID: {response.data['id']}")

if __name__ == "__main__":
    # テスト投稿用テキスト
    sample_text = (
        "【AP Calculus BC × 米トップ大攻略】\n"
        "学費$50,000+削減とCMU/MIT合格を最短距離で狙う戦略設計。\n\n"
        "詳細シミュレーターはこちら👇\n"
        "https://apstempath.com/calculator/"
    )
    post_tweet(sample_text)