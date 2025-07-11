import logging
import os
from datetime import datetime

import aiohttp
from dotenv import load_dotenv
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.ext import (
    Application,
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

load_dotenv()
BOT_TOKEN = os.getenv("TOKEN")
API_URL = os.getenv("API_URL")
USER_API_URL = os.getenv("USER_API_URL")

if not BOT_TOKEN or not API_URL:
    raise ValueError("Отсутствует TOKEN или API_URL в .env файле")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main_keyboard():
    return ReplyKeyboardMarkup([["Подробности"]], resize_keyboard=True)


async def start(update: Update, context: CallbackContext) -> None:
    """Приветственное сообщение и регистрация пользователя."""
    user = update.effective_user
    user_data = {
        "user_id": str(user.id),
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "subscribed": True,
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                USER_API_URL, json=user_data, headers={"Bot-Token": BOT_TOKEN}
            ) as response:
                response.raise_for_status()
        except aiohttp.ClientResponseError as e:
            logger.error(
                f"Ошибка регистрации пользователя: {e.status}, "
                f"пользователь с user_id {user_data['user_id']} уже существует."
            )
        except Exception as e:
            logger.error(f"Сетевая ошибка: {e}")

    await update.message.reply_text(
        f"Спасибо, что вы включили меня, {user_data['first_name']}! "
        f"Я бот мероприятий. Используй кнопку Подробности,"
        f"чтобы узнать ближайшие события!",
        reply_markup=main_keyboard(),
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
            await update.message.reply_text(
                "Ошибка получения данных, попробуйте позже."
            )
            return

    if not events:
        await update.message.reply_text(
            "Скоро будут новые мероприятия, следите за обновлениями!"
        )
        return

    for event in events[:5]:
        keyboard = [
            [InlineKeyboardButton("📖 Описание", callback_data=f"desc_{event['id']}")],
            [
                InlineKeyboardButton(
                    "🗓 Дата и время", callback_data=f"date_{event['id']}"
                )
            ],
            [
                InlineKeyboardButton(
                    "📍 Место проведения", callback_data=f"loc_{event['id']}"
                )
            ],
            [
                InlineKeyboardButton(
                    "🏢 Компания организатор", callback_data=f"comp_{event['id']}"
                )
            ],
            [
                InlineKeyboardButton(
                    "👗 Дресс-код", callback_data=f"dress_{event['id']}"
                )
            ],
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

    # Парсинг и форматирование даты и времени
    date_time_str = event["date_time"]
    date_time_obj = datetime.fromisoformat(date_time_str)
    formatted_date_time = date_time_obj.strftime("%d.%m.%Y в %H:%M")

    fields_map = {
        "desc": f"📖 Описание:\n{event['description']}",
        "date": f"🗓 Дата и время:\n{formatted_date_time}",
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
    app.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^Подробности$"), get_events)
    )
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
