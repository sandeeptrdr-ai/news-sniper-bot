from flask import Flask
import os

# TERE ID YAHAN ADD HAIN
BOT_TOKEN_DIRECT = "-8849871999:AAE5hWMAytjXDW2ksZCWwyiw2Oab-bmg-Q0"
CHAT_ID_DIRECT = "7393523550"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot LIVE - News Sniper UP!"

@app.route('/health')
def health():
    return "OK - Bot is awake", 200

@app.route('/test')
def test():
    try:
        import telebot
        token = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN") or BOT_TOKEN_DIRECT
        chat = os.getenv("TELEGRAM_CHAT_ID") or os.getenv("CHAT_ID") or CHAT_ID_DIRECT
        
        bot = telebot.TeleBot(token)
        bot.send_message(chat, "✅ Sandeep FINAL TEST - Bot UP hai! Ye message code se aaya hai!")
        return f"✅ Telegram pe bhej diya! Chat: {chat}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
