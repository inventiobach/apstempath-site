import os
import json
from datetime import datetime, timezone, timedelta
import resend

CAMPAIGNS_FILE = os.path.join(os.path.dirname(__file__), "outreach_campaigns.json")

def load_campaigns():
    if not os.path.exists(CAMPAIGNS_FILE):
        print("outreach_campaigns.json not found.")
        return []
    with open(CAMPAIGNS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_campaigns(campaigns):
    with open(CAMPAIGNS_FILE, "w", encoding="utf-8") as f:
        json.dump(campaigns, f, ensure_ascii=False, indent=2)

def generate_html(campaign, recipient_name):
    bullets_html = "".join([f"<li style='margin-bottom: 8px;'>{b}</li>" for b in campaign["summary_bullets"]])
    return f"""
    <div style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; line-height: 1.7; color: #1e293b; max-width: 600px; margin: 0 auto; padding: 24px; border: 1px solid #e2e8f0; border-radius: 8px;">
        <p style="font-size: 14px; color: #64748b; margin-bottom: 12px;">AP STEM PATH | プレス＆高等教育インサイト</p>
        <h2 style="color: #0f172a; font-size: 20px; border-bottom: 2px solid #2563eb; padding-bottom: 12px; margin-top: 0;">{campaign["headline"]}</h2>
        <p>{recipient_name} 様</p>
        <p>米最難関工科大学におけるAP単位認定ポリシーおよび学費圧縮・早期キャリア形成に関する最新分析レポートをお届けします。</p>
        
        <div style="background-color: #f8fafc; border-left: 4px solid #2563eb; padding: 16px; margin: 20px 0; border-radius: 0 4px 4px 0;">
            <h4 style="margin: 0 0 10px 0; color: #0f172a;">【エグゼクティブ・サマリー】</h4>
            <ul style="margin: 0; padding-left: 20px;">
                {bullets_html}
            </ul>
        </div>

        <p style="margin-top: 24px;">
            <a href="{campaign['link_url']}" style="background-color: #2563eb; color: #ffffff; padding: 12px 20px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">レポート全文・詳細解説を見る →</a>
        </p>

        <p style="font-size: 13px; color: #64748b; margin-top: 24px;">
            学費削減・単位スキップROI試算: <a href="{campaign['calculator_url']}" style="color: #2563eb;">オンラインシミュレーター</a>
        </p>

        <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 30px 0 16px 0;" />
        <p style="font-size: 12px; color: #94a3b8; margin: 0;">
            AP STEM PATH / MathTutor-AI Academy<br>
            Web: <a href="https://apstempath.com/" style="color: #94a3b8;">https://apstempath.com/</a>
        </p>
    </div>
    """

def run_outreach():
    api_key = os.environ.get("RESEND_API_KEY")
    sender_email = os.environ.get("SENDER_EMAIL", "AP STEM PATH <newsletter@apstempath.com>")

    if not api_key:
        print("Error: RESEND_API_KEY is not set.")
        return

    resend.api_key = api_key
    campaigns = load_campaigns()
    jst = timezone(timedelta(hours=9))

    updated = False
    for campaign in campaigns:
        if campaign.get("status") != "ready":
            continue

        print(f"Starting Campaign: {campaign['id']}")
        for recipient in campaign.get("recipients", []):
            if recipient.get("sent", False):
                continue

            html_content = generate_html(campaign, recipient.get("name", "関係者"))
            try:
                params = {
                    "from": sender_email,
                    "to": [recipient["email"]],
                    "subject": campaign["subject"],
                    "html": html_content,
                }
                res = resend.Emails.send(params)
                print(f"Sent to {recipient['email']} - ID: {res.get('id', 'OK')}")
                recipient["sent"] = True
                recipient["sent_at"] = datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S JST")
                updated = True
            except Exception as e:
                print(f"Failed to send to {recipient['email']}: {e}")

        # 全員に送信完了したらステータスを sent に更新
        all_sent = all(r.get("sent", False) for r in campaign.get("recipients", []))
        if all_sent:
            campaign["status"] = "sent"
            campaign["sent_at"] = datetime.now(jst).strftime("%Y-%m-%d %H:%M:%S JST")

    if updated:
        save_campaigns(campaigns)
        print("outreach_campaigns.json updated.")
    else:
        print("No pending emails to send.")

if __name__ == "__main__":
    run_outreach()