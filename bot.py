import json
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# -------------------------
# تحميل الإعدادات
# -------------------------
with open("config.json", "r") as f:
    config = json.load(f)

BOT_TOKEN = config["bot_token"]
API_KEY = config["api_key"]
ADMIN_ID = config["admin_id"]
DEFAULT_CHANNEL = config["default_channel"]
DEFAULT_VIEWS = config["default_views"]
API_URL = config.get("api_url", "https://kd1s.com/api/increase_views")

# -------------------------
# تخزين المستخدمين
# -------------------------
try:
    with open("users.json", "r") as f:
        users = json.load(f)
except:
    users = []

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f)

# -------------------------
# دوال البوت
# -------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    # السماح فقط للمدير بالاستخدام
    if user_id != ADMIN_ID:
        await update.message.reply_text("⚠️😂 هذا البوت يعمل فقط مع المدير.")
        return

    # رسالة ترحيب شخصية
    await update.message.reply_text(
        f"أهلاً وسهلاً أخي الكريم {user.full_name} في البوت، سيساعدك كثيرًا في زيادة المشاهدات!"
    )

    # إضافة المستخدم لقائمة المستخدمين إذا جديد
    if user_id not in users:
        users.append(user_id)
        save_users()

        # إشعار للمدير
        msg = f""" دخول شخص جديد إلى البوت الخاص بك 😎
-----------------------
• معلومات النفـرر الجديد :
• الاسم😂: {user.full_name}
• معرف↗️: @{user.username if user.username else 'لا يوجد'}
• الايدي🆔: {user.id}
-----------------------
• 😂عدد الأعضاء الكلي: {len(users)}
"""
        await context.bot.send_message(chat_id=ADMIN_ID, text=msg)

    # أزرار شفافة
    keyboard = [
        [InlineKeyboardButton("🔼😂 زيادة تلقائية", callback_data='auto')],
        [InlineKeyboardButton("✍️☪️ زيادة يدوية", callback_data='manual')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👍اختر الي يعجبـك:",
        reply_markup=reply_markup
    )

# -------------------------
# زيادة تلقائية
# -------------------------
async def auto_views(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = {
        "api_key": API_KEY,
        "channel": DEFAULT_CHANNEL,
        "views": DEFAULT_VIEWS
    }
    try:
        r = requests.post(API_URL, data=data)
        if r.status_code == 200:
            await update.message.reply_text(f"😂تم زيادة {DEFAULT_VIEWS} مشاهدة للمنشورات في {DEFAULT_CHANNEL}")
        else:
            await update.message.reply_text(f"❌ فشل في زيادة المشاهدات. كود الخطأ: {r.status_code}")
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ: {e}")

# -------------------------
# التعامل مع الأزرار
# -------------------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'auto':
        await auto_views(update, context)

    elif query.data == 'manual':
        # الرسالة الأولى: رابط المنشور
        await query.edit_message_text("✍️😂 يلا قاسـم أرسل رابط منشورك  :")
        # حفظ حالة المستخدم ليعرف أنه في وضع الزيادة اليدوية
        context.user_data['manual_step'] = 1

# -------------------------
# زيادة يدوية بالتتابع (رابط ثم عدد المشاهدات)
# -------------------------
async def manual_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return  # فقط المدير يمكنه استخدام البوت

    if 'manual_step' in context.user_data:
        step = context.user_data['manual_step']

        if step == 1:
            # حفظ رابط المنشور
            context.user_data['manual_link'] = update.message.text
            await update.message.reply_text("✍️😂 الآن أرسل عدد المشاهدات :")
            context.user_data['manual_step'] = 2

        elif step == 2:
            try:
                views = int(update.message.text)
                link = context.user_data.get('manual_link', '')
                # استدعاء API لزيادة المشاهدات
                data = {
                    "api_key": API_KEY,
                    "channel": link,
                    "views": views
                }
                r = requests.post(API_URL, data=data)
                if r.status_code == 200:
                    await update.message.reply_text(f"😂تم زيادة {views} مشاهدة للمنشور {link}")
                else:
                    await update.message.reply_text(f"❌ فشل في زيادة المشاهدات. كود الخطأ: {r.status_code}")
            except:
                await update.message.reply_text("❌ خطأ: يرجى إدخال  رابـط للمشاهدات.")

            # إزالة حالة المستخدم بعد الانتهاء
            context.user_data.pop('manual_step', None)
            context.user_data.pop('manual_link', None)

# -------------------------
# إعداد البوت وتشغيله
# -------------------------
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("auto", auto_views))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manual_input))

# تشغيل البوت
app.run_polling()
