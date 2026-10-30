import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

# 1. توكن البوت الخاص بك
TOKEN = "9021613013:AAH14nGg2KbW7gIhhHz9Y3C3e31-nxCOGoE"
bot = telebot.TeleBot(TOKEN)

# 2. استبدل هذا الرقم برقم الـ ID الحقيقي الخاص بك كأدمن
ADMIN_ID = 123456789  # <--- حط رقم الـ ID تبعك هون

# --- إعداد قاعدة البيانات المحلية (SQLite) ---
def init_db():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    # جدول لتخزين المستخدمين
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            balance REAL DEFAULT 0.0
        )
    ''')
    # جدول لتخزين إعدادات النصوص والخدمات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    # وضع نص ترحيب افتراضي إذا مش موجود
    cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('welcome_text', 'أهلاً بك في بوت الدوكر والخدمات الرقمية!')")
    conn.commit()
    conn.close()

init_db()

# دوال مساعدة لقاعدة البيانات
def get_setting(key):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else ""

def update_setting(key, value):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

# --- القوائم الرئيسية ---
def main_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("🚀 الخدمات والدوكر", callback_data="services"),
        InlineKeyboardButton("💳 رصيدي والحساب", callback_data="account"),
        InlineKeyboardButton("💬 الدعم الفني", callback_data="support")
    )
    return markup

def admin_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("✏️ تعديل رسالة الترحيب", callback_data="edit_welcome"),
        InlineKeyboardButton("📊 إحصائيات المستخدمين", callback_data="admin_stats"),
        InlineKeyboardButton("📢 إذاعة عامة", callback_data="admin_broadcast"),
        InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_main")
    )
    return markup

# أمر /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    # تسجيل المستخدم بقاعدة البيانات إذا لم يكن موجوداً
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, user_name))
    conn.commit()
    conn.close()
    
    # جلب نص الترحيب المخزن بقاعدة البيانات
    wel_text = get_setting('welcome_text')
    welcome_text = f"أهلاً بك يا {user_name}\n\n{wel_text}"
    
    if user_id == ADMIN_ID:
        markup = main_menu()
        markup.add(InlineKeyboardButton("🔐 لوحة التحكم (للأدمن)", callback_data="admin_panel"))
        bot.send_message(message.chat.id, welcome_text, reply_markup=markup)
    else:
        bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu())

# --- معالجة الأزرار التفاعلية ---
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    user_id = call.from_user.id

    if call.data == "services":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 رجوع", callback_data="back_main"))
        bot.edit_message_text("🚀 قائمة الخدمات المتاحة حالياً:\n- تفعيل حزم الدوكر\n- ربط الحسابات السريعة", chat_id, message_id, reply_markup=markup)

    elif call.data == "account":
        # جلب رصيد المستخدم من قاعدة البيانات
        conn = sqlite3.connect('bot_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        res = cursor.fetchone()
        balance = res[0] if res else 0.0
        conn.close()

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 رجوع", callback_data="back_main"))
        bot.edit_message_text(f"👤 معلومات حسابك:\n- الاسم: {call.from_user.first_name}\n- الـ ID: `{user_id}`\n- الرصيد الحالي: {balance} $", chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "support":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 رجوع", callback_data="back_main"))
        bot.edit_message_text("💬 للتواصل مع الدعم الفني أو شحن الرصيد، يرجى مراسلة الإدارة.", chat_id, message_id, reply_markup=markup)

    # لوحة التحكم للأدمن
    elif call.data == "admin_panel":
        if user_id == ADMIN_ID:
            bot.edit_message_text("👑 **لوحة التحكم الرئيسية للإدارة:**", chat_id, message_id, parse_mode="Markdown", reply_markup=admin_menu())
        else:
            bot.answer_callback_query(call.id, "هذه القائمة مخصصة للمشرفين فقط!", show_alert=True)

    elif call.data == "edit_welcome":
        if user_id == ADMIN_ID:
            msg = bot.send_message(chat_id, "✏️ أرسل النص الجديد لرسالة الترحيب الآن في رسالة منفصلة:")
            bot.register_next_step_handler(msg, save_new_welcome)
        else:
            bot.answer_callback_query(call.id, "غير مسموح!", show_alert=True)

    elif call.data == "admin_stats":
        if user_id == ADMIN_ID:
            conn = sqlite3.connect('bot_database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            conn.close()

            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("🔙 رجوع للوحة التحكم", callback_data="admin_panel"))
            bot.edit_message_text(f"📊 إحصائيات البوت:\n- إجمالي عدد المستخدمين المسجلين: {user_count} مستخدم", chat_id, message_id, reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, "غير مسموح!", show_alert=True)

    elif call.data == "admin_broadcast":
        if user_id == ADMIN_ID:
            msg = bot.send_message(chat_id, "📢 أرسل نص الإذاعة الذي تريد إرساله لجميع المستخدمين:")
            bot.register_next_step_handler(msg, execute_broadcast)
        else:
            bot.answer_callback_query(call.id, "غير مسموح!", show_alert=True)

    elif call.data == "back_main":
        wel_text = get_setting('welcome_text')
        welcome_text = f"القائمة الرئيسية:\n\n{wel_text}"
        if user_id == ADMIN_ID:
            markup = main_menu()
            markup.add(InlineKeyboardButton("🔐 لوحة التحكم (للأدمن)", callback_data="admin_panel"))
            bot.edit_message_text(welcome_text, chat_id, message_id, reply_markup=markup)
        else:
            bot.edit_message_text(welcome_text, chat_id, message_id, reply_markup=main_menu())

# --- دالة حفظ رسالة الترحيب الجديدة عبر الشات ---
def save_new_welcome(message):
    if message.from_user.id != ADMIN_ID:
        return
    new_text = message.text
    update_setting('welcome_text', new_text)
    bot.send_message(message.chat.id, "✅ تمت اَلتحَدِيث وتغيير رسالة الترحيب بنجاح!")

# --- دالة الإذاعة العامة لجميع المستخدمين ---
def execute_broadcast(message):
    if message.from_user.id != ADMIN_ID:
        return
    broadcast_text = message.text
    
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    all_users = cursor.fetchall()
    conn.close()

    success = 0
    fail = 0
    for row in all_users:
        u_id = row[0]
        try:
            bot.send_message(u_id, f"📢 **إشعار من الإدارة:**\n\n{broadcast_text}", parse_mode="Markdown")
            success += 1
        except Exception:
            fail += 1

    bot.send_message(message.chat.id, f"📊 **نتيجة الإذاعة:**\n- تم الإرسال بنجاح: {success}\n- فشل الإرسال (حظروا البوت): {fail}")

# تشغيل البوت
bot.infinity_polling()
