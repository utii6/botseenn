import json
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ===== إعدادات البوت =====
TOKEN = "YOUR_BOT_TOKEN"
bot = Bot(token=TOKEN)

# ===== ملف المستخدمين =====
USERS_FILE = "users.json"

def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {"allowed": [], "banned": []}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def add_user(user_id):
    users = load_users()
    if user_id not in users["allowed"]:
        users["allowed"].append(user_id)
    if user_id in users["banned"]:
        users["banned"].remove(user_id)
    save_users(users)

def ban_user(user_id):
    users = load_users()
    if user_id not in users["banned"]:
        users["banned"].append(user_id)
    if user_id in users["allowed"]:
        users["allowed"].remove(user_id)
    save_users(users)

def is_allowed(user_id):
    users = load_users()
    return user_id in users["allowed"]

def is_banned(user_id):
    users = load_users()
    return user_id in users["banned"]

# ===== قائمة الخدمات =====
services = {
    "13021": "مشاهدات تيك توك رخيصة 😎",
    "13400": "مشاهدات انستا رخيصة 🅰️",
    "14527": "مشاهدات تلي ✅",
    "15644": "لايكات تيك توك جودة عالية 💎",
    "14676": "لايكات انستا سريعة وقوية 😎👍"
}

# ===== أوامر البوت =====
ADMIN_ID = 5581457665  # معرفك للتحكم بالمستخدمين

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if is_banned(user_id):
        await update.message.reply_text("❌😂 تم حظرك من استخدام البوت")
        return

    if not is_allowed(user_id):
        await update.message.reply_text("⚠️ راسل @E2E12 لفتح الحظر العام أنت غير مسموح لك بالوصول")
        return

    # عرض الخدمات
    keyboard = [[InlineKeyboardButton(name, callback_data=service_id)] for service_id, name in services.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("😂اختر الخدمة:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    service_id = query.data
    service_name = services.get(service_id, "💔خدمة غير معروفة")
    await query.message.reply_text(f"😎تم اختيار الخدمة: {service_name}\n🔹 هنا يمكنك إضافة كود تنفيذ الطلب عبر API")

# ===== أوامر الإدارة =====
async def add_user_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    try:
        user_id = int(context.args[0])
        add_user(user_id)
        await update.message.reply_text(f"💁✅ تم إضافة المستخدم: {user_id}")
    except:
        await update.message.reply_text("▶️استخدام: /add_user <user_id>")

async def ban_user_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    try:
        user_id = int(context.args[0])
        ban_user(user_id)
        await update.message.reply_text(f"❌😂 تم حظر المستخدم: {user_id}")
    except:
        await update.message.reply_text("▶️استخدام: /ban_user <user_id>")

# ===== تشغيل البوت =====
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(CommandHandler("add_user", add_user_cmd))
app.add_handler(CommandHandler("ban_user", ban_user_cmd))

print("Bot is running...")
app.run_polling()
