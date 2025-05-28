from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
import asyncio
import logging

API_TOKEN = '8094183993:AAErYMPxP-ODVDgMBJb01AZjdi3w5WbNIis'  
RESPONSIBLE_USERNAME = '@ZaGLSklad'  

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

pending_requests = {}

@dp.message_handler(commands=['запрос'])
async def handle_request(message: Message):
    detail = message.get_args()
    if not detail:
        await message.reply("Укажите номер детали. Пример: /запрос 123456")
        return

    reply = await message.reply(
        f"Запрос детали: {detail}\nОтветственный: {RESPONSIBLE_USERNAME}\n⏳ Ожидаем ответ..."
    )
    pending_requests[reply.message_id] = (message.chat.id, detail)

    await asyncio.sleep(600)  # 10 минут
    if reply.message_id in pending_requests:
        await message.answer(
            f"🔁 Напоминание: запрошена деталь {detail}\n{RESPONSIBLE_USERNAME}, проверь, пожалуйста!"
        )

@dp.message_handler()
async def handle_response(message: Message):
    for msg_id in list(pending_requests):
        if str(pending_requests[msg_id][1]) in message.text:
            del pending_requests[msg_id]

if __name__ == '__main__':
    executor.start_polling(dp)
