import telebot
import sqlite3
from flask import Flask
import threading

TOKEN = "9021613013:AAH14nGg2KbW7gIhhHz9Y3C3e3l-nxCOGoE"
bot = telebot.TeleBot(TOKEN)

# إنشاء قاعدة البيانات والحداول تلقائياً فور تشغيل البوت
def init_db():
    conn = sqlite3.connect('dockers_system.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            balance REAL DEFAULT 0.0,
            status TEXT DEFAULT 'active'
        )
    ''')
    conn.commit()
    conn.close()

init_db()

app = Flask('')

@app.route('/')
def home():
    return "Dockers Real System is running!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or "No Username"
    
    # حفظ المستخدم بقاعدة البيانات الحقيقية
    conn = sqlite3.connect('dockers_system.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()
    
    # جلب الرصيد الحقيقي من قاعدة البيانات
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    balance = row[0] if row else 0.0
    conn.close()

    bot.send_message(
        message.chat.id, 
        f"🛠 **أهلاً بك يا معلمي أبو النور في النظام الحقيقي** 🛠\n\n"
        f"🆔 أيدي حسابك: `{user_id}`\n"
        f"💰 رصيدك الحقيقي بقاعدة البيانات: `{balance} SYP`", 
        parse_mode="Markdown"
    )

if __name__ == '__main__':
    keep_alive()
    bot.infinity_polling()
