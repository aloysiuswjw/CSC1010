import Constants as keys
import Responses as R
from telegram.ext import *


print("Bot Started...")

def start_command(update, context):
    update.message.reply_text("Type something to get started.")

def help_command(update, context):
    update.message.reply_text("Help words")

def handle_message(update, context):
    text = str(update.message.text).lower() #recieve text from the user
    response = R.sample_reponses(text) #this process the message
    update.message.reply_text(response) #put it back to the user

def error(update,context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(keys.API_KEY, use_context=True) #starting up the bot
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(error)

    updater.start_polling() #how many seconds for the bot to check for the user input
    updater.idle()

main()

