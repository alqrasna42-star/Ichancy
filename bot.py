import telebot
from telebot import types

# توكن البوت الخاص بك
TOKEN = '9021613013:AAH14nGg2KbW7gIhhHz9Y3C3e31-nxCOGoE'
bot = telebot.TeleBot(TOKEN, parse_mode='Markdown')

# رابط منصة ايشاني الرسمي
ICHANCY_URL = 'https://www.ichancy.com'

# --- أمر الـ Start والقائمة الرئيسية ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    balance = 0.0
    ichancy_acc = 'غير مسجل'

    # لوحة المفاتيح والأزرار
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn_deposit = types.InlineKeyboardButton('شحن رصيد 🔴', callback_data='deposit')
    btn_withdraw = types.InlineKeyboardButton('سحب رصيد 🟩', callback_data='withdraw')
    btn_ref = types.InlineKeyboardButton('نظام الاحالات 🟡', callback_data='referral')
    btn_gift_send = types.InlineKeyboardButton('اهدِاء رصيد 🎁', callback_data='gift_send')
    btn_gift_code = types.InlineKeyboardButton('كود هدية 🎁', callback_data='gift_code')
    btn_support = types.InlineKeyboardButton('للتواصل فريق الدعم 🔴', callback_data='support')
    btn_tech = types.InlineKeyboardButton('مشكلة تقنية 🔵', callback_data='tech_issue')
    btn_history = types.InlineKeyboardButton('السجل 💕', callback_data='history')
    btn_guide = types.InlineKeyboardButton('كيفية الاستخدام 🟦', callback_data='guide')
    btn_rules = types.InlineKeyboardButton('شروط الاستخدام 🔴', callback_data='rules')
    btn_wheel = types.InlineKeyboardButton('عجلة الحظ 🎡', callback_data='wheel')
    btn_jackpot = types.InlineKeyboardButton('الجاكبوت 💰', callback_data='jackpot')
    
    # زر رابط ايشاني المباشر
    btn_ichancy = types.InlineKeyboardButton('حساب ايشاني وشحنه ⚡', callback_data='ichancy_account_manage')

    markup.add(btn_deposit, btn_withdraw)
    markup.add(btn_ref)
    markup.add(btn_gift_send, btn_gift_code)
    markup.add(btn_support, btn_tech)
    markup.add(btn_history, btn_guide)
    markup.add(btn_rules)
    markup.add(btn_wheel, btn_jackpot)
    markup.add(btn_ichancy)

    text = (
        f"📊 **قائمة الخيارات الرئيسية**\n\n"
        f"💰 **الرصيد الحالي:** {balance} SYP\n"
        f"🆔 **أيدي حسابك:** `{user_id}`\n"
        f"⚡ **حساب ايشاني:** {ichancy_acc}\n"
    )
    
    bot.send_message(message.chat.id, text, reply_markup=markup)

# --- معالجة الضغط على الأزرار ---
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    user_id = call.from_user.id
    
    if call.data == 'deposit':
        bot.answer_callback_query(call.id)
        bot.send_message(user_id, "🔴 لإتمام عملية شحن الرصيد، يرجى التواصل مع الإدارة أو تحويل المبلغ وإرسال الإيصال هنا.")
        
    elif call.data == 'withdraw':
        bot.answer_callback_query(call.id)
        bot.send_message(user_id, "🟩 يرجى إرسال المبلغ المراد سحبه ومعلومات الحساب الخاص بك.")
        
    elif call.data == 'ichancy_account_manage':
        bot.answer_callback_query(call.id)
        # إرسال رسالة تحتوي على رابط المنصة الرسمي مع تفاصيل الحساب
        msg_text = (
            f"⚡ **إدارة حساب ايشاني الخاص بك**\n\n"
            f"🌐 يمكنك زيارة الموقع الرسمي للمنصة عبر الرابط التالي:\n"
            f"[منصة ايشاني الرسمية]({ICHANCY_URL})\n\n"
            f"🆔 أيدي الحساب المرتبط: `{user_id}`\n"
            f"لإتمام عمليات الشحن أو السحب، يرجى التواصل مع الكاشير أو الإدارة."
        )
        # زر تفاعلي يفتح الرابط مباشرة
        url_markup = types.InlineKeyboardMarkup()
        url_markup.add(types.InlineKeyboardButton("🔗 فتح موقع ايشاني", url=ICHANCY_URL))
        
        bot.send_message(user_id, msg_text, reply_markup=url_markup)

    elif call.data == 'support':
        bot.answer_callback_query(call.id)
        bot.send_message(user_id, "📞 للتواصل مع فريق الدعم الفني، اكتب رسالتك وسيتم تحويلها للإدارة مباشرة.")
        
    else:
        bot.answer_callback_query(call.id, "هذا الزر قيد الخدمة والتحديث.")

# تشغيل البوت بثبات
if __name__ == '__main__':
    print("Bot is running smoothly with Ichancy link...")
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"Error: {e}")

