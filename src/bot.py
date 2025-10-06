import os
import asyncio
import sys
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
import logging

load_dotenv()

from src.services.services import get_weather, convert_currency

logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

dp = Dispatcher()

# Функция для создания клавиатуры с кнопками
def weather_buttons(city: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Сейчас", callback_data=f"weather_now|{city}"),
            InlineKeyboardButton(text="Сегодня", callback_data=f"weather_today|{city}"),
            InlineKeyboardButton(text="Завтра", callback_data=f"weather_tomorrow|{city}")
        ]
    ])
    return keyboard


@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.reply(
    "Привет! Я Weather & Currency бот.\n"
    "Используй /weather &lt;city&gt; или /convert &lt;amount&gt; &lt;from currency&gt; &lt;to currency&gt;"
)

@dp.message(Command("weather"))
async def weather_cmd(msg: types.Message):
    args = msg.text.split(maxsplit=1)  # разделяем "/weather Moscow" на ['/weather', 'Moscow']
    if len(args) < 2:
        await msg.reply("Укажи город, например: /weather Moscow")
        return
    city = args[1]  # "Moscow"
    
    try:
        data = await get_weather(city)
        print(data)
        await msg.reply(
            f"Погода в {data['city']}:\n{data['temperature_c_now']}°C, {data['description']}",
            reply_markup=weather_buttons(city)  # Добавляем кнопки
        )
    except Exception as e:
        logger.error(f"Weather API error: {e}, city: {city}, user: {msg.from_user.id}")
        await msg.reply("Не удалось получить данные о погоде. Проверь название города и попробуй снова.")

@dp.message(Command("convert"))
async def conver_cmd(msg: types.Message):
    args = msg.text.split()
    if len(args) != 4:
        await msg.reply("Используй формат: /convert &lt;amount&gt; &lt;from currency&gt; &lt;to currency&gt;")
        return
    try:
        amount = float(args[1])
        from_cur = args[2].upper()
        to_cur = args[3].upper()
        converted = await convert_currency(from_cur, to_cur, amount)
        await msg.reply(f"{amount} {from_cur.upper()} = {converted:.2f} {to_cur.upper()}")

    except ValueError as e:
        logger.warning(f"Invalid number format: {e}, user: {msg.from_user.id}, input: {msg.text}")
        await msg.reply("Неверный формат числа. Убедись, что сумма - это число.")
    
    except ConnectionError as e:
        logger.error(f"Connection error in currency conversion: {e}")
        await msg.reply("Сервис конвертации временно недоступен. Попробуй позже.")
    
    except Exception as e:
        logger.error(f"Unexpected error in convert command: {e}, user: {msg.from_user.id}, input: {msg.text}")
        await msg.reply("Произошла непредвиденная ошибка. Попробуй еще раз или обратись к администратору.")

async def handle_weather_callback(callback: types.CallbackQuery):

    raw = callback.data or ""
    try:
        action, city = raw.split("|", 1)
    except ValueError:
        await callback.answer("Неправильные данные", show_alert=True)
        return

    await callback.answer()  # закрывает "loading" у кнопки

    weather_data = await get_weather(city)

    if action == "weather_now":
        # Отправить прогноз на сегодня

        await callback.message.answer(f"Погода сегодня: {weather_data['description']}, {weather_data['temperature_c_now']}°C")

    elif action == "weather_today":
        # Отправить прогноз на сегодня

        await callback.message.answer(f"Погода сегодня: {weather_data['temperature_c_today']}")

    elif action == "weather_tomorrow":
        # Отправить прогноз на завтра 

        await callback.message.answer(f"Прогноз на завтра: {weather_data['temperature_c_tomorrow']}")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    default_props = DefaultBotProperties(parse_mode="HTML")

    bot = Bot(token=TOKEN, default=default_props)

    dp.callback_query.register(handle_weather_callback)
    
    # And the run events dispatching
    await dp.start_polling(
        bot, 
        allowed_updates=["message", "callback_query"]
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

