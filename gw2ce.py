# -*- coding: utf-8 -*-

import telebot
from telebot import types
import urllib3
import json
import time

API_URL = "https://api.guildwars2.com/v2/commerce/exchange/coins?quantity="

API_TOKEN = '873331378:AAHMGCU70vFp9TeXGbxCGVUR2kA-5OIqpyQ'

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Hi there, Coins treshold?
""")
    bot.register_next_step_handler(msg, process_reply_step)


def process_reply_step(message):
    try:
        chat_id = message.chat.id
        http = urllib3.PoolManager()
        last_res = 0

        while True:
            print(chat_id)
            resp = http.request('GET', API_URL + '1000000' + '&access_token=564F181A-F0FC-114A-A55D-3C1DCD45F3767AF3848F-AB29-4EBF-9594-F91E6A75E015')
            print(chat_id)
            data = json.loads(resp.data.decode('utf-8'))
            #print('coins_per_gem: ' + str(data['coins_per_gem']) + ', quantity: ' + str(data['quantity']))
            res = data['coins_per_gem']*100
            print(res)
            if res != last_res and res < int(message.text):
                #msg = bot.reply_to(message, 'coins_per_gem: ' + str(data['coins_per_gem']) + ', quantity: ' + str(data['quantity']))
                bot.send_message(chat_id,'''\
Value reached!!!.
Threshold set: {treshold_set}
Coins: {coins}.\
'''.format(treshold_set= message.text, coins=res)                
                )
                last_res = res
            time.sleep(10)
    except Exception as e:
        bot.reply_to(message, str(e))


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
#bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
#bot.load_next_step_handlers()

bot.polling()