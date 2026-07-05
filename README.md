# Process Mining & AI Readiness Assessment
ابزار تحلیل فرآیند و ارزیابی آمادگی هوش مصنوعی برای سازمان‌ها

## معماری سیستم
Camunda DB (act_hi_*)
↓
Python + PM4Py (تحلیل)
↓
Process Mining DB (نتایج)
↓
Streamlit Dashboard (نمایش)

## امکانات

- تحلیل لاگ‌های Camunda
- کشف فرآیند با PM4Py
- محاسبه شاخص‌های کلیدی (Rework Rate, Cycle Time, Completion Rate)
- ارزیابی آمادگی AI برای هر فرآیند
- داشبورد تعاملی با Streamlit

## پیش‌نیازها

- Python 3.11+
- PostgreSQL 16+
- Camunda 7

## نصب و راه‌اندازی

### ۱. کلون کردن پروژه
```bash
git clone https://github.com/afsaneh3041/process-mining-ai-readiness.git
cd process-mining-ai-readiness
```

### ۲. نصب کتابخونه‌ها
```bash
pip install -r requirements.txt
```

### ۳. تنظیم دیتابیس
دو دیتابیس PostgreSQL بساز:
- `camunda_db`: برای جداول Camunda
- `process_mining`: برای نتایج تحلیل

### ۴. تنظیم متغیرهای محیطی
یک فایل `.env` در پوشه پروژه بساز:
DB_PASSWORD=پسورد_PostgreSQL_خودت
**نکته:** فایل `.env` رو هرگز روی GitHub آپلود نکن!

### ۵. اجرای Notebook
```bash
jupyter notebook mining.ipynb
```

### ۶. اجرای داشبورد
```bash
streamlit run app.py
```

## شاخص‌های تحلیل

| شاخص | توضیح |
|------|-------|
| Rework Rate | نرخ بازکاری |
| Cycle Time | زمان کل فرآیند |
| Completion Rate | نرخ تکمیل |
| Variant Ratio | تنوع مسیرها |
| AI Readiness Score | امتیاز آمادگی AI |

## ساختار دیتابیس

### camunda_db (ورودی)
- `act_hi_procinst`: نمونه‌های فرآیند
- `act_hi_actinst`: تاریخچه فعالیت‌ها
- `act_hi_taskinst`: تاریخچه تسک‌ها
- `act_hi_varinst`: متغیرها

### process_mining (خروجی)
- `pm_process_summary`: خلاصه فرآیندها
- `pm_activity_analysis`: تحلیل فعالیت‌ها
- `pm_ai_readiness`: امتیاز AI
- `pm_recommendations`: توصیه‌ها

## نکات امنیتی

- پسورد دیتابیس رو توی `.env` نگه دار
- فایل `.env` توی `.gitignore` قرار داره و آپلود نمی‌شه
- توکن‌های API رو هرگز توی کد قرار نده

## سازنده

افسانه راوش - BPM & AI Consultant

---
⭐ اگر مفید بود ستاره بدید!
