from telethon import TelegramClient, events

def xor_cipher(text, key="secret"):
    return "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))

ENCRYPTED_API_ID = 'AT[D]@E\\'
ENCRYPTED_API_HASH = 'DT\x02\x16R\x15A\x01VET\x16\x17W\x00\x11UBK\x01\x07A]DF\x03UA\x06A\x16V'

API_ID = int(xor_cipher(ENCRYPTED_API_ID))
API_HASH = xor_cipher(ENCRYPTED_API_HASH)

SESSION_NAME = "my_session"
AUTO_REPLY_TEXT = "Привет! Я сейчас не в сети."
replied_users = set()

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    if event.is_private:
        sender_id = event.sender_id

        me = await client.get_me()
        status = await client.get_entity(me.id)

        if status.status.__class__.__name__ in ["UserStatusOffline", "UserStatusRecently"]:
            if sender_id not in replied_users:
                await event.reply(AUTO_REPLY_TEXT)
                replied_users.add(sender_id)

async def main():
    await client.start()
    print("Автоответчик запущен!")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())