# 🏦 مدیریت هوشمند هزینه‌ها

سیستم تحلیل پیامک‌های بانکی و مدیریت هوشمند هزینه‌ها

## ✨ ویژگی‌ها

- 📱 **تحلیل خودکار پیامک‌های بانکی** - پارس کردن پیامک‌های بانک‌های مختلف
- 🏷️ **دسته‌بندی هوشمند** - دسته‌بندی خودکار هزینه‌ها و درآمدها
- 💾 **ذخیره‌سازی محلی** - استفاده از SQLite برای ذخیره داده‌ها
- 📊 **نمایش آمار** - نمودار و گزارش‌گیری از تراکنش‌ها
- 🔗 **اتصال به N8N** - ارسال داده‌ها برای پردازش پیشرفته‌تر
- 🌐 **رابط کاربری راحت** - طراحی ریسپانسیو و کاربرپسند

## 🚀 راه‌اندازی سریع

### 1. Clone پروژه
```bash
git clone https://github.com/your-username/expense-manager.git
cd expense-manager
```

### 2. نصب وابستگی‌ها
```bash
pip install -r requirements.txt
```

### 3. اجرای برنامه
```bash
python app.py
```

برنامه روی `http://localhost:5000` اجرا خواهد شد.

## 🌐 دیپلوی

### Railway
```bash
# نصب Railway CLI
npm install -g @railway/cli

# ورود به Railway
railway login

# دیپلوی پروژه
railway up
```

### Render
1. فایل‌ها را به GitHub آپلود کنید
2. به render.com بروید
3. "New Web Service" انتخاب کنید
4. Repository خود را متصل کنید
5. Deploy کلیک کنید

### Vercel (فقط فایل‌های استاتیک)
```bash
# نصب Vercel CLI
npm install -g vercel

# دیپلوی
vercel
```

## ⚙️ متغیرهای محیطی

برای عملکرد بهتر، این متغیرها را تنظیم کنید:

```bash
# اختیاری - برای اتصال به N8N
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/expense

# تنظیم پورت (خودکار در پلتفرم‌های ابری)
PORT=5000

# تنظیم محیط
FLASK_ENV=production
```

## 📱 نحوه استفاده

1. **تحلیل پیامک:**
- پیامک بانکی را در کادر وارد کنید
- "تحلیل پیامک" کلیک کنید
- نتایج را مشاهده کنید

2. **مشاهده آمار:**
- آمار کلی در بالای صفحه نمایش داده می‌شود
- تب "نمودار" برای نمایش بصری
- تب "دسته‌بندی" برای گروه‌بندی هزینه‌ها

3. **اتصال N8N:**
- URL webhook N8N را در متغیر محیطی تنظیم کنید
- "تست اتصال N8N" کلیک کنید

## 🔧 ساختار پروژه

expense-manager/
├── app.py              # برنامه اصلی Flask
├── requirements.txt    # وابستگی‌های Python
├── railway.json       # تنظیمات Railway
├── runtime.txt        # نسخه Python
├── Dockerfile         # تنظیمات Docker
├── README.md          # مستندات
├── .gitignore         # فایل‌های نادیده گرفته شده
└── transactions.db    # دیتابیس SQLite (خودکار ایجاد می‌شود)


## 🛠️ تکنولوژی‌ها

- **Backend:** Python Flask
- **Database:** SQLite
- **Frontend:** HTML5/CSS3/JavaScript
- **Charts:** Chart.js
- **Icons:** Font Awesome
- **Deploy:** Railway, Render, Vercel

## 📊 نمونه پیامک‌های پشتیبانی شده

- `کارت شما به مبلغ 125,000 ریال بابت خرید از فروشگاه پردیس بدهکار گردید`
- `حساب شما به مبلغ 50,000 تومان بابت خرید از کافه نادری بدهکار گردید`
- `کارت شما به مبلغ 1,500,000 ریال بابت واریز حقوق بستانکار گردید`

## 🤝 مشارکت

برای مشارکت در پروژه:

1. Fork کنید
2. Branch جدید بسازید (`git checkout -b feature/AmazingFeature`)
3. Commit کنید (`git commit -m 'Add some AmazingFeature'`)
4. Push کنید (`git push origin feature/AmazingFeature`)
5. Pull Request باز کنید

## 📝 لایسنس

این پروژه تحت لایسنس MIT منتشر شده است.

## 📧 تماس

سوال یا پیشنهاد دارید؟ با ما در تماس باشید:

- GitHub Issues: [مسائل پروژه](https://github.com/your-username/expense-manager/issues)
- Email: your-email@example.com

---

**ساخته شده با ❤️ برای مدیریت بهتر هزینه‌ها**
