# Telegram Views Bot (kd1s)

بوت خاص بالمدير فقط لزيادة مشاهدات منشورات تيليجرام عبر موقع [kd1s.com](https://kd1s.com)  
مبني باستخدام **python-telegram-bot + FastAPI** ومهيأ للعمل على Render.

---

## 📂 الملفات
- `bot.py` : الكود الرئيسي للبوت (يدعم Webhook + FastAPI)
- `config.json` : الإعدادات (التوكن، API Key، ID المدير، ID الخدمة)
- `requirements.txt` : المكتبات المطلوبة
- `Procfile` : ملف تشغيل Render
- `README.md` : ملف الشرح

---

## ⚙️ الإعدادات (config.json)
```json
{
  "BOT_TOKEN": "8388967054:AAG0zsdXGrsjTXDTZ37OcjdMGbJc7UWlRfM",
  "API_KEY": "5be3e6f7ef37395377151dba9cdbd552",
  "ADMIN_ID": 5581457665,
  "SERVICE_ID": 14527
}
