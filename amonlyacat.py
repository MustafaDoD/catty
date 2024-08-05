from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

# تحميل المتغيرات البيئية من ملف .env
TOKEN = '7379071104:AAEZxMSQsAbX5NOL6-LZxdWh_x1iIlgYgKY'
OWNER_CHAT_ID = '1003581140'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'مرحبًا! أرسل صورة قطتك الجميلة لنراها. الرجاء إرسال صورة فقط.'
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('أنا أستقبل صورًا فقط. الرجاء إرسال صورة قطة.')

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    photo = update.message.photo[-1]
    caption = update.message.caption if update.message.caption else "قطة جميلة!"
    user = update.message.from_user
    user_info = f"الصورة مرسلة من المستخدم @{user.username if user.username else user.first_name}"

    # إرسال الصورة إلى مالك البوت
    bot = Bot(token=TOKEN)
    await bot.send_photo(chat_id=OWNER_CHAT_ID, photo=photo.file_id, caption=f"{caption}\n\n{user_info}")

    # إخبار المستخدم أن الصورة قد تم إرسالها
    await update.message.reply_text('تم إرسال الصورة!')

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    application.run_polling()

if __name__ == '__main__':
    main()

