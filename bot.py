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

    # لوحة مجموعة الإدارة الكاملة
    if chat_type in ['group', 'supergroup']:
        admin_markup = types.InlineKeyboardMarkup(row_width=2)
        
        # صف 1: نشاط لاعب
        btn1 = types.InlineKeyboardButton("🔄 نشاط لاعب", callback_data="player_activity")
        admin_markup.add(btn1)
        
        # صف 2: تصفير نقاط وتسري رصيد
        btn2 = types.InlineKeyboardButton("⭐ تصفير نقاط لاعب", callback_data="reset_points")
        btn3 = types.InlineKeyboardButton("💰 تصفير رصيد لاعب", callback_data="reset_balance")
        admin_markup.add(btn2, btn3)
        
        # صف 3: بحث عن عملية
        btn4 = types.InlineKeyboardButton("🔍 بحث عن عملية", callback_data="search_op")
        admin_markup.add(btn4)
        
        # صف 4: شحن وحرق عملية
        btn5 = types.InlineKeyboardButton("📥 شحن عملية", callback_data="recharge_op")
        btn6 = types.InlineKeyboardButton("🔥 حرق عملية", callback_data="burn_op")
        admin_markup.add(btn5, btn6)
        
        # صف 5: حظر وإلغاء حظر مستخدم
        btn7 = types.InlineKeyboardButton("🚫 حظر مستخدم", callback_data="ban_user")
        btn8 = types.InlineKeyboardButton("⭕ إلغاء حظر مستخدم", callback_data="unban_user")
        admin_markup.add(btn7, btn8)
        
        # صف 6: إشكاليات وإعدادات البوت
        btn9 = types.InlineKeyboardButton("📊 إجماليات البوت", callback_data="bot_totals")
        btn10 = types.InlineKeyboardButton("⚙️ إعدادات البوت", callback_data="bot_settings")
        admin_markup.add(btn9, btn10)
        
        # صف 7: إرسال رسالة وأكواد الهدايا
        btn11 = types.InlineKeyboardButton("💬 إرسال رسالة", callback_data="send_msg")
        btn12 = types.InlineKeyboardButton("🎁 أكواد الهدايا", callback_data="gift_codes")
        admin_markup.add(btn11, btn12)
        
        # صف 8: شحن وسحب يدوي
        btn13 = types.InlineKeyboardButton("📥 شحن رصيد يدوي", callback_data="manual_recharge")
        btn14 = types.InlineKeyboardButton("📤 سحب رصيد يدوي", callback_data="manual_withdraw")
        admin_markup.add(btn13, btn14)
        
        # صف 9: تحديث جلسة البوت
        btn15 = types.InlineKeyboardButton("🔄 تحديث جلسة البوت", callback_data="refresh_session")
        admin_markup.add(btn15)
        
        # صف 10: إعدادات شام كاش وسيرياتيل
        btn16 = types.InlineKeyboardButton("💳 اعدادات شام كاش", callback_data="sham_cash")
        btn17 = types.InlineKeyboardButton("📱 إعدادات سيرياتيل", callback_data="syriatel")
        admin_markup.add(btn16, btn17)
        
        # صف 11: إعدادات Binance Pay
        btn18 = types.InlineKeyboardButton("🌍 إعدادات Binance Pay", callback_data="binance")
        admin_markup.add(btn18)
        
        # صف 12: إعدادات طرق الشحن والسحب
        btn19 = types.InlineKeyboardButton("⚙️ إعدادات طرق الشحن والسحب", callback_data="methods_settings")
        admin_markup.add(btn19)

        admin_text = (
            f"🛠 **قائمة الادارة - Dockers** 🛠\n"
            f"==============================\n"
            f"📍 أيدي المجموعة: `{chat_id}`\n"
            f"👤 أيدي المعلم (أبو النور): `{user_id}`\n\n"
            f"اختر العملية المطلوبة من اللوحة أدناه:"
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

# معالجة ضغط الأزرار الإدارية
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data
    # رد ترحيبي عند الضغط على أي زر لضمان الاستجابة الفورية
    bot.answer_callback_query(call.id, f"تم تنفيذ الأمر: {data}")

if __name__ == '__main__':
    keep_alive()
    bot.infinity_polling()
