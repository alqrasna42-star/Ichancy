import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 1. التوكن الخاص ببوتك
TOKEN = "9021613013:AAH14nGg2KbW7gIhhHz9Y3C3e31-nxCOGoE"
bot = telebot.TeleBot(TOKEN)

# 2. حط الـ ID تبعك هون (لتفوت على لوحة التحكم) - حط رقم الـ ID الحقيقي لك كأدمن
ADMIN_ID = 123456789  # استبدل هذا الرقم برقم حسابك الحقيقي على تلغرام

# --- القائمة الرئيسية للزبائن ---
def main_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("🚀 الخدمات والدوكر", callback_data="services"),
        InlineKeyboardButton("💳 طرق الشحن", callback_data="recharge"),
        InlineKeyboardButton("💬 الدعم الفني", callback_data="support"),
        InlineKeyboardButton("ℹ️ معلومات الحساب", callback_data="account")
    )
    return markup

# --- لوحة تحكم الأدمن ---
def admin_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("📢 إذاعة للمستخدمين", callback_data="admin_broadcast"),
        InlineKeyboardButton("📊 الإحصائيات", callback_data="admin_stats"),
        InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_main")
    )
    return markup

# أمر /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    welcome_text = f"أهلاً بك يا {user_name} في بوت الدوكر والخدمات!\nيرجى اختيار ما تحتاجه من القائمة أدناه:"
    
    # إذا كان المستخدم هو الأدمن، نظهر له زر لوحة التحكم
    if user_id == ADMIN_ID:
        markup = main_menu()
        markup.add(InlineKeyboardButton("🔐 لوحة التحكم (للأدمن)", callback_data="admin_panel"))
        bot.
