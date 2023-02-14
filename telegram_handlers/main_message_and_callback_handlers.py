from bot_base.bot_main import *
from telegram_handlers.error_handlers import *
from time import sleep
from datetime import datetime, timedelta
from bot_reboot.ressurection_handler import *
from logs.custom_logger import *

with open(os.path.join(os.getcwd(), 'fda_db_download', 'applno_fda_dict.json')) as f:
    applno_fda_dict = json.load(f)

with open(os.path.join(os.getcwd(), 'fda_db_download', 'drug_fda_dict.json')) as f:
    drug_fda_dict = json.load(f)
    drug_params = [[i, 'Drug name', i] for i in list(drug_fda_dict.keys())]

queries_list = sorted([[i[0],
                InlineQueryResultArticle(id = str(num),
                                        title = i[0],
                                        input_message_content = InputTextMessageContent(i[0]),
                                        description = i[1]),
                i[2]
                ] for num, i in enumerate(drug_params)], key = lambda x: x[0])

@bot.inline_handler(lambda query: True)
def query_text(inline_query):

    try:
        if len(inline_query.query)>=2:

            results_first = []
            results_rest = []

            for i in queries_list:
                if inline_query.query.lower() in i[0].lower():
                    if len(inline_query.query) == len(i[0]):
                        results_first.append(i[1])

                    else:
                        results_rest.append(i[1])

            results = list(results_first + results_rest)[:30]

            if results:
                bot.answer_inline_query(inline_query.id, results)

    except Exception as e:
        print(e)

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
                bot.register_next_step_handler(msg, process_drug_search, chat_id)

@message_error_handler()
def process_drug_search(message, chat_id):
    search_query = message.text
    results_list = drug_fda_dict.get(search_query)

    if not results_list:
        bot.send_message(chat_id, drug_not_found)

    else:
        if len(results_list) == 1:
            bot.send_message(chat_id, single_dict_represent_msg(results_list[0]))

        else:

            markup = InlineKeyboardMarkup(row_width=6)

            all_buttons = []
            supportive_text = []
            for result in results_list:
                supportive_text.append(str(result['ApplNo']) + ' → ' + result['Sponsor'] + ' (sponsor)')
                all_buttons.append(InlineKeyboardButton(str(result['ApplNo']) , callback_data= f"search_"+str(result['ApplNo']) ))

            all_buttons_splitted = []
            i = 0
            for _ in all_buttons:
                try:
                    all_buttons_splitted.append([all_buttons[i], all_buttons[i+1]])
                except:
                    if len(all_buttons) % 2 != 0:
                        all_buttons_splitted.append([all_buttons[-1]])
                        break
                    else:
                        break
                i += 2

            for btn in all_buttons_splitted:
                if len(btn) == 2:
                    markup.row(btn[0], btn[1])
                else:
                    markup.row(btn[0])

            bot.send_message(chat_id, multiple_applno_matches + '\n'.join(supportive_text), parse_mode='html', reply_markup=markup)

def single_dict_represent_msg(results_dict):
    return results_dict['Drug'] + '\n---\n' + '\n'.join([f'• {key}' + ': ' + str(value) for key, value in results_dict.items() if not key == 'Drug'])

@bot.callback_query_handler(func=lambda call: True)
@message_error_handler()
def callback_inline(call):
    try:
        if call.message:

            if 'search_' in str(call.data):
                appl_no = str(call.data).split('_')[-1]
                bot.send_message(call.message.chat.id, single_dict_represent_msg(applno_fda_dict.get(appl_no)))

    except Exception as e:
        print(repr(e))


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