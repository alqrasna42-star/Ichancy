import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# توكن البوت الخاص بك الصحيح
TOKEN = "9021613013:AAH14nGg2KbW7gIhhHz9Y3C3e31-nxCOGoE"

# قاعدة بيانات وهمية لتجربة الرصيد (في الواقع يفضل ربطها بـ SQLite أو PostgreSQL)
USER_DATA = {}

def get_user(user_id, username):
    if user_id not in USER_DATA:
        USER_DATA[user_id] = {
            "balance": 0,
            "username": username or "مستخدم",
            "referred_by": None,
            "referrals": 0
        }
    return USER_DATA[user_id]

# أمر البدء /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = get_user(user.id, user.username)
    
    # التحقق من رابط الإحالة
    if context.args and context.args[0].isdigit():
        referrer_id = int(context.args[0])
        if referrer_id != user.id and not db_user["referred_by"]:
            db_user["referred_by"] = referrer_id
            if referrer_id in USER_DATA:
                USER_DATA[referrer_id]["referrals"] += 1
                USER_DATA[referrer_id]["balance"] += 500  # هدية الإحالة كمثال

    text = (
        f"👋 أهلاً بك {user.first_name} في بوت الشحن والخدمات المالي الآلي!\n\n"
        f"💳 <b>رصيدك الحالي:</b> {db_user['balance']} ليرة / نقطة\n"
        f"👥 <b>عدد الإحالات:</b> {db_user['referrals']}\n\n"
        "الرجاء اختيار أحد الخيارات من القائمة أدناه لقضاء خدماتك تلقائياً:"
    )
    
    keyboard = [
        [InlineKeyboardButton("📥 شحن الرصيد (إيداع)", callback_data="deposit")],
        [InlineKeyboardButton("📤 سحب الأرباح", callback_data="withdraw")],
        [InlineKeyboardButton("🔗 رابط الإحالة الخاص بي", callback_data="referral")],
        [InlineKeyboardButton("📞 الدعم الفني والاستفسارات", callback_data="support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="HTML")

# معالج الأزرار التفاعلية
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    db_user = get_user(user_id, query.from_user.username)
    
    if query.data == "deposit":
        text = (
            "💰 <b>قسم شحن الرصيد التلقائي:</b>\n\n"
            "الرجاء اختيار وسيلة الدفع المناسبة لك لإرسال الأموال:\n"
            "1️⃣ <b>سيريتل كاش / شام كاش</b>\n"
            "2️⃣ <b>MTN كاش</b>\n"
            "3️⃣ <b>USDT (TRC20)</b>\n\n"
            "⚠️ بعد تحويل المبلغ، أرسل إشعار التحويل أو رقم المعاملة للدعم لتأكيد الشحن فوراً."
        )
        keyboard = [[InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="main_menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
        
    elif query.data == "withdraw":
        text = (
            "💸 <b>قسم سحب الأرباح والرصيد:</b>\n\n"
            f"رصيدك المتاح للسحب هو: {db_user['balance']} ليرة.\n"
            "⚠️ الحد الأدنى للسحب هو 5000 ليرة.\n\n"
            "اضغط على الدعم الفني لإرسال بيانات محفظتك وقيمة المبلغ المراد سحبه."
        )
        keyboard = [[InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="main_menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "referral":
        bot_username = context.bot.username
        ref_link = f"https://t.me/{bot_username}?start={user_id}"
        text = (
            "👥 <b>نظام الإحالة وكسب الأرباح:</b>\n\n"
            "قم بنسخ الرابط أدناه وإرساله لأصدقائك. ستحصل على مكافأة مالية فورية داخل البوت عن كل شخص يقوم بالتسجيل والشحن من خلالك!\n\n"
            f"🔗 <code>{ref_link}</code>"
        )
        keyboard = [[InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="main_menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "support":
        text = "📞 للتواصل المباشر مع إدارة البوت أو تقديم شكاوى وإرسال فواتير الشحن، يرجى مراسلة الحساب: @Your_Support_Handle"
        keyboard = [[InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="main_menu")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "main_menu":
        # إعادة إظهار القائمة الرئيسية
        text = (
            f"💳 <b>رصيدك الحالي:</b> {db_user['balance']} ليرة / نقطة\n"
            f"👥 <b>عدد الإحالات:</b> {db_user['referrals']}\n\n"
            "الرجاء اختيار أحد الخيارات من القائمة أدناه:"
        )
        keyboard = [
            [InlineKeyboardButton("📥 شحن الرصيد (إيداع)", callback_data="deposit")],
            [InlineKeyboardButton("📤 سحب الأرباح", callback_data="withdraw")],
            [InlineKeyboardButton("🔗 رابط الإحالة الخاص بي", callback_data="referral")],
            [InlineKeyboardButton("📞 الدعم الفني والاستفسارات", callback_data="support")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

def main():
    # بناء التطبيق وتمرير التوكن
    application = Application.builder().token(TOKEN).build()

    # إضافة الأوامر والمستمعين
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # تشغيل البوت بنظام التحديث المستمر
    application.run_polling()

if __name__ == "__main__":
    main()
