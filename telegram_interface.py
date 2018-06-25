from telegram.ext import Updater, CommandHandler
import sqlite3
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()
TOKEN = "593812672:AAE_77FAMjFoISjwvsWt_XSy5MkMQ8Smsvs"
connection = sqlite3.connect('surveyor.db')


def start(bot, update):
    logger.info(update.message.chat.title)
    update.message.reply_text(
        "I'm a bot, Nice to meet you!")


def main():
    # Create Updater object and attach dispatcher to it
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    logger.info("Bot started")
    # Add command handler to dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()
