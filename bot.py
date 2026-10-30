import telebot
from flask import Flask, render_template_string, request, redirect, url_for, session
import threading
from telebot import types

TOKEN = "9021613013:AAH14nGg2KbW7gIhhHz9Y3C3e3l-nxCOGoE"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)
app.secret_key = 'dockers_admin_secret_key_2026'  # مفتاح سري لجلسات الأدمين

# بيانات الدخول الخاصة باللوحة (فيك تعدلها متل ما بدك)
ADMIN_USER = "abounour"
ADMIN_PASS = "dockers2026"

# ----------------- واجهة الويب (Web Panel) -----------------

# الصفحة الرئيسية أو التوجيه لتسجيل الدخول
@app.route('/')
def home():
    if 'logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))

# صفحة تسجيل الدخول للأدمن
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'اسم المستخدم أو كلمة المرور غير صحيحة يا معلم!'
            
    # تصميم بسيط ورايق لصفحة الدخول (Dark Mode مثل اللوحات الفخمة)
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>تسجيل دخول الأدمن - Dockers</title>
        <style>
            body { background-color: #0f172a; color: #f8fafc; font-family: Tahoma, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .login-box { background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); width: 320px; text-align: center; }
            h2 { color: #38bdf8; margin-bottom: 20px; }
            input { width: 100%; padding: 10px; margin: 10px 0; background: #0f172a; border: 1px solid #334155; color: #fff; border-radius: 6px; box-sizing: border-box; }
            button { background: #0284c7; color: white; border: none; padding: 10px; width: 100%; border-radius: 6px; font-weight: bold; cursor: pointer; margin-top: 10px; }
            button:hover { background: #0369a1; }
            .error { color: #f87171; font-size: 14px; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h2>🔐 دخول الأدمن</h2>
            <form method="POST">
                <input type="text" name="username" placeholder="اسم المستخدم (Admin)" required>
                <input type="password" name="password" placeholder="كلمة المرور" required>
                <button type="submit">دخول للوحة التحكم</button>
            </form>
            {% if error %}<div class="error">{{ error }}</div>{% endif %}
        </div>
    </body>
    </html>
    ''', error=error)

# لوحة التحكم الرئيسية (Admin Dashboard)
@app.route('/admin')
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    # تصميم لوحة التحكم الشبيهة باللوحات التجارية
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>لوحة التحكم - Dockers</title>
        <style>
            body { background-color: #0f172a; color: #f8fafc; font-family: Tahoma, sans-serif; margin: 0; display: flex; }
            .sidebar { width: 250px; background: #1e293b; height: 100vh; position: fixed; padding: 20px; box-sizing: border-box; }
            .sidebar h3 { color: #38bdf8; text-align: center; margin-bottom: 30px; }
            .sidebar a { display: block; color: #cbd5e1; text-decoration: none; padding: 10px 15px; margin: 8px 0; border-radius: 6px; transition: 0.3s; }
            .sidebar a:hover, .sidebar a.active { background: #0284c7; color: white; }
            .main-content { margin-right: 250px; padding: 40px; width: calc(100% - 250px); box-sizing: border-box; }
            .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 15px; margin-bottom: 30px; }
            .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; }
            .card { background: #1e293b; padding: 20px; border-radius: 10px; border-right: 4px solid #0284c7; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
            .card h4 { margin: 0 0 10px 0; color: #94a3b8; }
            .card p { font-size: 24px; font-weight: bold; margin: 0; color: #38bdf8; }
            .logout { color: #f87171 !important; margin-top: 50px; }
        </style>
    </head>
    <body>
        <div class="sidebar">
            <h3>⚡ Dockers Admin</h3>
            <a href="#" class="active">🏠 لوحة التحكم</a>
            <a href="#">💰 طلبات الشحن</a>
            <a href="#">🎁 أكواد الهدايا</a>
            <a href="#">👥 المستخدمين</a>
            <a href="#">⚙️ إعدادات البوت</a>
            <a href="/logout" class="logout">🚪 تسجيل الخروج</a>
        </div>
        <div class="main-content">
            <div class="header">
                <h2>أهلاً بك يا معلمي (أبو النور) في لوحة التحكم الإدارية</h2>
                <span>🟢 السيرفر متصل 24/7</span>
            </div>
            <div class="cards">
                <div class="card">
                    <h4>إجمالي المستخدمين</h4>
                    <p>1,240</p>
                </div>
                <div class="card">
                    <h4>الطلبات المعلقة</h4>
                    <p>5</p>
                </div>
                <div class="card">
                    <h4>الأرصدة المشحونة</h4>
                    <p>SYP 450,000</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''')

# تسجيل الخروج
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# ----------------- بوت التيليجرام -----------------

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    chat_type = message.chat.type

    if chat_type in ['group', 'supergroup']:
        admin_markup = types.InlineKeyboardMarkup(row_width=2)
        admin_markup.add(
            types.InlineKeyboardButton("🔄 نشاط لاعب", callback_data="player_activity"),
            types.InlineKeyboardButton("🔍 بحث عن عملية", callback_data="search_op"),
            types.InlineKeyboardButton("📊 إجماليات البوت", callback_data="bot_totals"),
            types.InlineKeyboardButton("⚙️ إعدادات البوت", callback_data="bot_settings")
        )
        bot.send_message(chat_id, f"🛠 **لوحة إدارة Dockers - مجموعة الإدارة**\n📍 أيدي المجموعة: `{chat_id}`", parse_mode="Markdown", reply_markup=admin_markup)
    else:
        bot.send_message(chat_id, f"📊 أهلاً بك! أيدي حسابك: `{user_id}`", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.answer_callback_query(call.id, f"تم تنفيذ الطلب بنجاح: {call.data}")

# تشغيل سيرفر Flask في الخلفية
def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

if __name__ == '__main__':
    keep_alive()
    bot.infinity_polling()
