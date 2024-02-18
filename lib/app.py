import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler
from auth import token, spotify_client_id, spotify_client_secret
import spotify_api as sp_api

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="I'm a bot, please talk to me!"
        )
    
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
    
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def playlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #parse args
    msg = update.message.text
    msg = msg.split(' ')
    if len(msg) <= 1:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="What kind of playlist would you like?")
    else:
        #call spotify api
        link = sp_api.create_playlist(' '.join(msg[1:]), 10)
        #send playlist link as response
        await context.bot.send_message(chat_id=update.effective_chat.id, text= str(link))

async def recommend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    msg = msg.split(' ')
    if len(msg) <= 1:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="What kind of playlist would you like?")
    else:
        #call spotify api
        link, name  = sp_api.get_recommendations(' '.join(msg[1:]), 10)
        #send playlist link as response
        msg = "if you like " + ' '.join(msg[1:]) + " you should listen to " + name + " at " + link
        await context.bot.send_message(chat_id=update.effective_chat.id, text= msg)

if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    spotify_handler = CommandHandler('playlist', playlist, has_args=True)
    recommend_handler = CommandHandler('recommend', recommend, has_args=True)

    application.add_handler(recommend_handler)
    application.add_handler(spotify_handler)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.run_polling()