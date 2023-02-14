import json
from pathlib import Path
import os

with open (os.path.join(os.getcwd(), 'configs', 'creds_and_tokens.json')) as f:
    credentials = json.load(f)


# telegram token
TOKEN = credentials.get('telegram_token')

# spam_defender_files
with open(os.path.join(os.getcwd(), 'spam_defender_files', 'banned_list.json')) as f:
    banned_list = json.load(f)

banned_message = f'Sorry, but you\'ve been banned for spamming'
welcome_message = 'Hello! I\'m a FDA (Food and Drug Administration) searching bot: send me the drug name like this:\n@<bot_username> phesgo'
drug_not_found = 'Entered drug was not found; make sure to use inline search (@<bot_user_name>) to get available data'
multiple_applno_matches = 'Following FDA applications matched your search: in other words, here is a list of all applNos with your drug, choose one :)\n\n'

# Errors and developers
error_for_developer = 'An error occurred for this user, plz take a look at bot logs and tracebacks'
developer = credentials['developer_tag_name']
error_with_developer = f"An error occurred, plz contact {developer} for further instructions"
developer_chat_id = credentials['developer_chat_id']