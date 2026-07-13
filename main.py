import os
import random
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


import random


async def find_names(update: Update, context: ContextTypes.DEFAULT_TYPE):

    prefixes = [
        "neo", "ai", "nova", "zen", "nex",
        "cyber", "meta", "byte", "quant",
        "pay", "coin", "lux", "vibe"
    ]

    endings = [
        "ix", "io", "ora", "ly",
        "on", "ex", "a", "um",
        "ify", "labs"
    ]

    names = []

    for i in range(10):
        name = random.choice(prefixes) + random.choice(endings)

        score = rate_username(name)

        names.append((name, score))


    names.sort(key=lambda x: x[1], reverse=True)


    text = "🔥 Новые потенциальные юзы:\n\n"

    for name, score in names:
        text += f"@{name} ⭐ {score}/100\n"


    await update.message.reply_text(text)
    

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
