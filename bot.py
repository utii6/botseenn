import json
import requests
from telethon import TelegramClient, events
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# تحميل الإعدادات
with open("config.json", "r") as f:
    config = json.load(f)

BOT_TOKEN = config["8388967054:AAG0zsdXGrsjTXDTZ37OcjdMGbJc7UWlRfM"]
API_KEY = config["81db6d6480686d9da6f35ff2cf6a30b4"]
ADMIN_ID = config["5581457665"]
DEFAULT_CHANNEL = config["qd3qd"]
DEFAULT_VIEWS = config["600"]

# -------------------------
# TELEGRAM BOT PART
# -------------------------
app = ApplicationBuilder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        await update.message.reply_text(
            "أهلاً! هذا البوت جاهز لزيادة مشاهدات قناتك😂.\n\n"
            "استخدم:\n"
            "/auto - 😂زيادة تلقائية لمشاهدات القناة\n"
            "/manual <القناة> <رقم المنشور> <عدد المشاهدات> - لزيادة يدويًا"
        )
    else:
        await update.message.reply_text("⚠️ 😂أنت غير مخول لاستخدام هذا البوت.")

async def auto_views(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # إرسال طلب زيادة المشاهدات تلقائيًا للقناة الافتراضية😂
    data = {
        "api_key": API_KEY,
        "channel": DEFAULT_CHANNEL,
        "views": DEFAULT_VIEWS
    }
    r = requests.post("https://example.com/api/increase_views", data=data)
    if r.status_code == 200:
        await update.message.reply_text(f"تم زيادة {DEFAULT_VIEWS} 😂مشاهدة للمنشورات في {DEFAULT_CHANNEL}")
    else:
        await update.message.reply_text("❌ ❗️فشل في زيادة المشاهدات.")

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
        r = requests.post("https://example.com/api/increase_views", data=data)
        if r.status_code == 200:
            await update.message.reply_text(f"تم زيادة {views} مشاهدة للمنشور {post_id} في {channel}")
        else:
            await update.message.reply_text("❌ 💰فشل في زيادة المشاهدات.")
    except:
        await update.message.reply_text("❌ الخطأ: استخدم الصيغة الصحيحة:\n/manual <القناة> <رقم المنشور> <عدد المشاهدات>")

# إضافة الأوامر للبوت
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("auto", auto_views))
app.add_handler(CommandHandler("manual", manual_views))

# تشغيل البوت
app.run_polling()
