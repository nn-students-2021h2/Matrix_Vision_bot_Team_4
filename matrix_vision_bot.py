import functools
import logging
from matrix_vision import MatrixVision
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater
from configs import Config

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

log = logging.getLogger()
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text(f'Hi, {update.effective_user.first_name}!')


def chat_help(update: Update, context: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Send /start')


def reply_to_text(update: Update, context: CallbackContext):
    """Send some help to user."""
    update.message.reply_text("Image is expected!")


def reply_animation(update: Update, context: CallbackContext, config: Config):
    """Send animated photo in matrix vision style to user."""
    image = update.message.photo[-1].get_file()
    log.info("Image has been downloaded.")
    matrix_vision = MatrixVision(image.download(), config.properties['fonts_path'])
    animation_file_id = matrix_vision.run()
    with open(animation_file_id, 'rb') as animation:
        update.message.reply_animation(animation = animation)


def reply_to_document(update: Update, context: CallbackContext):
    """Send echo photo to user."""
    update.message.reply_text("Image is expected!")


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    log.warning(f'Update {update} caused error {context.error}')
    update.message.reply_text('Something happened, please try again later.')


def main():
    global_config = Config(file_path='config.json')
    updater = Updater(global_config.properties['token'], use_context=True)

    # on different commands - answer in Telegram
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', chat_help))

    # add replies for image, documents and text messages on Telegram
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, functools.partial(reply_animation, config = global_config)))
    updater.dispatcher.add_handler(MessageHandler(Filters.document, reply_to_document))

    updater.dispatcher.add_handler(MessageHandler(Filters.text, reply_to_text))

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
