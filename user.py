from pyrogram import Client
import config
import asyncio
from main import bot
import random
client = Client("fsfdsf", config.API_ID, config.API_HASH)
client.start()
# 
async def get_chats():
    list = []
    async for dialog in client.iter_dialogs():
        if dialog.chat.type == 'supergroup':
            list.append({'title' : dialog.chat.first_name or dialog.chat.title, 'id' : dialog.chat.id})
    return list
# 
async def leave_from_channel(id):
    try:
        await client.leave_chat(id)
        return True
    except:
        return False
# 
async def spamming(spam_list, settings, db):
    while settings[4] == 1: # БЕСКОНЕЧНЫЙ ЦИКЛ
        for chat in spam_list: # ПРОХОДИТ ПО ВСЕМ ЧАТАМ
            settings = db.settings()
            try:
                if settings[1] != '':
                    await client.send_photo(chat['id'], settings[1], caption=f"{settings[2]}\n\n{chat['text']}",parse_mode="HTML")
                    await bot.send_message(config.ADMIN, f'[LOG] Cообщение в {chat["title"]} было успешно отправленно.')
                else:
                    await client.send_message(chat['id'], f"{settings[2]}\n\n{chat['text']}")
            except Exception as e:
                try:
                    await client.send_message(chat['id'], f"{settings[2]}\n\n{chat['text']}")
                    await bot.send_message(config.ADMIN, f'[LOG] Cообщение в {chat["title"]} было успешно отправленно.')
                except Exception as e:
                    await bot.send_message(config.ADMIN, f'[LOG] Cообщение в {chat["title"]} не было отправлено из-за ошибки: {e}')
            await asyncio.sleep(random.randint(1,5)) # ПОСЛЕ КАЖДОГО ЧАТА СПИТ 2 СЕКУНДЫ
        # КОГДА ЦИКЛ ЗАВЕРШАЕТСЯ БОТ ЛОЖИТСЯ СПАТЬ НА УКАЗАННОЕ ТОБОЙ ВРЕМЯ
        await asyncio.sleep(settings[5]*60)
        if settings[4] != 1:
            break
        # ПРОЦЕДУРА ОПЯТЬ ПОВТОРЯЕТСЯ