from flask import Flask
import telebot
import os

app = Flask(__name__)

# FINAL IDS - Added
BOT_TOKEN = "-8849871999:AAGpyVcLESkyao9XiaJjdZqOGGU4fMVCC_s"
CHAT_ID = "7393523550"

# Use env if exists, else use direct
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or BOT_TOKEN
CHAT = os.getenv("TELEGRAM_CHAT_ID") or CHAT_ID

bot = telebot.TeleBot(TOKEN)

@app.route('/')
def home():
    return "News Sniper LIVE"

@app.route('/health')
def health():
    return "OK", 200

@app.route('/test')
def test():
    bot.send_message(CHAT, f"✅ FINAL CONFIRMED!\n\nBot UP hai!\nToken: {TOKEN[:10]}...\nChat ID: {CHAT}\n\nAb ready hai 7 PM news ke liye!\n100% Working!")
    return "Sent!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
