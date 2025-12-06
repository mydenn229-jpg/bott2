import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

a = "8465834662:AAE3UKK1-46C2-LqThduiv3WHGk970Zec4c"

bot = Bot(token=a)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer('Hello!')

@dp.message(Command('hi'))
async def cmd_hi(message: types.Message):
    await message.answer('привэт')

@dp.message(Command('help'))
async def cmd_help(message: types.Message):
    h_txt = """
    Доступные команды:
    /start - Начать работу
    /hi - Поздоровайтесь
    /random - Рандомное число
    /help - Помощь
"""
    await message.answer(h_txt)

@dp.message(Command('random'))
async def cmd_random(message: types.Message):
    x = random.randint(1, 10000)
    await message.answer(f'Хмм... Твоё случайное число: {x}')

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())