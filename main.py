import os
import random

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)


TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Username Hunter запущен!\n\n"
        "Команды:\n"
        "/find — найти новые юзы\n\n"
        "Отправь любое имя — я оценю его."
    )


def rate_username(username):

    username = username.lower()

    score = 0
    reasons = []


    # Длина
    length = len(username)

    if length <= 5:
        score += 30
        reasons.append("короткий юз")
    elif length <= 7:
        score += 20
        reasons.append("хорошая длина")
    elif length <= 10:
        score += 10


    # Произносимость
    vowels = "aeiou"

    vowel_count = sum(
        1 for x in username if x in vowels
    )

    if vowel_count >= 2:
        score += 15
        reasons.append("легко произносится")


    # Брендовые слова
    premium_words = [
        "ai",
        "bot",
        "neo",
        "nova",
        "nex",
        "pay",
        "coin",
        "crypto",
        "meta",
        "labs",
        "hub",
        "cloud",
        "agent"
    ]


    for word in premium_words:
        if word in username:
            score += 20
            reasons.append(f"тема: {word}")
            break


    # Красивые буквы
    if any(x in username for x in ["x", "v", "z"]):
        score += 5


    # Штрафы

    if any(char.isdigit() for char in username):
        score -= 15
        reasons.append("есть цифры")


    if len(set(username)) < len(username) - 2:
        score -= 10


    score = max(0, min(score, 100))


    return score


async def find_names(update: Update, context: ContextTypes.DEFAULT_TYPE):

    prefixes = [
        "neo",
        "ai",
        "nova",
        "zen",
        "nex",
        "cyber",
        "meta",
        "byte",
        "quant",
        "pay",
        "coin",
        "lux",
        "vibe",
        "volt",
        "orb"
    ]

    endings = [
        "ix",
        "io",
        "ora",
        "ly",
        "on",
        "ex",
        "a",
        "um",
        "ify",
        "labs"
    ]


    results = set()


    while len(results) < 10:
        name = random.choice(prefixes) + random.choice(endings)
        results.add(name)


    ranked = []

    for name in results:
        score = rate_username(name)
        ranked.append((name, score))


    ranked.sort(
        key=lambda x: x[1],
        reverse=True
    )


    text = "🔥 Новые потенциальные юзы:\n\n"


    for name, score in ranked:
        text += f"@{name} ⭐ {score}/100\n"


    await update.message.reply_text(text)



async def check_username(update: Update, context: ContextTypes.DEFAULT_TYPE):

    username = (
        update.message.text
        .lower()
        .replace("@", "")
    )

    score = rate_username(username)


    await update.message.reply_text(
        f"🔍 Анализ: @{username}\n\n"
        f"⭐ Потенциал: {score}/100"
    )



def main():

    app = Application.builder().token(TOKEN).build()


    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("find", find_names)
    )


    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            check_username
        )
    )


    app.run_polling()



if __name__ == "__main__":
    main()
