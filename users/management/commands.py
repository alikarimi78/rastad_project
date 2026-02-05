import re
from django.core.management.base import BaseCommand
from django.conf import settings

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from users import services

REF_RE = re.compile(r"^ref_(\d+)$")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_id = update.effective_user.id
    services.upsert_user(tg_id)

    msg = "ثبت‌نام انجام شد."
    if context.args:
        m = REF_RE.match(context.args[0])
        if m:
            referrer_id = int(m.group(1))
            try:
                ref = services.create_referral(referrer_id, tg_id)
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
        dto = services.get_status(tg_id)
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
    data = services.get_ref_summary(tg_id)
    if data["count"] == 0:
        await update.message.reply_text("فعلاً زیرمجموعه‌ای نداری.")
        return

    lines = [f"count: {data['count']}", "last 5:"]
    for r in data["last_5_referrals"]:
        lines.append(f"- {r['telegram_id']} | {r['created_at']}")
    await update.message.reply_text("\n".join(lines))

class Command(BaseCommand):
    help = "Run Telegram bot"

    def handle(self, *args, **options):
        app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("my_status", my_status))
        app.add_handler(CommandHandler("ref_summary", ref_summary))
        app.run_polling()