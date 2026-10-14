import os, time, requests
from bs4 import BeautifulSoup
from threading import Thread
from flask import Flask

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7393523550")

app = Flask(__name__)

@app.route('/')
def home():
    return "ALL NEWS Bot LIVE - Har news pe alert! Go to /test"

@app.route('/test')
def test_alert():
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        msg = "TEST ALERT SUCCESS!\n\nUSD - Test News (7 PM demo)\nActual: 5.5%\nForecast: 5.0%\nPrevious: 4.8%\n\nBot 100% Working! 7 PM news pe alert ayega!"
        requests.get(url, params={"chat_id": CHAT_ID, "text": msg}, timeout=10)
        return "Test alert sent to Telegram! Check now!"
    except Exception as e:
        return f"Error: {e}"

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.get(url, params={"chat_id": CHAT_ID, "text": msg}, timeout=10)
        print(f"Sent: {msg[:80]}")
    except Exception as e:
        print(f"Telegram error: {e}")

def scrape():
    headers = {"User-Agent": "Mozilla/5.0"}
    events = []
    try:
        r = requests.get("https://www.forexfactory.com/calendar", headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, 'html.parser')
        rows = soup.select("tr.calendar__row")
        for row in rows:
            try:
                currency = row.select_one(".calendar__currency")
                event_el = row.select_one(".calendar__event")
                actual_el = row.select_one(".calendar__actual")
                forecast_el = row.select_one(".calendar__forecast")
                previous_el = row.select_one(".calendar__previous")
                ct = currency.text.strip() if currency else ""
                et = event_el.text.strip() if event_el else ""
                at = actual_el.text.strip() if actual_el else ""
                ft = forecast_el.text.strip() if forecast_el else ""
                pt = previous_el.text.strip() if previous_el else ""
                if et and at:
                    events.append({"currency": ct, "event": et, "actual": at, "forecast": ft, "previous": pt})
            except:
                continue
    except Exception as e:
        print(f"Scrape error: {e}")
    return events

alerted = set()

def bot_loop():
    send_telegram("ALL NEWS Bot Started! Har news pe alert ayega - Red/Orange/Yellow/Silver. Test: /test kholo. 24/7 LIVE")
    while True:
        try:
            events = scrape()
            print(f"Found {len(events)} events with Actual")
            for ev in events:
                key = f"{ev['currency']}-{ev['event']}-{ev['actual']}"
                if key in alerted:
                    continue
                alerted.add(key)
                msg = f"NEWS AA GAYI!\n\n{ev['currency']} - {ev['event']}\nActual: {ev['actual']}\nForecast: {ev['forecast'] or 'N/A'}\nPrevious: {ev['previous'] or 'N/A'}"
                send_telegram(msg)
            if len(alerted) > 500:
                alerted.clear()
        except Exception as e:
            print(f"Loop error: {e}")
        time.sleep(30)

if __name__ == "__main__":
    Thread(target=bot_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
