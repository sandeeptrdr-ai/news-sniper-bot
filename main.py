import os
from flask import Flask
import threading
import telebot
import time

# TERE ID - MAINE ADD KAR DIYE
BOT_TOKEN_HARDCODED = "-8849871999:AAE5hWMAytjXDW2ksZCWwyiw2Oab-bmg-Q0"
CHAT_ID_HARDCODED = "7393523550"

app = Flask(__name__)

def get_token():
    return os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN") or BOT_TOKEN_HARDCODED

def get_chat():
    return os.getenv("CHAT_ID") or os.getenv("TELEGRAM_CHAT_ID") or CHAT_ID_HARDCODED

@app.route('/')
def home():
    return "Bot LIVE - News Sniper UP!"

@app.route('/health')
def health():
    return "OK - Bot is awake", 200

@app.route('/test')
def test():
    BOT_TOKEN = get_token()
    CHAT_ID = get_chat()
    try:
        bot = telebot.TeleBot(BOT_TOKEN)
        bot.send_message(CHAT_ID, "✅ Sandeep FINAL TEST - Tera News Sniper UP hai! 🔥")
        return "✅ Message sent to Telegram! Check kar!"
    except Exception as e:
        return f"Telegram Error: {e} | Token={BOT_TOKEN[:10]}... Chat={CHAT_ID}"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def run_bot():
    BOT_TOKEN = get_token()
    if not BOT_TOKEN:
        print("No token!")
        while True:
            time.sleep(60)
    bot = telebot.TeleBot(BOT_TOKEN)
    print("Bot polling started...")
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Bot error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()
