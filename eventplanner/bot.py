import os
import aiohttp
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv('TOKEN')
API_URL = os.getenv('API_URL')
USER_API_URL = os.getenv('USER_API_URL')

# Проверка наличия необходимых переменных окружения
if not BOT_TOKEN or not API_URL:
    raise ValueError("Отсутствует TOKEN или API_URL в .env файле")

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main_keyboard():
    return ReplyKeyboardMarkup([['/events']], resize_keyboard=True)

async def start(update: Update, context: CallbackContext) -> None:
    """Приветственное сообщение и регистрация пользователя."""
    user = update.effective_user
    user_data = {
        "user_id": str(user.id),
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "subscribed": True
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(USER_API_URL, json=user_data) as response:
                response.raise_for_status()
        except Exception as e:
            logger.error(f"Ошибка регистрации пользователя: {e}")
    
    await update.message.reply_text(
        "Привет! Я бот мероприятий. Используй /events, чтобы узнать ближайшие события!",
        reply_markup=main_keyboard()
    )

async def get_events(update: Update, context: CallbackContext) -> None:
    """Получает и отправляет список событий с кнопками."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(API_URL) as response:
                response.raise_for_status()
                events = await response.json()
        except Exception as e:
            logger.error(f"Ошибка получения событий: {e}")
            await update.message.reply_text("Ошибка получения данных, попробуйте позже.")
            return

    if not events:
        await update.message.reply_text("Скоро будут новые мероприятия, следите за обновлениями!")
        return

    for event in events[:5]:  # Ограничим 5 событиями
        keyboard = [
            [InlineKeyboardButton("📖 Описание", callback_data=f"desc_{event['id']}")],
            [InlineKeyboardButton("🗓 Дата и время", callback_data=f"date_{event['id']}")],
            [InlineKeyboardButton("📍 Локация", callback_data=f"loc_{event['id']}")],
            [InlineKeyboardButton("🏢 Компания", callback_data=f"comp_{event['id']}")],
            [InlineKeyboardButton("👗 Дресс-код", callback_data=f"dress_{event['id']}")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"📌 *{event['title']}*", parse_mode="Markdown", reply_markup=reply_markup
        )

async def button_handler(update: Update, context: CallbackContext) -> None:
    """Обработчик кнопок."""
    query = update.callback_query
    await query.answer()
    
    field, event_id = query.data.split("_", 1)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{API_URL}{event_id}/") as response:
                response.raise_for_status()
                event = await response.json()
        except Exception as e:
            logger.error(f"Ошибка получения информации о событии: {e}")
            await query.message.reply_text("Ошибка получения данных!")
            return
    
    fields_map = {
        "desc": f"📖 Описание:\n{event['description']}",
        "date": f"🗓 Дата и время:\n{event['date_time']}",
        "loc": f"📍 Локация:\n{event['location']}",
        "comp": f"🏢 Компания:\n{event['company_info']}",
        "dress": f"👗 Дресс-код:\n{event['dress_code']}",
    }
    
    if field in fields_map:
        await query.message.reply_text(fields_map[field])

def main():
    """Запуск бота."""
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("events", get_events))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    logger.info("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
