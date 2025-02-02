import requests
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# Конфигурация
API_URL = "http://127.0.0.1:8000/api/events/"  # URL API
BOT_TOKEN = ""  # Вставьте ваш токен

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    requests.post("http://127.0.0.1:8000/api/users/", json=user_data)
    
    await update.message.reply_text("Привет! Я бот мероприятий. Используй /events, чтобы узнать ближайшие события!")

async def get_events(update: Update, context: CallbackContext) -> None:
    """Получает и отправляет список событий с кнопками."""
    response = requests.get(API_URL)
    if response.status_code == 200:
        events = response.json()
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
            await update.message.reply_text(f"📌 *{event['title']}*", parse_mode="Markdown", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Ошибка получения данных, попробуйте позже.")

async def button_handler(update: Update, context: CallbackContext) -> None:
    """Обработчик кнопок."""
    query = update.callback_query
    await query.answer()
    
    event_id, field = query.data.split("_")[1], query.data.split("_")[0]
    response = requests.get(f"{API_URL}{event_id}/")
    
    if response.status_code == 200:
        event = response.json()
        fields_map = {
            "desc": f"📖 Описание:\n{event['description']}",
            "date": f"🗓 Дата и время:\n{event['date_time']}",
            "loc": f"📍 Локация:\n{event['location']}",
            "comp": f"🏢 Компания:\n{event['company_info']}",
            "dress": f"👗 Дресс-код:\n{event['dress_code']}",
        }
        
        if field in fields_map:
            await query.message.reply_text(fields_map[field])
    else:
        await query.message.reply_text("Ошибка получения данных!")

def main():
    """Запуск бота."""
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("events", get_events))
    app.add_handler(CallbackQueryHandler(button_handler))  # Обработка нажатий кнопок
    
    app.run_polling()

if __name__ == "__main__":
    main()
