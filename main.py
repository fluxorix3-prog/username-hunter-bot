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


def rate_username(username):

    username = username.lower()

    score = 50


    # Длина
    length = len(username)

    if 5 <= length <= 6:
        score += 25

    elif 7 <= length <= 9:
        score += 15

    elif length > 12:
        score -= 15


    # Гласные = легче произнести
    vowels = "aeiou"

    vowel_count = sum(
        1 for x in username if x in vowels
    )

    if vowel_count >= 2:
        score += 15


    # Ценные темы
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
            score += 15
            break


    # Красивые буквы
    if any(x in username for x in ["x", "v", "z"]):
        score += 5


    # Штрафы

    if any(char.isdigit() for char in username):
        score -= 20


    if " " in username:
        score -= 50


    return max(0, min(score, 100))



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Username Hunter запущен!\n\n"
        "Команды:\n"
        "/find — найти новые юзы\n\n"
        "Отправь любой юз для оценки."
    )



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


    while len(results) < 20:

        name = (
            random.choice(prefixes)
            +
            random.choice(endings)
        )


        if not name.isalpha():
            continue


        if len(name) < 5:
            continue


        results.add(name)



    ranked = []


    for name in results:

        score = rate_username(name)

        ranked.append(
            (name, score)
        )



    ranked.sort(
        key=lambda x: x[1],
        reverse=True
    )


    text = "🔥 ТОП потенциальных юзов:\n\n"


    for name, score in ranked[:10]:

        text += (
            f"@{name} ⭐ {score}/100\n"
        )



    await update.message.reply_text(text)




async def check_username(update: Update, context: ContextTypes.DEFAULT_TYPE):


    username = (
        update.message.text
        .lower()
        .replace("@", "")
    )


    score = rate_username(username)


    await update.message.reply_text(

        f"🔍 Анализ @{username}\n\n"
        f"⭐ Потенциал: {score}/100"

    )




def main():

    app = Application.builder().token(TOKEN).build()


    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CommandHandler(
            "find",
            find_names
        )
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
