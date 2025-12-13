"""
Простой эхо-бот на aiogram 3.x
Все в одном файле - минимальная структура
"""


import asyncio
import uuid
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode


# ШАГ 1: ВСТАВЬТЕ ВАШ ТОКЕН ЗДЕСЬ ↓
BOT_TOKEN = "8465834662:AAE3UKK1-46C2-LqThduiv3WHGk970Zec4c"


# Создаем объекты бота, диспетчера и роутера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()


# Словарь для хранения информации о фото
photo_storage = {}


# Регистрируем команду /start
@router.message(Command("start"))
async def start_handler(message: Message):
    """Обработчик команды /start"""
    await message.answer(
        "👋 Привет! Я бот для оценки фото!\n"
        "Отправьте мне фото, и я верну его с кнопками лайк/дизлайк!\n\n"
        "Как работает:\n"
        "• 👍 Лайк - покажет всплывающее уведомление\n"
        "• 👎 Дизлайк - отправит текстовое сообщение"
    )


# Обработчик для фото
@router.message(F.photo)
async def photo_handler(message: Message):
    """Обработчик для фото с добавлением кнопок лайк/дизлайк"""
    
    # Получаем file_id самого большого фото
    photo_file_id = message.photo[-1].file_id
    
    # Генерируем уникальный ID для фото
    photo_id = str(uuid.uuid4())[:8]
    
    # Сохраняем информацию о фото
    photo_storage[photo_id] = {
        "file_id": photo_file_id,
        "user_id": message.from_user.id,
        "caption": message.caption or "📸 Ваше фото"
    }
    
    # Создаем клавиатуру с кнопками
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👍 Лайк", callback_data=f"like_{photo_id}"),
                InlineKeyboardButton(text="👎 Дизлайк", callback_data=f"dislike_{photo_id}")
            ]
        ]
    )
    
    # Отправляем фото с кнопками
    caption = message.caption if message.caption else "📸 Ваше фото с оценкой"
    await message.answer_photo(
        photo_file_id,
        caption=caption,
        reply_markup=keyboard
    )


# Обработчик для кнопки Лайк
@router.callback_query(F.data.startswith("like_"))
async def like_callback_handler(callback_query: CallbackQuery):
    """Обработчик для кнопки Лайк"""
    
    # Извлекаем photo_id из callback_data
    photo_id = callback_query.data.replace("like_", "")
    
    # Проверяем существование фото
    if photo_id in photo_storage:
        # Отправляем всплывающее уведомление
        await callback_query.answer(
            "Спасибо за лайк! ❤️",
            show_alert=False
        )
        
        # Меняем кнопку после нажатия
        updated_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="✅ Вы лайкнули!", callback_data=f"liked_{photo_id}"),
                    InlineKeyboardButton(text="👎 Дизлайк", callback_data=f"dislike_{photo_id}")
                ]
            ]
        )
        
        # Обновляем клавиатуру в сообщении
        try:
            await callback_query.message.edit_reply_markup(reply_markup=updated_keyboard)
        except:
            pass
    else:
        await callback_query.answer("Фото больше не доступно!", show_alert=True)


# Обработчик для кнопки Дизлайк
@router.callback_query(F.data.startswith("dislike_"))
async def dislike_callback_handler(callback_query: CallbackQuery):
    """Обработчик для кнопки Дизлайк"""
    
    photo_id = callback_query.data.replace("dislike_", "")
    
    if photo_id in photo_storage:
        # Отправляем текстовое сообщение в чат
        await callback_query.message.answer(
            f"Очень жаль, что вам не понравилось фото 😢\n"
            f"Может быть, следующее понравится больше!"
        )
        
        # Меняем кнопку после нажатия
        updated_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="👍 Лайк", callback_data=f"like_{photo_id}"),
                    InlineKeyboardButton(text="❌ Вы дизлайкнули", callback_data=f"disliked_{photo_id}")
                ]
            ]
        )
        
        # Обновляем клавиатуру
        try:
            await callback_query.message.edit_reply_markup(reply_markup=updated_keyboard)
        except:
            pass
        
        # Подтверждаем обработку нажатия
        await callback_query.answer()
    else:
        await callback_query.answer("Фото больше не доступно!", show_alert=True)


# Дополнительные обработчики для уже оцененных фото
@router.callback_query(F.data.startswith("liked_"))
async def already_liked_handler(callback_query: CallbackQuery):
    await callback_query.answer("Вы уже лайкнули это фото! 👍", show_alert=False)


@router.callback_query(F.data.startswith("disliked_"))
async def already_disliked_handler(callback_query: CallbackQuery):
    await callback_query.answer("Вы уже дизлайкнули это фото! 👎", show_alert=False)


# Обработчик для текстовых сообщений
@router.message(F.text)
async def text_handler(message: Message):
    await message.answer(f"📝 Вы сказали: {message.text}\n\nОтправьте фото, чтобы протестировать кнопки!")


async def main():
    """Основная функция запуска бота"""
    print("🚀 Бот запускается...")
    
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    
    print("✅ Бот запущен!")
    print("📱 Откройте Telegram и найдите вашего бота")
    print("⏹️  Для остановки нажмите Ctrl+C")
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен")
