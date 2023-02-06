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
welcome_message = 'Hello! Send me a PMID or DOI like this:\n\n22012259\n10.1007/s10741-019-09825-x'

# Errors and developers
error_for_developer = 'An error occurred for this user, plz take a look at bot logs and tracebacks'
developer = credentials['developer_tag_name']
error_with_developer = f"An error occurred, plz contact {developer} for further instructions"
developer_chat_id = credentials['developer_chat_id']