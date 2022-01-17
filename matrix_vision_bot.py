import logging
from matrix_vision import MatrixVision
from telegram import Bot, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater
from configs import Config
import urllib
#import matrix_vision as mtr

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

log = logging.getLogger()
conf = Config()
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text(f'Hi, {update.effective_user.first_name}!')


def chat_help(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Send /start')


def echo_text(update: Update, context: CallbackContext):
    """Send some help to user."""
    update.message.reply_text("Image expected!")


def echo_photo(update: Update, context: CallbackContext):
    """Send echo photo to user."""
    MatrixVision().run()
    update.message.reply_photo(update.message.photo[-1])


def echo_document(update: Update, context: CallbackContext):
    """Send echo photo to user."""
    update.message.reply_text("")


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    log.warning(f'Update {update} caused error {context.error}')
    update.message.reply_text('Something happened, please try again later.')


def main():
    updater = Updater(conf.properties['token'], use_context=True)

    # on different commands - answer in Telegram
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', chat_help))

    # echo the message on Telegram
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo_text))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, echo_photo))
    updater.dispatcher.add_handler(MessageHandler(Filters.document, echo_document))

    # log all errors
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    log.info('Start Bot')
    main()
