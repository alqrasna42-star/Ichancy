import telebot
from telebot import types

# توكن البوت الخاص بك المعتمد حالياً
TOKEN = "9021613013:AAH14nGg2KbW7gIhhHz9Y3C3e31-nxCOGoE"
# أيدي مجموعة أو قناة الإدارة (إذا لم تحدده بعد، سيقوم البوت بقبوله أو يمكنك وضعه هنا لاحقاً)
ADMIN_CHAT_ID = None 

bot = telebot.TeleBot(TOKEN)

# 1. قائمة المستخدم العادي (تظهر بالخاص)
def get_user_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🔴 شحن رصيد", callback_data="user_charge"),
        types.InlineKeyboardButton("🟢 سحب رصيد", callback_data="user_withdraw")
    )
    markup.add(types.InlineKeyboardButton("🟡 نظام الاحالات", callback_data="user_ref"))
    markup.add(
        types.InlineKeyboardButton("🎁 اهداء رصيد", callback_data="user_gift"),
        types.InlineKeyboardButton("🎁 كود هدية", callback_data="user_code")
    )
    markup.add(
        types.InlineKeyboardButton("🔴 لتواصل فريق الدعم", callback_data="user_support"),
        types.InlineKeyboardButton("🔵 مشكلة تقنية", callback_data="user_tech")
    )
    markup.add(
        types.InlineKeyboardButton("💖 السجل", callback_data="user_history"),
        types.InlineKeyboardButton("🔵 كيفية الاستخدام", callback_data="user_help")
    )
    markup.add(types.InlineKeyboardButton("🔴 شروط الاستخدام", callback_data="user_terms"))
    markup.add(
        types.InlineKeyboardButton("🎡 عجلة الحظ", callback_data="user_wheel"),
        types.InlineKeyboardButton("💰 الجاكبوت", callback_data="user_jackpot")
    )
    markup.add(types.InlineKeyboardButton("⚡ حساب ايشاني وشحنه", callback_data="user_ichancy"))
    return markup

# 2. لوحة تحكم الأدمن الكاملة (تظهر في مجموعة الإدارة أو عند الأدمن)
def get_admin_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 إحصائيات البوت", callback_data="admin_stats"),
        types.InlineKeyboardButton("👥 إدارة المستخدمين", callback_data="admin_users")
    )
    markup.add(
        types.InlineKeyboardButton("⚙️ ضبط الأرصدة والأسعار", callback_data="admin_settings"),
        types.InlineKeyboardButton("📢 إرسال رسالة للجميع", callback_data="admin_broadcast")
    )
    markup.add(types.InlineKeyboardButton("🔄 تحديث لوحة التحكم", callback_data="admin_refresh"))
    return markup

# التعامل مع أمر /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    chat_type = message.chat.type
    
    # إذا كانت الرسالة واردة من مجموعة أو قناة (مجموعة الإدارة)
    if chat_type in ['group', 'supergroup']:
        admin_text = (
            "🛠 **لوحة إدارة بوت Dockers - الإعدادات الكاملة**\n"
            "==============================\n"
            f"📍 أيدي هذه المجموعة: `{chat_id}`\n"
            "مرحباً بك يا معلمي في لوحة التحكم الإدارية."
        )
        bot.send_message(chat_id, admin_text, reply_markup=get_admin_keyboard(), parse_mode="Markdown")
    else:
        # عرض القائمة العادية للعميل في المحادثة الخاصة
        user_text = (
            "📊 **قائمة الخيارات الرئيسية**\n\n"
            f"💰 الرصيد الحالي: SYP 0.0\n"
            f"🆔 أيدي حسابك: {user_id}\n"
            f"⚡ حساب ايشاني: غير مسجل"
        )
        bot.send_message(chat_id, user_text, reply_markup=get_user_keyboard(), parse_mode="Markdown")

# معالجة الضغط على الأزرار
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
