import os
from flask import Flask
import threading
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot LIVE!"

@app.route('/health')
def health():
    return "OK - Bot is awake", 200

@app.route('/test')
def test():
    return "Test route OK - Add BOT_TOKEN later!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def run_bot():
    try:
        import telebot
        BOT_TOKEN = os.getenv("BOT_TOKEN")
        CHAT_ID = os.getenv("CHAT_ID")
        if not BOT_TOKEN:
            print("BOT_TOKEN missing - Flask will keep running!")
            while True:
                time.sleep(60)
        bot = telebot.TeleBot(BOT_TOKEN)
        print("Bot polling started...")
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"Bot error: {e}")
        while True:
            time.sleep(60)

if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()
    print("Flask started, now running bot...")
    run_bot()
