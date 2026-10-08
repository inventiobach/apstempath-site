"""
X (Twitter) 見込み客リサーチ＆リードファインダー
AP STEM Path - Prospect Lead Finder for X (Twitter)

【機能】
1. インター校・海外大進学・AP理数・公文の壁などに悩む親御さんのリアルタイムポストを抽出する
   最適化されたX（Twitter）高度検索URLを自動生成。
2. ブラウザで最新ポスト（Liveタブ、RT除外、生の声のみ）を即座に開く。
3. 毎日のルーティン（1日2分）でフォロー＆いいねを行うための専用HTMLダッシュボードを自動生成・表示。
"""

import os
import sys
import webbrowser
import urllib.parse
from datetime import datetime

# 検索クエリ定義（RT除外、日本語、生の声・悩みにフォーカス）
SEARCH_PRESETS = [
    {
        "id": "intl_math",
        "title": "① インター校・帰国生の「Math/数学」悩み",
        "badge": "最重要ターゲット",
        "desc": "「学校のMathはAなのにAPで苦戦」「現地の進度についていけない」「英語での数学理解に限界」など",
        "x_query": '(インター校 OR 現地校 OR インター生 OR 帰国生 OR 帰国子女) (数学 OR Math OR Calculus OR 微積分 OR 代数) -filter:retweets lang:ja',
        "google_query": 'site:x.com ("インター校" OR "現地校" OR "帰国生") ("数学" OR "Math" OR "Calculus")',
        "advice": "「Mathの成績は良いのに高校の記述（FRQ）で失速する」という構造的悩みに最も刺さります。共感いいね＋プロフィールへの誘導が効果的です。"
    },
    {
        "id": "ap_stem",
        "title": "② AP微積分 (Calculus)・AP理数の苦戦＆対策",
        "badge": "今すぐ客",
        "desc": "「AP Calculus BCが難しすぎる」「Score 5取れるか不安」「過去問やFRQで点が出ない」「塾が見つからない」",
        "x_query": '("AP Calculus" OR "Calculus BC" OR "Calculus AB" OR "AP Math" OR "AP物理" OR "AP CS") (難しい OR 対策 OR 塾 OR スコア OR 過去問 OR つまず) -filter:retweets lang:ja',
        "google_query": 'site:x.com ("AP Calculus" OR "Calculus BC" OR "AP CS") ("対策" OR "難しい" OR "Score")',
        "advice": "まさに今AP試験対策に困っている中高生や親御さん。元OS・JVM開発者の専門性やnoteの攻略記事が劇的に信頼されます。"
    },
    {
        "id": "tuition_scholarship",
        "title": "③ 米大学・海外大の学費高騰・円安・奨学金",
        "badge": "共感・拡散大",
        "desc": "「学費4000万〜5000万で絶望」「1ドル150円超で留学断念危機」「給付型奨学金の倍率が高すぎる」",
        "x_query": '(米大学 OR アメリカ大学 OR 海外大 OR 米国大学) (学費 OR 円安 OR 奨学金 OR "4000万" OR "5000万" OR 費用) -filter:retweets lang:ja',
        "google_query": 'site:x.com ("米大学" OR "アメリカ大学" OR "海外大") ("学費" OR "円安" OR "奨学金")',
        "advice": "「定価で払わず、AP理数単位免除で1年分（約1,000万円）を短縮するハック」が強烈な解決策として響きます。"
    },
    {
        "id": "kumon_limits",
        "title": "④ 公文式の壁・算数先取り・高校数学の挫折",
        "badge": "潜在層・早期層",
        "desc": "「公文で数IIIまで進んだのに高校数学が解けない」「計算は速いのに文章題・数理モデリングができない」",
        "x_query": '(公文 OR くもん) (数III OR 高校数学 OR 微積分 OR つまづ OR 壁 OR 挫折 OR 伸び悩み) -filter:retweets lang:ja',
        "google_query": 'site:x.com ("公文" OR "くもん") ("数III" OR "高校数学" OR "壁" OR "挫折")',
        "advice": "小中学生の早期教育熱心な保護者。計算スピードと数理モデリング（思考力）の違いを説いたnote記事がドンピシャです。"
    },
    {
        "id": "programming_order",
        "title": "⑤ Scratchの限界・本格プログラミングへの移行",
        "badge": "IT・CS志望層",
        "desc": "「Scratchは何年もやったのにテキストコード（Java/Python）が書けない」「教室選びに悩んでいる」",
        "x_query": '(Scratch OR スクラッチ) (プログラミング OR Java OR Python OR テキストコード OR 限界 OR 移行) -filter:retweets lang:ja',
        "google_query": 'site:x.com ("Scratch" OR "スクラッチ") ("Java" OR "Python" OR "プログラミング教室")',
        "advice": "元JVM開発者の視点から「ブロックとテキストの境界（型・メモリ）」を語る権威性が群を抜いて刺さります。"
    },
    {
        "id": "elite_stem",
        "title": "⑥ 米トップ大STEM志望・IBDP・ボーディング校親",
        "badge": "高LTV顧客",
        "desc": "「MIT/スタンフォード/CMUを目指している」「IB Math HLが過酷」「サマープログラムどうするか」",
        "x_query": '(インター校 OR ボーディングスクール OR 海外進学) (STEM OR MIT OR スタンフォード OR CMU OR "IB Math") -filter:retweets lang:ja',
        "google_query": 'site:x.com ("インター校" OR "ボーディングスクール") ("STEM" OR "MIT" OR "CMU")',
        "advice": "高単価個別指導（月額10万〜）の決定権を持つ熱心なご家庭。実績やCMU・Georgia Techの分析記事が有効です。"
    }
]

