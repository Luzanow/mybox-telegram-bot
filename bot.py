import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "7680848123:AAHqNizmx3hOXmjVOmzdnwQCenlXHTWX8OA"
ADMIN_CHAT_ID = '5498505652'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}

# Старт
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📦 Орендувати контейнер", "📍 Перегляд локацій", "📞 Зв'язатися з нами")
    await message.answer("🖐 Вітаємо у MyBox!\nОберіть опцію нижче:", reply_markup=keyboard)

# Перегляд локацій
@dp.message_handler(lambda message: message.text == "📍 Перегляд локацій")
async def view_locations(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    locations = [
        ("📍 вул. Лугова 9", "https://maps.google.com/?q=50.425689,30.483118"),
        ("📍 вул. Плодова 1", "https://maps.google.com/?q=50.400233,30.457452"),
        ("📍 вул. Дегтярівська 21", "https://maps.google.com/?q=50.457832,30.480274"),
        ("📍 вул. Сім'ї Сосніних 3", "https://maps.google.com/?q=50.434291,30.464987"),
        ("📍 пр-т Лобановського 119", "https://maps.google.com/?q=50.426594,30.495850"),
        ("📍 вул. Сортувальна 5", "https://maps.google.com/?q=50.464835,30.490526"),
        ("📍 вул. Пухівська 4А", "https://maps.google.com/?q=50.422968,30.510332"),
        ("📍 вул. Новокостянтинівська 18", "https://maps.google.com/?q=50.438151,30.497368"),
        ("📍 вул. Бальзака 85А", "https://maps.google.com/?q=50.395106,30.455319"),
        ("📍 вул. Будіндустрії 5", "https://maps.google.com/?q=50.476872,30.464531"),
        ("📍 вул. Бориспільська 9", "https://maps.google.com/?q=50.446179,30.476200"),
        ("📍 вул. Віскозна 1", "https://maps.google.com/?q=50.453824,30.487111"),
        ("📍 вул. Промислова 4", "https://maps.google.com/?q=50.425598,30.508532")
    ]

    for loc, link in locations:
        keyboard.add(types.InlineKeyboardButton(text=loc, url=link))

    await message.answer("Оберіть локацію для перегляду на карті:", reply_markup=keyboard)

# Оренда контейнера
@dp.message_handler(lambda message: message.text == "📦 Орендувати контейнер")
async def rent(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("5 футів", "7.5 футів", "15 футів", "30 футів")
    await message.answer("Оберіть розмір контейнера:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in ["5 футів", "7.5 футів", "15 футів", "30 футів"])
async def select_location(message: types.Message):
    user_data[message.from_user.id] = {"size": message.text}
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("📍 вул. Лугова 9", "📍 вул. Плодова 1", "📍 вул. Дегтярівська 21", "📍 вул. Сім'ї Сосніних 3", "📍 пр-т Лобановського 119")
    keyboard.add("📍 вул. Сортувальна 5", "📍 вул. Пухівська 4А", "📍 вул. Новокостянтинівська 18", "📍 вул. Бальзака 85А", "📍 вул. Будіндустрії 5")
    keyboard.add("📍 вул. Бориспільська 9", "📍 вул. Віскозна 1", "📍 вул. Промислова 4")
    await message.answer("Оберіть локацію:", reply_markup=keyboard)

# Вибір локації
@dp.message_handler(lambda message: message.text.startswith("📍"))
async def select_duration(message: types.Message):
    user_data[message.from_user.id]["location"] = message.text
    await message.answer("Оберіть термін оренди (в місяцях):", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(lambda message: message.text.isdigit())
async def get_name(message: types.Message):
    user_data[message.from_user.id]["months"] = int(message.text)
    await message.answer("Введіть ваше ім'я:")

@dp.message_handler(lambda message: message.text.isalpha())
async def get_phone(message: types.Message):
    user_data[message.from_user.id]["name"] = message.text
    await message.answer("Введіть ваш номер телефону:")

@dp.message_handler(lambda message: "+" in message.text or message.text.isdigit())
async def finish(message: types.Message):
    uid = message.from_user.id
    user_data[uid]["phone"] = message.text
    size = user_data[uid]["size"]
    months = user_data[uid]["months"]
    name = user_data[uid]["name"]
    phone = user_data[uid]["phone"]
    location = user_data[uid]["location"]

    prices = {
        "5 футів": 1850,
        "7.5 футів": 2350,
        "15 футів": 3800,
        "30 футів": 6650
    }

    price = prices[size] * months
    total = price  # без знижки

    text = f"✅ Нова заявка:\n👤 Ім'я: {name}\n📞 Телефон: {phone}\n📦 Контейнер: {size}\n📍 Локація: {location}\n📅 Місяців: {months}\n💰 Сума: {total} грн"

    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
    await message.answer("✅ Дякуємо! Ваша заявка відправлена.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
