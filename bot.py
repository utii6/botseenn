import json
from fastapi import FastAPI, Request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.error import BadRequest

# ===== إعدادات البوت =====
TOKEN = "8388967054:AAG0zsdXGrsjTXDTZ37OcjdMGbJc7UWlRfM"
bot = Bot(token=TOKEN)

# ===== معلومات القناة =====
CHANNEL_USERNAME = "@qd3QD"

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
    "13372": "مشاهدات تيك توك رخيصة 😎",
    "13400": "مشاهدات انستا رخيصة 🅰️",
    "14527": "مشاهدات تلي ✅",
    "15007": "لايكات تيك توك جودة عالية 💎",
    "14676": "لايكات انستا سريعة وقوية 😎👍"
}

# ===== إعدادات المدير =====
ADMIN_ID = 5581457665  # ضع هنا معرفك

# ===== فحص الاشتراك بالقناة =====
async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ['member', 'creator', 'administrator']
    except BadRequest:
        return False

# ===== أوامر البوت =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    # رسالة ترحيب للمدير
    if user_id == ADMIN_ID:
        await update.message.reply_text(f"👑😂 أهلاً بك يا المدير، البوت بوتك {user.first_name}")

    # تحقق الحظر
    if is_banned(user_id):
        await update.message.reply_text("😂❌ تم حظرك من استخدام البوت")
        return

    # تحقق السماح
    if not is_allowed(user_id):
        await update.message.reply_text("⚠️❗️ أنت غير مسموح لك بالوصول راسل @E2E12")
        return

    # تحقق الاشتراك الإجباري
    subscribed = await check_subscription(user_id)
    if not subscribed:
        await update.message.reply_text(
            f"⚠️ اسف حبيبي، اشترك بالقناة أولاً: {CHANNEL_USERNAME}\n"
            "بعد الاشتراك اضغط /start مرة أخرى"
        )
        return

    # رسالة ترحيب للمستخدم العادي
    await update.message.reply_text(f"أهلاً وسهلاً {user.first_name} في بوت قاسـم نجمهه 😂✨")

    # عرض الخدمات
    keyboard = [[InlineKeyboardButton(name, callback_data=service_id)] for service_id, name in services.items()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("😂 اختر الخدمة:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    service_id = query.data
    service_name = services.get(service_id, "💔❗️خدمة غير معروفة")
    await query.message.reply_text(f"😂 تم اختيار الخدمة: {service_name}\n🔹 هنا يمكنك إضافة كود تنفيذ الطلب عبر API")

# ===== أوامر الإدارة =====
async def add_user_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    try:
        user_id = int(context.args[0])
        add_user(user_id)
        await update.message.reply_text(f"✅😂 تم إضافة المستخدم: {user_id}")
    except:
        await update.message.reply_text("❗️استخدام: /add_user <user_id>")

async def ban_user_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    try:
        user_id = int(context.args[0])
        ban_user(user_id)
        await update.message.reply_text(f"❌😂 تم حظر المستخدم: {user_id}")
    except:
        await update.message.reply_text("❗️استخدام: /ban_user <user_id>")

# ===== Telegram Application =====
telegram_app = ApplicationBuilder().token(TOKEN).build()
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CallbackQueryHandler(button))
telegram_app.add_handler(CommandHandler("add_user", add_user_cmd))
telegram_app.add_handler(CommandHandler("ban_user", ban_user_cmd))

# ===== FastAPI App =====
app = FastAPI()

@app.post(f"/webhook/{TOKEN}")
async def webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot)
    await telegram_app.process_update(update)

# ===== تشغيل محلي (اختياري) =====
if __name__ == "__main__":
    print("Bot is running locally...")
    telegram_app.run_polling()
