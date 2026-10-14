from flask import Flask
import os
import telebot

app = Flask(__name__)

# === TERI IDS YAHAN ADD HAIN ===
BOT_TOKEN = "-8849871999:AAGpyVcLESkyao9XiaJjdZqOGGU4fMVCC_s"
CHAT_ID = "7393523550"

# Environment me hai to wahan se lega, nahi to ye wala lega
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or BOT_TOKEN
CHAT = os.getenv("TELEGRAM_CHAT_ID") or CHAT_ID

bot = telebot.TeleBot(TOKEN)

@app.route('/')
def home():
    return "News Sniper LIVE - 24/7"

@app.route('/health')
def health():
    return "OK", 200

@app.route('/test')
def test():
    try:
        bot.send_message(CHAT, "✅ Sandeep FINAL TEST - Bot UP hai!\n\nToken + Chat ID add ho gaya hai!\nChat ID: 7393523550\nAb 7 PM news pe alert ayega!\n100% Working!")
        return f"✅ Telegram pe bhej diya! Chat: {CHAT}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
