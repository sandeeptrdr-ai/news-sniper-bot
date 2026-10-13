import os, time, re, requests
from threading import Thread
from flask import Flask
BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID=os.getenv("TELEGRAM_CHAT_ID","7393523550")
app=Flask(__name__)
@app.route('/')
def home(): return "✅ News Sniper Bot LIVE 24/7 - All Colors"
def send_telegram(msg):
 try: requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",params={"chat_id":CHAT_ID,"text":msg,"parse_mode":"Markdown"},timeout=10)
 except: pass
def parse_number(s):
 if not s: return None
 m=re.search(r'-?\d+\.?\d*', s.replace("%",""))
 return float(m.group()) if m else None
def scrape():
 try:
  r=requests.get("https://www.forexfactory.com/calendar",headers={"User-Agent":"Mozilla/5.0"},timeout=15)
  from bs4 import BeautifulSoup
  soup=BeautifulSoup(r.text,'html.parser')
  rows=soup.select("tr.calendar__row")
  evs=[]
  for row in rows:
   try:
    cur=row.select_one(".calendar__currency")
    evt=row.select_one(".calendar__event")
    act=row.select_one(".calendar__actual")
    fore=row.select_one(".calendar__forecast")
    evs.append({"currency":cur.text.strip() if cur else "","event":evt.text.strip() if evt else "","actual":act.text.strip() if act else "","forecast":fore.text.strip() if fore else ""})
   except: continue
  return evs
 except: return []
alerted=set()
def loop():
 send_telegram("✅ *News Sniper Started!*\n24/7 LIVE on Render\nAll News Red/Orange/Yellow >10% gap alert")
 while True:
  try:
   for ev in scrape():
    a=parse_number(ev["actual"]); f=parse_number(ev["forecast"])
    if a is None or f is None or f==0: continue
    gap=abs((a-f)/f)*100
    if gap>10:
     key=f"{ev['currency']}-{ev['event']}-{ev['actual']}"
     if key in alerted: continue
     alerted.add(key)
     sig="SELL XAUUSD" if a>f else "BUY XAUUSD"
     if ev["currency"]=="USD": sig=f"{sig} / USD {'Strong' if a>f else 'Weak'}"
     send_telegram(f"🚨 *NEWS GAP {gap:.1f}%*\n{ev['currency']} {ev['event']}\nActual: {ev['actual']}\nForecast: {ev['forecast']}\nSignal: {sig}")
  except: pass
  time.sleep(60)
if __name__=="__main__":
 Thread(target=loop,daemon=True).start()
 app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))
