import os, time, re, requests
from bs4 import BeautifulSoup
from threading import Thread
from flask import Flask

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7393523550")

app = Flask(__name__)
@app.route('/')
def home():
    return "âœ… ALL NEWS Bot LIVE - Har news pe alert!"

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.get(url, params={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=10)
        print(f"Sent: {msg[:100]}")
    except Exception as e:
        print(f"Telegram error: {e}")

def scrape():
    # Try to get calendar - ForexFactory now uses heavy JS, so we try both forexfactory and investing fallback
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    events = []
    try:
        # Method 1: ForexFactory
        r = requests.get("https://www.forexfactory.com/calendar", headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, 'html.parser')
        rows = soup.select("tr.calendar__row")
        print(f"FF Rows found: {len(rows)}")
        for row in rows:
            try:
                currency = row.select_one(".calendar__currency")
                event_el = row.select_one(".calendar__event")
                actual_el = row.select_one(".calendar__actual")
                forecast_el = row.select_one(".calendar__forecast")
                previous_el = row.select_one(".calendar__previous")
                impact_el = row.select_one(".calendar__impact span")
                time_el = row.select_one(".calendar__time")

                currency_text = currency.text.strip() if currency else ""
                event_text = event_el.text.strip() if event_el else ""
                actual_text = actual_el.text.strip() if actual_el else ""
                forecast_text = forecast_el.text.strip() if forecast_el else ""
                previous_text = previous_el.text.strip() if previous_el else ""
                time_text = time_el.text.strip() if time_el else ""
                
                impact = "yellow"
                if impact_el:
                    cls = " ".join(impact_el.get("class", []))
                    if "high" in cls or "red" in cls.lower(): impact = "ðŸ”´ RED"
                    elif "medium" in cls or "orange" in cls.lower(): impact = "ðŸŸ  ORANGE"
                    elif "low" in cls or "yellow" in cls.lower(): impact = "ðŸŸ¡ YELLOW"
                    else: impact = cls
                else:
                    # try to find icon color from title
                    imp_title = row.get("data-impact", "")
                    if "High" in str(row): impact = "ðŸ”´ RED"
                    elif "Medium" in str(row): impact = "ðŸŸ  ORANGE"
                    elif "Low" in str(row): impact = "ðŸŸ¡ YELLOW"

                if event_text and actual_text: # Only if actual came
                    events.append({
                        "time": time_text,
                        "currency": currency_text,
                        "event": event_text,
                        "actual": actual_text,
                        "forecast": forecast_text,
                        "previous": previous_text,
                        "impact": impact
                    })
            except Exception as e:
                continue
    except Exception as e:
        print(f"Scrape error: {e}")
    return events

alerted = set()

def bot_loop():
    send_telegram("âœ… *ALL NEWS Bot Started!*\n\nAb *HAR NEWS* pe alert ayega - Red/Orange/Yellow/Silver\nChahe gap 0% ho ya 100%\n\n7 PM wali news ke liye Ready! ðŸš€\n24/7 LIVE on Render")
    while True:
        try:
            events = scrape()
            print(f"Found {len(events)} events with Actual")
            for ev in events:
                key = f"{ev['currency']}-{ev['event']}-{ev['actual']}"
                if key in alerted:
                    continue
                alerted.add(key)
                
                msg = f"ðŸš¨ *NEWS AA GAYI!*\n\nâ° Time: {ev['time']}\nðŸ’° {ev['currency']} - {ev['event']}\n{ev['impact']}\n\nðŸ“Š *Actual:* {ev['actual']}\nðŸ“ˆ Forecast: {ev['forecast'] or 'N/A'}\nðŸ“‰ Previous: {ev['previous'] or 'N/A'}\n\nâš¡ _Har news pe alert - No gap filter_"
                send_telegram(msg)
            
            if len(alerted) > 500:
                alerted.clear()
        except Exception as e:
            print(f"Loop error: {e}")
        time.sleep(30) # Check every 30 seconds for fast alert

if __name__ == "__main__":
    Thread(target=bot_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
