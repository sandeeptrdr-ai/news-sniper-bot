from flask import Flask
import os
import telebot

app = Flask(__name__)

# TERA TOKEN + CHAT ID YAHAN ADD HAI
BOT_TOKEN_DIRECT = "-8849871999:AAGpyVcLESkyao9XiaJjdZqOGGU4fMVCC_s"
CHAT_ID_DIRECT = "7393523550"

# Pehle Environment se lega, nahi mila to direct wala lega
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN") or BOT_TOKEN_DIRECT
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") or os.getenv("CHAT_ID") or CHAT_ID_DIRECT

bot = telebot.TeleBot(BOT_TOKEN) if BOT_TOKEN else None

def send_telegram(msg):
    try:
        if bot and CHAT_ID:
            bot.send_message(CHAT_ID, msg)
            print(f"Sent to {CHAT_ID}")
    except Exception as e:
        print(f"Error: {e}")

@app.route('/')
def home():
    return "News Sniper LIVE - Token Added!"

@app.route('/health')
def health():
    return "OK", 200

@app.route('/test')
def test():
    try:
        send_telegram("✅ Sandeep FINAL TEST - Bot UP hai!\n\nToken + Chat ID add ho gaya hai!\nChat ID: 7393523550\nAb 7 PM news pe alert ayega!\n100% Working!")
        return f"✅ Telegram pe bhej diya! Chat: {CHAT_ID}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
