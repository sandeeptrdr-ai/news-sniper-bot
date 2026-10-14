import os, time, requests
from bs4 import BeautifulSoup
from threading import Thread
from flask import Flask

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7393523550")

app = Flask(__name__)

@app.route('/')
def home():
    return "âœ… ALL NEWS Bot LIVE - Har news pe alert! | Go to /test for testing"

@app.route('/test')
def test_alert():
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        msg = "ðŸ§ª *TEST ALERT SUCCESS!*\n\nðŸ’° USD - Test News (7 PM wali ka demo)\nðŸ“Š Actual: 5.5%\nðŸ“ˆ Forecast: 5.0%\nðŸ“‰ Previous: 4.8%\n\nâœ… Bot 100% Working hai! 7 PM wali news pe aise hi alert ayega!\nðŸš€ 24/7 LIVE"
        requests.get(url, params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=10)
        return "âœ… Test alert sent to Telegram! Check your bot now!"
    except Exception as e:
        return f"Error: {e}"

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.get(url, params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=10)
        print(f"Sent: {msg[:100]}")
    except Exception as e:
        print(f"Telegram error: {e}")

def scrape():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
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
                currency_text = currency.text.strip() if currency else ""
                event_text = event_el.text.strip() if event_el else ""
                actual_text = actual_el.text.strip() if actual_el else ""
                forecast_text = forecast_el.text.strip() if forecast_el else ""
                previous_text = previous_el.text.strip() if previous_el else ""
                if event_text and actual_text:
                    events.append({"currency": currency_text, "event": event_text, "actual": actual_text, "forecast": forecast_text, "previous": previous_text})
            except:
                continue
    except Exception as e:
        print(f"Scrape error: {e}")
    return events

alerted = set()

def bot_loop():
    send_telegram("âœ… *ALL NEWS Bot Started!*\n\nAb HAR NEWS pe alert ayega - Red/Orange/Yellow/Silver\nChahe gap 0% ho ya 100%\n\nTest ke liye /test kholo\n24/7 LIVE on Render")
    while True:
        try:
            events = scrape()
            print(f"Found {len(events)} events with Actual")
            for ev in events:
                key = f"{ev['currency']}-{ev['event']}-{ev['actual']}"
                if key in alerted:
                    continue
                alerted.add(key)
                msg = f"ðŸš¨ *NEWS AA GAYI!*\n\nðŸ’° {ev['currency']} - {ev['event']}\n\nðŸ“Š *Actual:* {ev['actual']}\nðŸ“ˆ Forecast: {ev['forecast'] or 'N/A'}\nðŸ“‰ Previous: {ev['previous'] or 'N/A'}\n\nâš¡ _Har news pe alert_"
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
