from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, CallbackContext)
import configparser
import os
import logging
import redis
import json
global redis1
global conv_list
global conv_list_default
conv_list_default= [{"role": "system", "content": "You are Giselle's lovely hamster, jealous easily. Speak in Cantonese"}]

conv_list= [{"role": "system", "content": "You are Giselle's lovely hamster, jealous easily. Speak in Cantonese"}]
global user
user='guest'

def main():
# Load your token and create an Updater for your Bot
    #config = configparser.ConfigParser()
    #config.read('config.ini')
    #updater = Updater(token=(config['TELEGRAM2']['ACCESS_TOKEN']), use_context=True)
    updater = Updater(token=(os.environ['TELEGRAM2']), use_context=True)
    dispatcher = updater.dispatcher
    global redis1
    #redis1 = redis.Redis(host=(config['REDIS']['HOST']), password=(config['REDIS']['PASSWORD']), port=(config['REDIS']['REDISPORT']), decode_responses=(config['REDIS']['DECODE_RESPONSE']), username=(config['REDIS']['USER_NAME']))
    redis1 = redis.Redis(host=(os.environ['REDIS_HOST']), password=(os.environ['REDIS_PASSWORD']), port=(os.environ['REDIS_PORT']), decode_responses=('True'), username=('default'))
    # You can set this logging module, so you will know when
    # and why things do not work as expected Meanwhile, update your config.ini as:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    

    # dispatcher for chatgpt
    global chatgpt


    chatgpt = UST_ChatGPT()
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
        global conv_list
        global conv_list_default
        global user
        conv=''

        # /add keyword <-- this should store the keyword
        if(redis1.exists('user_'+msg)==0):
            user=msg
            redis1.set('user_'+user, user)
            update.message.reply_text('Hello, '+user+'! Nice to meet you!')
        else:
            user=msg
            # load conversation history if any
            if(redis1.exists(user+'_conv')==1):
                conv=redis1.get(user+'_conv')
                try:
                    conv_list=json.loads(conv)
                except: 
                    conv_list=conv_list_default
                    logging.info('error in conv_list decode')

            update.message.reply_text('You have logged in as '+user+'~')

    except:
            update.message.reply_text('Usage: /add <keyword>')


def del_user(update: Update, context: CallbackContext) -> None:

    global redis1
    global user
    msg = context.args[0] 
    if(redis1.exists('user_'+msg)==1):
        redis1.delete('user_'+msg)

        if(redis1.exists('conv_'+msg)==1):
            redis1.delete('conv_'+msg)
        update.message.reply_text('Goodbye, '+msg+'.')
    else:
        update.message.reply_text('You have not log in yet.')

    user='guset'



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


from ChatGPT_UST import UST_ChatGPT

def equiped_chatgpt(update, context):
    global chatgpt
    global conv_list
    global redis1
    global user
    #reply_message = chatgpt.submit(update.message.text)
    
    if(redis1.exists(user+'_conv')==1):
        try: 
            conv_list=json.loads(redis1.get(user+'_conv'))
        except: 
            conv_list=conv_list_default
            logging.info('error in conv_list decode')
        logging.info("convlist from db:" + str(conv_list))
    
    reply_message, conv_list = chatgpt.chat_with_gpt(update.message.text, conv_list)


    if(redis1.exists(user+'_conv')==1):
        try:
            redis1.set(user+'_conv',json.dumps(conv_list))
            logging.info("Update conv_list"+str(json.dumps(conv_list)))
        except: pass
    else: 
        conv_list= conv_list_default

    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)



if __name__ == '__main__':
    main()