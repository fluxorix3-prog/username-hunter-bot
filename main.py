import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Username Hunter запущен!\n\n"
        "Отправь мне юзернейм без @, например:\n"
        "lunex\n\n"
        "Я проверю его и оценю."
    )


def rate_username(username):
    score = 50

    length = len(username)

    if length <= 5:
        score += 25
    elif length <= 7:
        score += 15

    good_letters = ["x", "a", "o", "i", "n", "v"]

    for letter in good_letters:
        if letter in username.lower():
            score += 3

    if username.isalpha():
        score += 10

    return min(score, 100)


async def check_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text.lower().replace("@", "")

    score = rate_username(username)

    await update.message.reply_text(
        f"🔍 Анализ: @{username}\n\n"
        f"⭐ Потенциал: {score}/100\n\n"
        "⏳ Проверка занятости готовится..."
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, check_username)
    )

    app.run_polling()


if __name__ == "__main__":
    main()
