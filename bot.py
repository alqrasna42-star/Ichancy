import telebot
from flask import Flask
import threading
from telebot import types

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

    # إذا كانت المحادثة مجموعة إدارة (Group أو Supergroup)
    if chat_type in ['group', 'supergroup']:
        # أزرار خاصة بالتحكم الإداري داخل المجموعة
        admin_markup = types.InlineKeyboardMarkup(row_width=2)
        btn_stats = types.InlineKeyboardButton("📊 إحصائيات البوت", callback_data="admin_stats")
        btn_broadcast = types.InlineKeyboardButton("📢 إرسال للكل", callback_data="admin_broadcast")
        btn_settings = types.InlineKeyboardButton("⚙️ إعدادات الحسابات", callback_data="admin_settings")
        admin_markup.add(btn_stats, btn_broadcast, btn_settings)

        admin_text = (
            f"🛠 **لوحة Dockers - مجموعة الإدارة** 🛠\n"
            f"==============================\n"
            f"📍 أيدي هذه المجموعة: `{chat_id}`\n"
            f"👤 أيدي المعلم (أبو النور): `{user_id}`\n\n"
            f"أهلاً بك يا معلمي، اختر أحد خيارات التحكم أدناه:"
        )
        bot.send_message(chat_id, admin_text, parse_mode="Markdown", reply_markup=admin_markup)
    
    else:
        # القائمة العادية للزبائن على الخاص
        user_markup = types.InlineKeyboardMarkup(row_width=2)
        btn_balance = types.InlineKeyboardButton("💰 شحن الرصيد", callback_data="recharge")
        btn_link = types.InlineKeyboardButton("⚡ ربط حساب ايشاني", callback_data="link_account")
        btn_support = types.InlineKeyboardButton("📞 الدعم الفني", callback_data="support")
        user_markup.add(btn_balance, btn_link, btn_support)

        user_text = (
            f"📊 **قائمة الخيارات الرئيسية** 📊\n\n"
            f"💰 الرصيد الحالي: SYP 0.0\n"
            f"🆔 أيدي حسابك: `{user_id}`\n"
            f"⚡ حساب ايشاني: غير مسجل"
        )
        bot.send_message(chat_id, user_text, parse_mode="Markdown", reply_markup=user_markup)

# معالجة الضغط على الأزرار (سواء للزبائن أو للإدارة بالمجموعة)
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data
    
    # خيارات لوحة الإدارة في المجموعة
    if data == "admin_stats":
        bot.answer_callback_query(call.id, "📊 البوت شغال 100% وحالياً متصل بنجاح.")
    elif data == "admin_broadcast":
        bot.answer_callback_query(call.id, "📢 ميزة الإذاعة جاهزة للاستخدام قريباً.")
    elif data == "admin_settings":
        bot.answer_callback_query(call.id, "⚙️ جاري فتح إعدادات النظام...")
        
    # خيارات الزبائن على الخاص
    elif data == "recharge":
        bot.answer_callback_query(call.id, "قريباً سيتم تفعيل نظام الشحن الآلي!")
    elif data == "link_account":
        bot.answer_callback_query(call.id, "أرسل كود الربط الخاص بك هنا.")
    elif data == "support":
        bot.answer_callback_query(call.id, "سيتم تحويلك للدعم الفني.")

if __name__ == '__main__':
    keep_alive()
    bot.infinity_polling()
