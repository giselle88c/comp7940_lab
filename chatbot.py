from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackContext)
import configparser
import os
import logging
import redis
global redis1


def main():
# Load your token and create an Updater for your Bot
    #config = configparser.ConfigParser()
    #config.read('config.ini')
    #updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    updater = Updater(token=(os.environ['TELEGRAM']), use_context=True)
    dispatcher = updater.dispatcher
    global redis1
    #redis1 = redis.Redis(host=(config['REDIS']['HOST']), password=(config['REDIS']['PASSWORD']), port=(config['REDIS']['REDISPORT']), decode_responses=(config['REDIS']['DECODE_RESPONSE']), username=(config['REDIS']['USER_NAME']))
    redis1 = redis.Redis(host=(os.environ['REDIS_HOST']), password=(os.environ['REDIS_PASSWORD']), port=(os.environ['REDIS_PORT']), decode_responses=('True'), username=('default'))
    
    # You can set this logging module, so you will know when
    # and why things do not work as expected Meanwhile, update your config.ini as:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    

    # dispatcher for chatgpt
    global chatgpt


    chatgpt = HKBU_ChatGPT()
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command),
    equiped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)

    """
    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)
    """
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", hello))

    dispatcher.add_handler(CommandHandler("user", add_user))
    dispatcher.add_handler(CommandHandler("logout", del_user))

    # To start the bot:
    updater.start_polling()
    updater.idle()


"""
def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)
"""

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def add_user(update: Update, context: CallbackContext) -> None:

    try:

        global redis1
        logging.info(context.args[0])
        msg = context.args[0] 

        # /add keyword <-- this should store the keyword
        if(redis1.exists('user')==0):
            redis1.set('user',msg)
            update.message.reply_text('Hello, '+msg+'! Nice to meet you!')
        else:
            msg=redis1.get('user')
            update.message.reply_text('You have already logged in as '+msg+'~')


    except:
        if(redis1.exists('user')==1):
            msg=redis1.get('user')
            update.message.reply_text('You have already logged in as '+msg+'~')
        else: 
            update.message.reply_text('Usage: /add <keyword>')


def del_user(update: Update, context: CallbackContext) -> None:

    global redis1

    if(redis1.exists('user')==1):

        msg=redis1.get('user')
        redis1.delete('user')
        update.message.reply_text('Goodbye, '+msg+'.')
    else:
        update.message.reply_text('You have not log in yet.')



def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')


def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0] 
        # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg) + ' times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')

def hello(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /hello is issued."""
    try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0] 

        update.message.reply_text('Good day, ' + msg + '!')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /hello <keyword>')


from ChatGPT_HKBU import HKBU_ChatGPT

def equiped_chatgpt(update, context):
    global chatgpt

    reply_message = chatgpt.submit(update.message.text)
        
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

    chatgpt_check=False

if __name__ == '__main__':
    main()