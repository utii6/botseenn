import json
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# تحميل الإعدادات
with open("config.json", "r") as f:
    config = json.load(f)

BOT_TOKEN = config["bot_token"]
API_KEY = config["api_key"]
ADMIN_ID = config["admin_id"]
DEFAULT_CHANNEL = config["default_channel"]
DEFAULT_VIEWS = config["default_views"]

# -------------------------
# TELEGRAM BOT PART
# -------------------------
app = ApplicationBuilder().token(BOT_TOKEN).build()

# رسالة ترحيب
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        await update.message.reply_text(
            "😂أهلاً! هذا البوت جاهز لزيادة مشاهدات قناتك.\n\n"
            "الأوامر:\n"
            "/auto - 😂زيادة تلقائية لمشاهدات القناة\n"
            "/manual <القناة> <رقم المنشور> <عدد المشاهدات> - لزيادة يدويًا"
        )
    else:
        await update.message.reply_text("⚠️💰 أنت غير مخول لاستخدام هذا البوت.")

# زيادة تلقائية لمشاهدات القناة الافتراضية
async def auto_views(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = {
        "api_key": API_KEY,
        "channel": DEFAULT_CHANNEL,
        "views": DEFAULT_VIEWS
    }
    try:
        r = requests.post("https://kd1s.com/api/increase_views", data=data)
        if r.status_code == 200:
            await update.message.reply_text(f"😂تم زيادة {DEFAULT_VIEWS} مشاهدة للمنشورات في {DEFAULT_CHANNEL}")
        else:
            await update.message.reply_text(f"💔❌ فشل في زيادة المشاهدات. كود الخطأ: {r.status_code}")
    except Exception as e:
        await update.message.reply_text(f"❌❗️ خطأ: {e}")

# زيادة يدويًا لأي منشور
async def manual_views(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        channel = args[0]
        post_id = args[1]
        views = int(args[2])
        data = {
            "api_key": API_KEY,
            "channel": channel,
            "post_id": post_id,
            "views": views
        }
        r = requests.post("https://kd1s.com/api/increase_views", data=data)
        if r.status_code == 200:
            await update.message.reply_text(f"😂تم زيادة {views} مشاهدة للمنشور {post_id} في {channel}")
        else:
            await update.message.reply_text(f"❌💁 فشل في زيادة المشاهدات. كود الخطأ: {r.status_code}")
    except:
        await update.message.reply_text("❌❗️ الخطأ: استخدم الصيغة الصحيحة:\n/manual <القناة> <رقم المنشور> <عدد المشاهدات>")

# إضافة الأوامر للبوت
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("auto", auto_views))
app.add_handler(CommandHandler("manual", manual_views))

# تشغيل البوت
app.run_polling()
