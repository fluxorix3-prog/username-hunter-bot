import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Username Hunter запущен!\n\n"
        "Команды:\n"
        "/find — найти варианты юзов\n\n"
        "Или отправь любое имя для оценки."
    )


def rate_username(username):
    score = 50

    if len(username) <= 5:
        score += 25
    elif len(username) <= 7:
        score += 15

    if username.isalpha():
        score += 10

    for letter in ["x", "a", "o", "i", "n", "v"]:
        if letter in username.lower():
            score += 3

    return min(score, 100)


async def find_names(update: Update, context: ContextTypes.DEFAULT_TYPE):
    names = [
        ("aivora", 94),
        ("nexora", 92),
        ("payzen", 90),
        ("lunex", 88),
        ("veliq", 87),
    ]

    text = "🔥 Потенциальные юзернеймы:\n\n"

    for name, score in names:
        text += f"@{name} — ⭐ {score}/100\n"

    await update.message.reply_text(text)


async def check_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text.lower().replace("@", "")

    score = rate_username(username)

    await update.message.reply_text(
        f"🔍 Анализ: @{username}\n\n"
        f"⭐ Потенциал: {score}/100\n\n"
        "⏳ Проверка занятости будет добавлена."
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("find", find_names))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, check_username)
    )

    app.run_polling()


if __name__ == "__main__":
    main()
