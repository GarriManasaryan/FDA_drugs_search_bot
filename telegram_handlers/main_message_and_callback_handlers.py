from bot_base.bot_main import *
from telegram_handlers.error_handlers import *
from services.generate_citation import *
from time import sleep
from datetime import datetime, timedelta
from bot_reboot.ressurection_handler import *
from logs.custom_logger import *

@bot.message_handler(content_types=['text'])
@message_error_handler()
def welcome(message):
    chat_id = message.chat.id

    if chat_id in banned_list:
        bot.send_message(chat_id, banned_message)

    else:
        text = message.text

        if text == '/start':
            if user_is_spamming(message, chat_id):
                bot.send_message(chat_id, banned_message)

            else:
                msg = bot.send_message(chat_id, welcome_message)
                bot.register_next_step_handler(msg, process_citation_generation, chat_id)

@message_error_handler()
def process_citation_generation(message, chat_id):
    bot.send_message(chat_id, 'Processing...')
    bot.send_message(chat_id, single_citation_main(message.text))

@message_error_handler()
def user_is_spamming(message, chat_id):
    chat_id_string = str(chat_id)

    if chat_id_string != developer_chat_id:
        with open(os.path.join(os.getcwd(), 'spam_defender_files', 'spam_counter.json')) as f:
            spam_counter = json.load(f)

        clicked = spam_counter.get(chat_id_string, 0)
        spam_counter[chat_id_string] = clicked + 1

        with open(os.path.join(os.getcwd(), 'spam_defender_files', 'spam_counter.json'), 'w') as f:
            json.dump(spam_counter, f)

        if spam_counter.get(chat_id_string) > 3:
            old_user_handler(chat_id, 'banned_list')
            return True

        else:
            return False

    else:
        return False

def old_user_handler(user_chat_id, old_user_reason_list):
    with open(os.path.join(os.getcwd(), 'spam_defender_files', f'{old_user_reason_list}.json'), 'w') as f:
        source_list = banned_list if old_user_reason_list == 'banned_list' else already_processed_users
        source_list.append(user_chat_id)
        json.dump(source_list, f)