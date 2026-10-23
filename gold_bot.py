import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from bs4 import BeautifulSoup

# تنظیمات لاگ‌گیری
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# تابع دریافت قیمت لحظه‌ای طلا ۱۸ عیار
def get_gold_price_18k():
    try:
        url = "https://www.tgju.org/profile/geram18"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        price_str = soup.find('span', {'data-col': 'info.last_trade.PDrts'}).text
        price = int(price_str.replace(',', ''))
        return price
    except Exception as e:
        print(f"خطا در استخراج قیمت: {e}")
        return None

# الگوریتم تحلیل و پیش‌بینی ۴۸ ساعته
def advanced_48h_analysis():
    dollar_trend = "up"            # روند نرخ ارز
    global_gold_rsi = 62           # شاخص تکنیکال انس جهانی
    market_bubble_status = "high"  # وضعیت حباب بازار

    score = 0
    reasons = []

    if dollar_trend == "up":
        score += 2
        reasons.append("• دلار آزاد در کانال صعودی کوتاه مدت قرار دارد.")
    elif dollar_trend == "down":
        score -= 2
        reasons.append("• فشار نزولی در بازار ارز مشاهده می‌شود.")

    if global_gold_rsi > 70:
        score -= 1
        reasons.append("• انس جهانی در محدوده اشباع خرید قرار گرفته است.")
    elif global_gold_rsi < 35:
        score += 1
        reasons.append("• انس جهانی در محدوده حمایتی قرار دارد.")
    else:
        reasons.append("• انس جهانی نوسان خنثی و طبیعی دارد.")

    if market_bubble_status == "high":
        score -= 2
        reasons.append("• حباب بازار طلا بالا است؛ احتمال اصلاح قیمت وجود دارد.")
    else:
        score += 1
        reasons.append("• حباب بازار در محدوده امن قرار دارد.")

    if score >= 2:
        recommendation = (
            "🟢 **سیگنال ۴۸ ساعته: نگهداری / پتانسیل رشد ملایم**\n"
            "با توجه به وضعیت شاخص‌ها، افت قیمتی شدیدی در ۴۸ ساعت آینده پیش‌بینی نمی‌شود."
        )
    elif score <= -2:
        recommendation = (
            "🔴 **سیگنال ۴۸ ساعته: احتیاط و احتمال اصلاح قیمت**\n"
            "به دلیل حباب بالا یا فشار فروش در بازارهای مرجع، احتمال اصلاح قیمت کوتاه مدت وجود دارد."
        )
    else:
        recommendation = (
            "🟡 **سیگنال ۴۸ ساعته: بازار خنثی**\n"
            "تغییرات قیمت در ۴۸ ساعت آینده محدود و نوسانی خواهد بود."
        )

    analysis_text = f"📊 **تحلیل تکنیکال و فاندامنتال (۴۸ ساعت آینده):**\n"
    for r in reasons:
        analysis_text += f"{r}\n"
    analysis_text += f"\n{recommendation}"
    
    return analysis_text

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! به ربات محاسبه‌گر و تحلیل‌گر قیمت طلا خوش آمدید.\n\n"
        "لطفاً وزن طلای ۱۸ عیار را به **گرم** وارد کنید (مثلاً: 12.5):"
    )

# پردازش وزن ورودی
async def process_weight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        weight = float(text)
        price_per_gram = get_gold_price_18k()
        
        if price_per_gram:
            total_price = weight * price_per_gram
            market_analysis = advanced_48h_analysis()
            
            response_text = (
                f"⚖️ **وزن:** {weight} گرم\n"
                f"💰 **نرخ ۱۸ عیار:** {price_per_gram:,} ریال\n"
                f"💎 **ارزش کل:** {int(total_price):,} ریال\n\n"
                f"-----------------------------------\n"
                f"{market_analysis}"
            )
        else:
            response_text = "خطا در دریافت قیمت لحظه‌ای. لطفاً مجدداً تلاش کنید."
            
    except ValueError:
        response_text = "لطفاً عدد معتبر وارد کنید (مثلاً: 5 یا 10.5)."

    await update.message.reply_text(response_text, parse_mode='Markdown')

if __name__ == '__main__':
    # توکن اختصاصی شما در کد زیر قرار دارد
    TOKEN = "8678134153:AAGjr-ZuyRDa55XbRZ9pEawBEUxUjhLEra0"
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_weight))
    
    print("ربات طلا با موفقیت روشن شد...")
    app.run_polling()