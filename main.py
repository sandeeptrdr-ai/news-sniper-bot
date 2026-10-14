import os
import time
import threading
import requests
from flask import Flask
from datetime import datetime

app = Flask(__name__)

# --- CONFIG ---
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHAT_ID = os.getenv("CHAT_ID", "")

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Error: {e}")

def check_news_loop():
    print("News Sniper Loop Started...")
    while True:
        try:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Bot LIVE")
            time.sleep(30)
        except Exception as e:
            time.sleep(10)

@app.route('/')
def home():
    return "Bot LIVE - 100% Ready", 200

@app.route('/health')
def health():
    return "OK - Bot is awake", 200

@app.route('/test')
def test():
    send_telegram("🚀 <b>TEST SUCCESS!</b>\n\nSandeep tera bot 100% LIVE hai! UptimeRobot ab UP dikhayega!")
    return "Test sent to Telegram!", 200

if __name__ != "__main__":
    thread = threading.Thread(target=check_news_loop, daemon=True)
    thread.start()

if __name__ == "__main__":
    thread = threading.Thread(target=check_news_loop, daemon=True)
    thread.start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
