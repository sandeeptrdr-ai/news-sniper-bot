from flask import Flask
import os, telebot, threading, time, requests, json
from datetime import datetime
import pytz

app = Flask(__name__)

# === TERI FINAL IDS ===
BOT_TOKEN = "-8849871999:AAGpyVcLESkyao9XiaJjdZqOGGU4fMVCC_s"
CHAT_ID = "7393523550"

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or BOT_TOKEN
CHAT = os.getenv("TELEGRAM_CHAT_ID") or CHAT_ID
bot = telebot.TeleBot(TOKEN)

IST = pytz.timezone('Asia/Kolkata')
sent_today = set()  # Ek news ek hi baar bheje

def send(msg):
    try:
        bot.send_message(CHAT, msg, parse_mode='HTML')
        print(f"Sent: {msg[:50]}")
    except Exception as e:
        print(f"Error: {e}")

def fetch_forex_news():
    try:
        # ForexFactory ka official JSON
        url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        
        now_ist = datetime.now(IST)
        current_date_str = now_ist.strftime("%Y-%m-%d")
        
        for event in data:
            # Sirf USD + HIGH impact (Red folder)
            if event.get('country') != 'USD':
                continue
            if event.get('impact') != 'High':  # Red news only
                continue
            
            # Date check - aaj ki news
            event_time_str = event.get('date') # format: 2024-... check karo
            # ForexFactory date UTC me hota hai, hum IST se match karenge
            
            title = event.get('title', 'USD News')
            actual = event.get('actual', '')
            forecast = event.get('forecast', '')
            previous = event.get('previous', '')
            
            # Agar Actual aaya hai aur aaj tak nahi bheja
            key = f"{title}-{event.get('date')}"
            if actual and key not in sent_today:
                # 7 PM ke aas paas ho to bhejo (ya koi bhi High USD news)
                msg = f"""🚨 <b>USD HIGH IMPACT NEWS!</b>

<b>{title}</b>
Actual: <b>{actual}</b>
Forecast: {forecast}
Previous: {previous}

Time: {now_ist.strftime('%I:%M %p IST')}
Impact: 🔴 HIGH

Sandeep — Market move hone wala hai!"""
                send(msg)
                sent_today.add(key)
                time.sleep(2)
                
    except Exception as e:
        print(f"News fetch error: {e}")

def news_loop():
    print("News Loop Started - Checking every 60 sec...")
    while True:
        fetch_forex_news()
        # Har 60 sec check karega
        time.sleep(60)

# Background me news check start
threading.Thread(target=news_loop, daemon=True).start()

@app.route('/')
def home():
    return "News Sniper LIVE - Forex RED News Active! 🔴"

@app.route('/health')
def health():
    return "OK", 200

@app.route('/test')
def test():
    send(f"""✅ <b>FINAL CONFIRMED!</b>

Bot UP hai!
Token: {TOKEN[:12]}...
Chat ID: {CHAT}

Ab ready hai 7 PM USD RED news ke liye!
Har 60 sec me ForexFactory check kar raha hai!

100% Working! 🚀""")
    return f"✅ Test bhej diya! Chat: {CHAT}"

@app.route('/testnews')
def testnews():
    # 7 PM wala demo news
    send("""🚨 <b>USD HIGH IMPACT NEWS! (DEMO)</b>

<b>CPI m/m</b>
Actual: <b>0.4%</b>
Forecast: 0.3%
Previous: 0.2%

Time: 07:00 PM IST
Impact: 🔴 HIGH

Ye 7 PM pe asli news aise hi ayegi!""")
    return "Demo news sent!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
