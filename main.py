import os #For creating HTTP server

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

EMAIL, NAME, CONFIRM, LOCATION, FREQUENCY, CHECK, BIO = range(7)

def connect(bot, update, user_data):
    update.message.reply_text(
        'Hi! I will now help you get personal notifications by connecting telegram to your ThirdWheel account.\n\n'
        'Send /cancel to stop talking to me.\n\n'
        'What is your login email?')
    return EMAIL

# user_data is like a global variable (dictionary) that can store data across states for use.
# To use, it needs to be put in the functions where it is accessed, and in the ConversationalHandler states below.
def email(bot, update, user_data):
    user = update.message.from_user
    email = update.message.text
    user_data['email'] = email
    logger.info("Email of %s: %s", user.first_name, email)
    update.message.reply_text('Confirm ' + email + ' is correct?', reply_markup=ReplyKeyboardMarkup([['Yes', 'No']], one_time_keyboard=True))
    return NAME

# Ask for name of 1 person user added
def name(bot, update, user_data):
    user = update.message.from_user
    logger.info("User %s is getting tested to see if email %s belongs to him/her.", user.first_name, user_data['email'])
    update.message.reply_text('Great, now I need to check if your email ' + user_data['email'] + ' belongs to you.'
                               'Tell me the name of 1 person you added to ThirdWheel.')
    return FREQUENCY

# Ask for frequency
def frequency(bot, update, user_data):
    user = update.message.from_user
    friend = update.message.text
    user_data['friend'] = friend
    update.message.reply_text('Now tell me, what freqency did you set ' + friend + ' to?',
           reply_markup=ReplyKeyboardMarkup([['1 Week', '2 Weeks', '3 Weeks', '1 Month', '6 Weeks', '3 Months', '6 Months']], one_time_keyboard=True))
    return CONFIRM

# Confirm 2 data points above
def confirm(bot, update, user_data):
    user = update.message.from_user
    frequency = update.message.text
    user_data['frequency'] = frequency
    update.message.reply_text('To confirm, you set ' + user_data['friend'] + ' on ' + user_data['frequency'] + ' ?',
                              reply_markup=ReplyKeyboardMarkup([['Yes', 'No']], one_time_keyboard=True))
    return CHECK

def check(bot, update, user_data):
    update.message.reply_text('Checking records...')
    logger.info("Telegram script sending SQL query to verify data...")
    return LOCATION

################################################################################################

def location(bot, update):
    user = update.message.from_user
    user_location = update.message.location
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me something about yourself.')
    return BIO


def skip_location(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me something about yourself.')
    return BIO


def bio(bot, update):
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def error_callback(bot, update, error):
    try:
        raise error
    except Unauthorized:
        logger.warning('remove update.message.chat_id from conversation list', update, error)
    except BadRequest:
        logger.warning('handle malformed requests', update, error)
    except TimedOut:
        logger.warning('handle slow connection problems', update, error)
    except NetworkError:
        logger.warning('handle other connection problems', update, error)
    except ChatMigrated as e:
        logger.warning('the chat_id of a group has changed, use e.new_chat_id instead', update, error)
    except TelegramError:
        logger.warning('handle all other telegram related errors', update, error)

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("725959580:AAHBI0I0A023e6sXw1ErIPYWPU86iBLEhp4")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('connect', connect, pass_user_data=True)],

        states={
            EMAIL: [RegexHandler('[^@]+@[^@]+\.[^@]+', email, pass_user_data=True)],

            NAME: [RegexHandler('Yes', name, pass_user_data=True),
                   RegexHandler('No', connect, pass_user_data=True)],

            FREQUENCY: [MessageHandler(Filters.text, frequency, pass_user_data=True)],

            CONFIRM: [RegexHandler('1 Week|2 Weeks|3 Weeks|1 Month|6 Weeks|3 Months|6 Months', confirm, pass_user_data=True),
                      RegexHandler('No', connect, pass_user_data=True)],

            CHECK: [RegexHandler('Yes', check, pass_user_data=True),
                   RegexHandler('No', name, pass_user_data=True)],

            BIO: [MessageHandler(Filters.text, bio, pass_user_data=True)],

            LOCATION: [MessageHandler(Filters.text, bio, pass_user_data=True)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)
    dp.add_error_handler(error_callback)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
    
    port = os.getenv('PORT', default=8000) #creating HTTP server server to tell Heroku to bind to to receive requests with tele API
    updater.start_webhook(port=port) # Connecting port to tele API
