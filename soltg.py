import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from config import TOKEN,WEATHER_API_KEY,NASA_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Задание 1: Простое меню с кнопками "Привет" и "Пока"
def get_greeting_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Привет", callback_data="greet")],
        [InlineKeyboardButton(text="Пока", callback_data="bye")]
    ])

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Выберите действие:", reply_markup=get_greeting_keyboard())

@dp.callback_query(F.data == "greet")
async def greet(callback: CallbackQuery):
    await callback.message.answer(f"Привет, {callback.from_user.first_name}!")
    await callback.answer()

@dp.callback_query(F.data == "bye")
async def bye(callback: CallbackQuery):
    await callback.message.answer(f"До свидания, {callback.from_user.first_name}!")
    await callback.answer()

# Задание 2: Кнопки с URL-ссылками
@dp.message(Command("links"))
async def links(message: Message):
    links_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Новости", url="https://news.ycombinator.com/")],
        [InlineKeyboardButton(text="Музыка", url="https://www.spotify.com/")],
        [InlineKeyboardButton(text="Видео", url="https://www.youtube.com/")]
    ])
    await message.answer("Выберите ссылку:", reply_markup=links_keyboard)

# Задание 3: Динамическое изменение клавиатуры
@dp.message(Command("dynamic"))
async def dynamic(message: Message):
    dynamic_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
    ])
    await message.answer("Динамическая клавиатура:", reply_markup=dynamic_keyboard)

@dp.callback_query(F.data == "show_more")
async def show_more(callback: CallbackQuery):
    more_options_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Опция 1", callback_data="option_1")],
        [InlineKeyboardButton(text="Опция 2", callback_data="option_2")]
    ])
    await callback.message.edit_text("Выберите опцию:", reply_markup=more_options_keyboard)
    await callback.answer()

@dp.callback_query(F.data.func(lambda data: data in ["option_1", "option_2"]))
async def handle_option(callback: CallbackQuery):
    option = "Опция 1" if callback.data == "option_1" else "Опция 2"
    await callback.message.answer(f"Вы выбрали: {option}")
    await callback.answer()

# Команда /help для отображения списка доступных команд
@dp.message(Command("help"))
async def help_command(message: Message):
    help_text = (
        "/start - Показать меню с кнопками Привет и Пока\n"
        "/links - Показать кнопки с URL-ссылками\n"
        "/dynamic - Динамическая клавиатура\n"
        "/help - Список команд"
    )
    await message.answer(help_text)

# Запуск бота
async def main():
   print("Бот запущен")
   await dp.start_polling(bot)

if __name__ == "__main__":
   # Запуск бота
    asyncio.run(main())
