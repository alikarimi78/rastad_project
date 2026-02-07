import re
import time
from datetime import datetime
from zoneinfo import ZoneInfo

from django.core.management.base import BaseCommand
from django.conf import settings

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from users import services

REF_RE = re.compile(r"^ref_(\d+)$")

PERSIAN_WEEKDAYS = [
    "دوشنبه",   # 0
    "سه‌شنبه",  # 1
    "چهارشنبه", # 2
    "پنجشنبه",  # 3
    "جمعه",     # 4
    "شنبه",     # 5
    "یکشنبه",   # 6
]

tz = ZoneInfo("Asia/Tehran")      # ایران


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.effective_user.id
    await services.upsert_user_async(tg_id)

    msg = "اگه شما زهرای منی، ثبت‌نام انجام شد 💖🫀😘✨\nبقیه مهم نیستن سیکتر😒"
    if context.args:
        m = REF_RE.match(context.args[0])
        if m:
            referrer_id = int(m.group(1))
            try:
                ref = await services.create_referral_async(referrer_id, tg_id)
                # اگر قبلاً referrer داشته باشد، get_or_create همان قبلی را برمی‌گرداند
                if ref.referrer.telegram_id != referrer_id:
                    msg = "قبلاً با یک referrer دیگر ثبت شده بودی؛ تغییری نکرد."
                else:
                    msg = f"ثبت‌نام انجام شد. referrer شما: {referrer_id}"
            except ValueError as e:
                msg = str(e)

    await update.message.reply_text(msg)

async def my_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.effective_user.id
    try:
        dto = await services.get_status_async(tg_id)
        txt = (
            f"telegram_id: {dto.telegram_id}\n"
            f"referrer_id: {dto.referrer_telegram_id}\n"
            f"created_at: {dto.created_at}"
        )
    except Exception:
        txt = "هنوز ثبت‌نام نشده‌ای. /start را بزن."
    await update.message.reply_text(txt)

async def ref_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.effective_user.id
    data = await services.get_ref_summary_async(tg_id)
    if data["count"] == 0:
        await update.message.reply_text("فعلاً زیرمجموعه‌ای نداری.")
        return

    lines = [f"count: {data['count']}", "last 5:"]
    for r in data["last_5_referrals"]:
        lines.append(f"- {r['telegram_id']} | {r['created_at']}")
    await update.message.reply_text("\n".join(lines))

async def print_daily_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now(tz)
    weekday = PERSIAN_WEEKDAYS[now.weekday()]
    time_str = now.strftime("%H:%M:%S")
    await update.message.reply_text(f"امروز {weekday} ساعت {time_str} بیشتر از دیروز عاشقتم زهرای من🫀😘🫠 ")

class Command(BaseCommand):
    help = "Run Telegram bot"

    def handle(self, *args, **options):
        app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("my_status", my_status))
        app.add_handler(CommandHandler("ref_summary", ref_summary))
        app.add_handler(CommandHandler("daily_note", print_daily_note))
        app.run_polling()