import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN, WEATHER_API_KEY, NASA_API_KEY, CAT_API_KEY
import requests
from datetime import datetime, timedelta
import random

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Главное меню с кнопками
async def get_main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Кошки", callback_data="cats")],
        [InlineKeyboardButton(text="Погода в Москве", callback_data="weather")],
        [InlineKeyboardButton(text="Космос", callback_data="space")]
    ])

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Добро пожаловать! Выберите действие:", reply_markup=await get_main_menu())

@dp.message(Command("help"))
async def help_command(message: Message):
    help_text = (
        "/start - Главное меню\n"
        "/help - Список команд\n"
        "Кнопки:\n"
        "Кошки - Получить случайное изображение кошки\n"
        "Погода в Москве - Узнать текущую погоду в Москве\n"
        "Космос - Получить случайное изображение дня из NASA"
    )
    await message.answer(help_text)

# Обработчик кнопки "Кошки"
def get_random_cat():
    try:
        url = "https://api.thecatapi.com/v1/images/search"
        headers = {"x-api-key": CAT_API_KEY}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()[0]['url']
        return ""
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к The Cat API: {e}")
        return ""

@dp.callback_query(F.data == "cats")
async def cats_handler(callback: CallbackQuery):
    await callback.answer()  # Быстрый ответ, чтобы избежать истечения времени
    cat_image_url = get_random_cat()
    if cat_image_url:
        await callback.message.answer_photo(photo=cat_image_url, caption="Милый котик для вас! 🐱")
    else:
        await callback.message.answer("Не удалось получить изображение котика. Попробуйте позже.")

# Обработчик кнопки "Погода в Москве"
def mypogoda(city_name, units):
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units={units}'
        response = requests.get(url, timeout=10)
        data = response.json()
        stroka = ''
        if response.status_code == 200:
            stroka = f"Погода в {city_name}: \nТемпература: {data['main']['temp']}°C \nВлажность: {data['main']['humidity']}% \nОписание: {data['weather'][0]['description']}"
        else:
            stroka = f"Ошибка: {data['message']}"
        return stroka
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к OpenWeather API: {e}")
        return "Не удалось получить данные о погоде."

@dp.callback_query(F.data == "weather")
async def weather_handler(callback: CallbackQuery):
    await callback.answer()  # Быстрый ответ для Telegram
    city_name = 'Moscow'
    units = 'metric'
    weather_info = mypogoda(city_name, units)
    await callback.message.answer(weather_info)

# Обработчик кнопки "Космос"
def get_random_apod():
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        random_date = start_date + (end_date - start_date) * random.random()
        date_str = random_date.strftime("%Y-%m-%d")

        url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date_str}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data['url'], data['title']
        return None, None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к NASA API: {e}")
        return None, None

@dp.callback_query(F.data == "space")
async def space_handler(callback: CallbackQuery):
    await callback.answer()  # Быстрый ответ для Telegram
    photo_url, title = get_random_apod()
    if photo_url:
        await callback.message.answer_photo(photo=photo_url, caption=f"{title}")
    else:
        await callback.message.answer("Не удалось получить изображение космоса. Попробуйте позже.")

# Запуск бота
async def main():
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