def make_x_url(query: str, mode: str = "live") -> str:
    encoded = urllib.parse.quote(query)
    if mode == "live":
        return f"https://x.com/search?q={encoded}&f=live"
    return f"https://x.com/search?q={encoded}"

def make_google_url(query: str, timeframe: str = "w") -> str:
    encoded = urllib.parse.quote(query)
    # timeframe: w=過去1週間, d=過去24時間, m=過去1ヶ月
    return f"https://www.google.com/search?q={encoded}&tbs=qdr:{timeframe}"

def generate_dashboard_html(output_path: str):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    cards_html = ""
    for idx, p in enumerate(SEARCH_PRESETS, 1):
        x_live_url = make_x_url(p["x_query"], mode="live")
        x_top_url = make_x_url(p["x_query"], mode="top")
        g_week_url = make_google_url(p["google_query"], timeframe="w")
        
        cards_html += f"""
        <div class="card">
            <div class="card-header">
                <span class="badge">{p['badge']}</span>
                <h3>{p['title']}</h3>
            </div>
            <p class="desc">{p['desc']}</p>
            
            <div class="btn-group">
                <a href="{x_live_url}" target="_blank" class="btn btn-primary">
                    <span class="icon">⚡</span> X 最新ポストを開く (Live)
                </a>
                <a href="{x_top_url}" target="_blank" class="btn btn-secondary">
                    <span class="icon">🔥</span> X 話題ポスト
                </a>
                <a href="{g_week_url}" target="_blank" class="btn btn-outline">
                    <span class="icon">🔍</span> Google (直近1週間)
                </a>
            </div>
            
            <div class="advice-box">
                <div class="advice-label">💡 アプローチのヒント</div>
                <div class="advice-text">{p['advice']}</div>
            </div>
        </div>
        """
        
    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>X (Twitter) 見込み客リサーチ・ダッシュボード | AP STEM PATH</title>
    <style>
        :root {{
            --bg: #0f172a;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
            --accent: #38bdf8;
            --accent-hover: #0ea5e9;
            --primary: #2563eb;
            --primary-hover: #1d4ed8;
            --border: #334155;
            --badge-bg: #0369a1;
            --badge-text: #e0f2fe;
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }}
        body {{
            background-color: var(--bg);
            color: var(--text-main);
            padding: 24px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        header {{
            margin-bottom: 24px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            flex-wrap: wrap;
            gap: 16px;
        }}
        .header-title h1 {{
            font-size: 24px;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .header-title p {{
            color: var(--text-sub);
            font-size: 14px;
            margin-top: 4px;
        }}
        .batch-actions {{
            display: flex;
            gap: 12px;
        }}
        .banner {{
            background: linear-gradient(135deg, #1e3a8a, #0f172a);
            border: 1px solid #3b82f6;
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 24px;
            font-size: 14px;
            color: #cbd5e1;
        }}
        .banner strong {{
            color: #38bdf8;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(460px, 1fr));
            gap: 20px;
        }}
        @media (max-width: 600px) {{
            .grid {{
                grid-template-columns: 1fr;
            }}
        }}
        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 14px;
            transition: transform 0.15s, border-color 0.15s;
        }}
        .card:hover {{
            border-color: #60a5fa;
            transform: translateY(-2px);
        }}
        .card-header {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}
        .badge {{
            align-self: flex-start;
            background: var(--badge-bg);
            color: var(--badge-text);
            font-size: 12px;
            font-weight: 600;
            padding: 2px 10px;
            border-radius: 9999px;
            letter-spacing: 0.02em;
        }}
        .card-header h3 {{
            font-size: 18px;
            color: #fff;
        }}
        .desc {{
            font-size: 13px;
            color: var(--text-sub);
        }}
        .btn-group {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 4px;
        }}
        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.15s;
        }}
        .btn-primary {{
            background: var(--primary);
            color: #fff;
        }}
        .btn-primary:hover {{
            background: var(--primary-hover);
        }}
        .btn-secondary {{
            background: #334155;
            color: #f1f5f9;
        }}
        .btn-secondary:hover {{
            background: #475569;
        }}
        .btn-outline {{
            background: transparent;
            color: #94a3b8;
            border: 1px solid #475569;
        }}
        .btn-outline:hover {{
            color: #fff;
            border-color: #94a3b8;
        }}
        .btn-large {{
            padding: 10px 18px;
            font-size: 14px;
            background: #0284c7;
            color: #fff;
        }}
        .btn-large:hover {{
            background: #0369a1;
        }}
        .advice-box {{
            background: rgba(15, 23, 42, 0.6);
            border-left: 3px solid #38bdf8;
            border-radius: 0 6px 6px 0;
            padding: 10px 12px;
            font-size: 12px;
            margin-top: auto;
        }}
        .advice-label {{
            font-weight: bold;
            color: #38bdf8;
            margin-bottom: 2px;
        }}
        .advice-text {{
            color: #cbd5e1;
            line-height: 1.5;
        }}
        footer {{
            margin-top: 36px;
            text-align: center;
            font-size: 12px;
            color: var(--text-sub);
            border-top: 1px solid var(--border);
            padding-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="header-title">
                <h1>🎯 X 見込み客リサーチ・ダッシュボード</h1>
                <p>AP STEM PATH | 毎朝・夕方の1日2分ルーティン（最終更新: {now_str}）</p>
            </div>
            <div class="batch-actions">
                <button onclick="openTopTargets()" class="btn btn-large">
                    🚀 主要3カテゴリを一括オープン
                </button>
            </div>
        </header>

        <div class="banner">
            📌 <strong>【1日2分の運用ルール】</strong><br>
            ボタンを押すとXの「最新（Live）」検索結果が開きます。RT除外・日本語のリアルな悩みが並んでいます。<br>
            共感できるポストをした親御さんを <strong>1日3〜5人手動でフォロー ＆「いいね」を1つ押す</strong> だけ！相手に通知が届き、あなたの洗練されたプロフィールとnote記事へ流入します。
        </div>

        <div class="grid">
            {cards_html}
        </div>

        <footer>
            AP STEM PATH - Bilingual STEM & US College Admissions Engineering<br>
            ※完全手動操作のためXの利用規約に100%準拠。アカウント凍結リスクはありません。
        </footer>
    </div>

    <script>
        function openTopTargets() {{
            const urls = [
                "{make_x_url(SEARCH_PRESETS[0]['x_query'], mode='live')}",
                "{make_x_url(SEARCH_PRESETS[1]['x_query'], mode='live')}",
                "{make_x_url(SEARCH_PRESETS[2]['x_query'], mode='live')}"
            ];
            urls.forEach(url => window.open(url, '_blank'));
        }}
    </script>
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

def main():
    try:
        if sys.platform == 'win32':
            sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

    dashboard_path = os.path.join(os.path.dirname(__file__), "lead_research_dashboard.html")
    generate_dashboard_html(dashboard_path)
    
    print("\n" + "=" * 65)
    print(" [X (Twitter) 見込み客リサーチ＆リードファインダー]")
    print("    AP STEM PATH | 1日2分ルーティン・ツール")
    print("=" * 65)
    print("\n[生成完了] ダッシュボードHTMLを作成しました:")
    print(f" -> {dashboard_path}\n")
    
    print("ブラウザでダッシュボードを開きます...")
    webbrowser.open(f"file:///{os.path.abspath(dashboard_path).replace(os.sep, '/')}")
    
    print("\n各プリセットの直接URL一覧:")
    for idx, p in enumerate(SEARCH_PRESETS, 1):
        x_url = make_x_url(p["x_query"], mode="live")
        print(f"[{idx}] {p['title']}")
        print(f"    URL: {x_url}\n")
    
    print("=" * 65)
    print("ブラウザのダッシュボードからボタンをクリックしてリサーチを開始してください。")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    main()
