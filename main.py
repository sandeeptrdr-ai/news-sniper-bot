import os
from flask import Flask
import threading
import telebot
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telebot.TeleBot(BOT_TOKEN) if BOT_TOKEN else None
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot LIVE - News Sniper running!"

@app.route('/health')
def health():
    return "OK - Bot is awake", 200

@app.route('/test')
def test():
    if bot and CHAT_ID:
        try:
            bot.send_message(CHAT_ID, "✅ TEST SUCCESS - Bot LIVE!")
            return "Message sent!"
        except Exception as e:
            return f"Error: {e}"
    return "BOT_TOKEN or CHAT_ID missing!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def run_bot():
    if not bot:
        print("BOT_TOKEN missing!")
        return
    while True:
        try:
            print("Bot polling...")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Bot error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()
    run_bot()
