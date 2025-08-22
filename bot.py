import requests
import telegram
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# ---- إعدادات البوت ----
BOT_TOKEN = "8388967054:AAG0zsdXGrsjTXDTZ37OcjdMGbJc7UWlRfM"
API_KEY = "81db6d6480686d9da6f35ff2cf6a30b4"
ADMIN_ID = 5581457665
SERVICE_ID = 14527

# رابط الخدمة على Render
RENDER_URL = "https://botseenn.onrender.com"

# ---- إنشاء التطبيق ----
app = FastAPI()
application = Application.builder().token(BOT_TOKEN).build()

# لتخزين بيانات الطلب
pending_orders = {}

# ---- /start ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("🚫😂 هذا البوت خاص بالمدير  @E2E12 !")

    keyboard = [
        [InlineKeyboardButton("📈😂 طلب مشاهدات تيليجرام", callback_data="order_views")]
    ]
    await update.message.reply_text(
        "👋😂! أهلاً بك قاسـم نجمه البوت بوتك\nاختر الخدمه 😂ا:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ---- زر طلب الخدمة ----
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "order_views":
        pending_orders[query.from_user.id] = {"step": "await_link"}
        await query.message.reply_text("📌😂!أرسل رابـط منشـورك:")

# ---- استقبال الرسائل ----
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    if user_id in pending_orders:
        step = pending_orders[user_id].get("step")

        # استلام الرابط
        if step == "await_link":
            pending_orders[user_id]["link"] = update.message.text
            pending_orders[user_id]["step"] = "await_quantity"
            await update.message.reply_text("✅😂. تم استلام الرابط\n\n📌😂! الآن أرسل عدد المشاهدات المطلوب:")

        # استلام العدد وتنفيذ الطلب
        elif step == "await_quantity":
            try:
                quantity = int(update.message.text)
                link = pending_orders[user_id]["link"]

                # إرسال الطلب لـ kd1s
                response = requests.post("https://kd1s.com/api/v2", data={
                    "key": API_KEY,
                    "action": "add",
                    "service": SERVICE_ID,
                    "link": link,
                    "quantity": quantity
                }).json()

                if "order" in response:
                    order_id = response["order"]
                    await update.message.reply_text(
                        f"✅😂 تم تنفيذ الطلب بنجاح\n\n📌▶️ رقم الطلب: {order_id}\n🔗 الرابط: {link}\n📊 الكمية: {quantity}"
                    )
                else:
                    await update.message.reply_text(f"⚠️😂 حدث خطأ: {response}")

            except ValueError:
                await update.message.reply_text("🚫😂 أرسل عدد صحيح من المشاهدات.")
            
            pending_orders.pop(user_id, None)

# ---- إضافة Handlers ----
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_handler))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# ---- مسار Webhook ----
@app.post(f"/webhook/{BOT_TOKEN}")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return {"ok": True}

# ---- عند بدء التشغيل ----
@app.on_event("startup")
async def startup():
    webhook_url = f"{RENDER_URL}/webhook/{BOT_TOKEN}"
    await application.bot.set_webhook(webhook_url)
    await application.initialize()
    await application.start()

# ---- عند الإيقاف ----
@app.on_event("shutdown")
async def shutdown():
    await application.stop()
    await application.shutdown()
