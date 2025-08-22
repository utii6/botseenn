import json
import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# تحميل الإعدادات
with open("config.json", "r") as f:
    config = json.load(f)

BOT_TOKEN = config["BOT_TOKEN"]
API_KEY = config["API_KEY"]
ADMIN_ID = config["ADMIN_ID"]
SERVICE_ID = config["SERVICE_ID"]

# لتخزين بيانات الطلب
pending_orders = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("😂🚫 @E2E12 هذا البوت خاص بالمدير فقط!")

    keyboard = [
        [InlineKeyboardButton("📈 طلب مشاهدات تيليجرام", callback_data="order_views")]
    ]
    await update.message.reply_text(
        "👋😂 أهلاً بك عزيزي المدير\nاختر الخدمة التي تريد تنفيذها:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# عند الضغط على زر طلب المشاهدات
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "order_views":
        pending_orders[query.from_user.id] = {"step": "await_link"}
        await query.message.reply_text("📌 😂أرسل الآن رابط المنشور الذي تريد زيادة المشاهدات له:")

# استقبال الرسائل (الرابط أو العدد)
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
            await update.message.reply_text("✅😂 تم استلام الرابط\n\n📌 الآن أرسل عدد المشاهدات المطلوب:")

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
                        f"✅😂 تم تنفيذ الطلب بنجاح\n\n📌 رقم الطلب: {order_id}\n🔗 الرابط: {link}\n📊 الكمية: {quantity}"
                    )
                else:
                    await update.message.reply_text(f"⚠️ حدث خطأ: {response}")

            except ValueError:
                await update.message.reply_text("🚫 أرسل عدد صحيح من المشاهدات.")
            
            pending_orders.pop(user_id, None)

# تشغيل البوت
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
