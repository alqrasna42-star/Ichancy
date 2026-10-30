import telebot
from flask import Flask
import threading

TOKEN = "9021613013:AAH14nGg2KbW7gIhhHz9Y3C3e31-nxCOGoE"
bot = telebot.TeleBot(TOKEN)

app = Flask('')

@app.route('/')
def home():
    return "Ichancy Bot is alive and running!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    chat_type = message.chat.type

    if chat_type in ['group', 'supergroup']:
        admin_text = (
            f"🛠 **لوحة Dockers - مجموعة الإدارة** 🛠\n"
            f"==============================\n"
            f"📍 أيدي هذه المجموعة: `{chat_id}`\n"
            f"أهلاً بك يا معلمي في لوحة التحكم الإدارية"
        )
        bot.send_message(chat_id, admin_text, parse_mode="Markdown")
    else:
        user_text = (
            f"📊 **قائمة الخيارات الرئيسية** 📊\n\n"
            f"💰 الرصيد الحالي: SYP 0.0\n"
            f"🆔 أيدي حسابك: `{user_id}`\n"
            f"⚡ حساب ايشاني: غير مسجل"
        )
        bot.send_message(chat_id, user_text, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    pass

if __name__ == '__main__':
    keep_alive()
    bot.infinity_polling()
