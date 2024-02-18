import logging
from telegram import Update
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
)
from auth import token, spotify_client_id, spotify_client_secret
import spotify_api as sp_api

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hi, type /help to see the available commands.",
    )


async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    msg = msg.split(" ")
    response = ""
    if msg[0] == "/playlist":
        response = playlist(update, context)
    elif msg[0] == "/recommend":
        response = recommend(update, context)
    elif msg[0] == "/help":
        response = help(update, context)
    else:
        response = unknown(update, context)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=str(response))


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return "Sorry, I didn't understand that command. Type /help to see the available commands."


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return "Available commands: \n /playlist <genre/artist/song> - creates a playlist based on the parameters \n /recommend <song> - recommends a song based on the song you input \n /help - brings up this prompt"


def playlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # parse args
    msg = update.message.text
    msg = msg.split(" ")
    if len(msg) <= 1:
        response = "What genre/artist/song would you like a playlist for?"
    else:
        # call spotify api
        link = sp_api.create_playlist(" ".join(msg[1:]), 10)
        # send playlist link as response
        response = "Here is the playlist link: " + link
    return response


def recommend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    msg = msg.split(" ")
    if len(msg) <= 1:
        msg = "What song would you like a recommendation for?"
    else:
        # call spotify api
        link, name = sp_api.get_recommendation(" ".join(msg[1:]), 10)
        # send playlist link as response
        msg = (
            'if you like "'
            + " ".join(msg[1:])
            + '" you should listen to "'
            + name[1]
            + " - "
            + name[0]
            + '" at '
            + link
        )
    return msg


if __name__ == "__main__":
    application = ApplicationBuilder().token(token).build()

    message_handler = MessageHandler(filters.CHAT & (~filters.COMMAND), handle_message)
    command_handler = MessageHandler(filters.COMMAND, handle_command)

    application.add_handler(message_handler)
    application.add_handler(command_handler)
    application.run_polling()
