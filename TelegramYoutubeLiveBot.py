#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A simplle Telegra Bot that provides a Link to a Livestream.

Using the python-telegram-bot framework from https://github.com/python-telegram-bot/python-telegram-bot
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import json
import os
import requests

# configuration file (and data storage :P)
configFilename = 'config.json'
config = None

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Commands for the Bot
def start(bot, update, job_queue, chat_data):
    """Starts the livestream polling."""
    global config
    chanel = config['config']['chanel']
    interval  = config['config']['interval']
    chat_id = update.message.chat_id

    # Add job to queue
    if 'job' not in chat_data:
        # establish data structure
        if chat_id not in config['data']:
            config['data'][chat_id] = {}
        if 'StreamList' not in config['data'][chat_id]:
            config['data'][chat_id]['StreamList'] = {}
        with open(configFilename, 'w') as f:
            json.dump(config, f)

        # actually create the job
        job = job_queue.run_repeating(checkLivestreams, interval, first=0, context=chat_id, name=chat_id)
        chat_data['job'] = job
        update.message.reply_text('Hi! I am now watching for Livestreams of this chanel: ' + chanel + '. I will check every ' + str(interval) + ' Seconds if a new Stream has started. Use /stop to stop the Bot.')
    else:
        update.message.reply_text('You can only use /start once, please use /stop first')


def stop(bot, update, job_queue, chat_data):
    """Stops the livestream polling."""
    chat_id = update.message.chat_id

    # Delete stored data, regardles if a job is running (just to keep the file clean)
    if chat_id in config['data']:
        del config['data'][chat_id]

        with open(configFilename, 'w') as f:
            json.dump(config, f)

    if 'job' not in chat_data:
        update.message.reply_text('Nothing was running! Start using /start.')
        return

    # actually kill the job
    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']

    update.message.reply_text('Stopped successful! Start again using /start.')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('42!')
    # TODO add all Commands


# Jobs the Bot can do
def checkLivestreams(bot, job):
    """Send a message when a new Livestream starts."""
    global config
    chanel = config['config']['chanel']
    apiKey = config['config']['key']

    # Get the data using the youtube v3 api
    r = requests.get("https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=" + chanel + "&eventType=live&type=video&key=" + apiKey)

    if r.status_code != 200:
        logger.warning('The request wasn\'t successful. Errorcode: "%s" Header: "%s" Content: "%s"', r.status_code, r.headers, r.content)
        bot.send_message(job.context, text='There was a Problem with the connection (code ' + str(r.status_code) + ') to Youtube. Check the Chanel ID and your API-Key. You can stop polling using /stop')
    else:
        if r.json()['pageInfo']['totalResults'] > 0:
            newStreamList = {}

            for item in r.json()['items']:
                if item['id']['videoId'] not in config['data'][job.name]['StreamList']:
                    bot.send_message(job.context, text='New Livestream: https://www.youtube.com/watch?v=' + item['id']['videoId'])

                newStreamList[item['id']['videoId']] = item['id']['videoId']

            config['data'][job.name]['StreamList'] = newStreamList

            with open(configFilename, 'w') as f:
                json.dump(config, f)


# Error handlers
def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    global config
    with open(configFilename, 'r') as f:
        config = json.load(f)

    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config['config']['token'])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("stop", stop, pass_job_queue=True, pass_chat_data=True))
    dp.add_handler(CommandHandler("help", help))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()


    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

    logger.warning('Saving the config to "%s"...', configFilename)

    # Saving the config one last time, just in case
    with open(configFilename, 'w') as f:
        json.dump(config, f)

    logger.warning('Bye')


if __name__ == '__main__':
    main()
