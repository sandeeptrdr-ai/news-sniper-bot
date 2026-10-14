from flask import Flask
import os, telebot, threading, time, requests
from datetime import datetime
import pytz

app = Flask(__name__)

# === TERI IDS ===
BOT_TOKEN = "-8849871999:AAGpyVcLESkyao9XiaJjdZqOGGU4fMVCC_s"
CHAT_ID = "7393523550"

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or BOT_TOKEN
CHAT = os.getenv("TELEGRAM_CHAT_ID") or CHAT_ID
bot = telebot.TeleBot(TOKEN)

IST = pytz.timezone('Asia/Kolkata')
sent_today = set()

def send(msg):
    try:
        bot.send_message(CHAT, msg, parse_mode='HTML')
        print(f"Sent: {msg[:60]}")
    except Exception as e:
        print(f"Error: {e}")

def fetch_all_forex_news():
    try:
        url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        data = r.json()
        
        now_ist = datetime.now(IST)
        
        for event in data:
            title = event.get('title', 'News')
            country = event.get('country', 'ALL')
            impact = event.get('impact', 'Low')
            actual = event.get('actual', '')
            forecast = event.get('forecast', '')
            previous = event.get('previous', '')
            
            # Key - ek news ek hi baar
            key = f"{country}-{title}-{event.get('date')}"
            
            # Sirf tab bhejo jab Actual aaya ho aur pehle na bheja ho
            if actual and key not in sent_today:
                
                # Emoji impact ke hisab se
                if impact == 'High':
                    emoji = '🔴'
                elif impact == 'Medium':
                    emoji = '🟠'
                else:
                    emoji = '🟡'
                
                msg = f"""{emoji} <b>{country} FOREX NEWS!</b>

<b>{title}</b>
Actual: <b>{actual}</b>
Forecast: {forecast}
Previous: {previous}

Time: {now_ist.strftime('%I:%M %p IST')}
Country: {country}
Impact: {emoji} {impact}

Sandeep — Market alert!"""
                
                send(msg)
                sent_today.add(key)
                time.sleep(1)  # 1 sec gap taaki spam na lage
                
    except Exception as e:
        print(f"News error: {e}")

def news_loop():
    print("OPTION 3 LOOP Started - All Currency All News - Checking every 45 sec...")
    while True:
        fetch_all_forex_news()
        time.sleep(45)  # Har 45 sec check

threading.Thread(target=news_loop, daemon=True).start()

@app.route('/')
def home():
    return "News Sniper LIVE - ALL Currency ALL News Active! 🌍"

@app.route('/health')
def health():
    return "OK", 200

@app.route('/test')
def test():
    send(f"""✅ <b>OPTION 3 ACTIVE!</b>

Ab tujhe FOREX ki SABHI currency ki SABHI news ayegi!

USD, EUR, GBP, JPY, AUD, CAD, NZD, CHF
🔴 HIGH + 🟠 MEDIUM + 🟡 LOW

Har 45 sec check ho raha hai!
100% Working!""")
    return "Option 3 Test Sent!"

@app.route('/testnews')
def testnews():
    send("""🟡 <b>EUR FOREX NEWS! (DEMO - OPTION 3)</b>

<b>German CPI m/m</b>
Actual: <b>0.3%</b>
Forecast: 0.2%
Previous: 0.1%

Time: 11:27 AM IST
Country: EUR
Impact: 🟡 Low

Ab aise hi USD, EUR, GBP sab ki news ayegi!""")
    return "Option 3 Demo Sent!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
