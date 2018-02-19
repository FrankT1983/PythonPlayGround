from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty


api_id = 1234
api_hash = 'hash here'

phone = 'phon number'
username = 'user'

client = TelegramClient(username, api_id, api_hash)
client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone)
    try:
        client.sign_in(phone, input('Enter the code: '))
    except Exception:
        client.sign_in(password=input('Password: '))



me = client.get_me()
print(me)

chats = client.get_dialogs()

for c in chats:
    chatname = str(c.name);
    print(chatname)
    if ("Konrad" in chatname):
         messages = client.get_message_history(c.entity)

         for m in messages :
             print(str(m))


