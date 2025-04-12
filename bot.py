import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "7680848123:AAHqNizmx3hOXmjVOmzdnwQCenlXHTWX8OA"  # Ваш токен
ADMIN_CHAT_ID = '5498505652'  # Заміни на свій Telegram ID

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
        ("📍 вул. Лугова 9", "https://maps.google.com/?q=50.425689,30.483118", "1850 грн"),
        ("📍 вул. Плодова 1", "https://maps.google.com/?q=50.400233,30.457452", "1800 грн"),
        ("📍 вул. Дегтярівська 21", "https://maps.google.com/?q=50.457832,30.480274", "1900 грн"),
        ("📍 вул. Сім'ї Сосніних 3", "https://maps.google.com/?q=50.434291,30.464987", "1700 грн"),
        ("📍 пр-т Лобановського 119", "https://maps.google.com/?q=50.426594,30.495850", "2000 грн"),
        ("📍 вул. Сортувальна 5", "https://maps.google.com/?q=50.464835,30.490526", "2100 грн"),
        ("📍 вул. Пухівська 4А", "https://maps.google.com/?q=50.422968,30.510332", "2200 грн"),
        ("📍 вул. Новокостянтинівська 18", "https://maps.google.com/?q=50.438151,30.497368", "2100 грн"),
        ("📍 вул. Бальзака 85А", "https://maps.google.com/?q=50.395106,30.455319", "2000 грн"),
        ("📍 вул. Будіндустрії 5", "https://maps.google.com/?q=50.476872,30.464531", "1900 грн"),
        ("📍 вул. Бориспільська 9", "https://maps.google.com/?q=50.446179,30.476200", "1850 грн"),
        ("📍 вул. Віскозна 1", "https://maps.google.com/?q=50.453824,30.487111", "1750 грн"),
        ("📍 вул. Промислова 4", "https://maps.google.com/?q=50.425598,30.508532", "1800 грн")
    ]

    for loc, link, price in locations:
        keyboard.add(types.InlineKeyboardButton(text=f"{loc} - {price}", url=link))

    await message.answer("Оберіть локацію для перегляду на карті:", reply_markup=keyboard)

# Оренда контейнера
@dp.message_handler(lambda message: message.text == "📦 Орендувати контейнер")
async def rent_container(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📍 Перегляд локацій", "📞 Зв'язатися з нами")

    await message.answer("Оберіть локацію для оренди контейнера:", reply_markup=keyboard)
    user_data[message.from_user.id] = {'state': 'select_location'}

# Локація вибрана
@dp.message_handler(lambda message: message.text in ["📍 вул. Лугова 9", "📍 вул. Плодова 1", "📍 вул. Дегтярівська 21", 
                                                   "📍 вул. Сім'ї Сосніних 3", "📍 пр-т Лобановського 119", 
                                                   "📍 вул. Сортувальна 5", "📍 вул. Пухівська 4А", 
                                                   "📍 вул. Новокостянтинівська 18", "📍 вул. Бальзака 85А", 
                                                   "📍 вул. Будіндустрії 5", "📍 вул. Бориспільська 9", 
                                                   "📍 вул. Віскозна 1", "📍 вул. Промислова 4"])
async def location_chosen(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("5 футів", "7.5 футів", "15 футів", "30 футів")
    
    await message.answer(f"Ви вибрали локацію: {message.text}. Оберіть розмір контейнера:", reply_markup=keyboard)
    user_data[message.from_user.id]['location'] = message.text
    user_data[message.from_user.id]['state'] = 'select_size'

# Вибір розміру контейнера
@dp.message_handler(lambda message: message.text in ["5 футів", "7.5 футів", "15 футів", "30 футів"])
async def select_container_size(message: types.Message):
    user_data[message.from_user.id]['size'] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("1 місяць", "3 місяці", "6 місяців", "12 місяців")

    await message.answer("Оберіть термін оренди (в місяцях):", reply_markup=keyboard)
    user_data[message.from_user.id]['state'] = 'select_term'

# Вибір терміну оренди
@dp.message_handler(lambda message: message.text in ["1 місяць", "3 місяці", "6 місяців", "12 місяців"])
async def select_rent_term(message: types.Message):
    user_data[message.from_user.id]['term'] = message.text
    await message.answer("Введіть ваше ім'я:")
    user_data[message.from_user.id]['state'] = 'enter_name'

# Введення імені
@dp.message_handler(state='enter_name')
async def enter_name(message: types.Message):
    user_data[message.from_user.id]['name'] = message.text
    await message.answer("Поділіться номером або введіть вручну:")
    user_data[message.from_user.id]['state'] = 'enter_phone'

# Введення номеру телефону
@dp.message_handler(state='enter_phone', content_types=[types.ContentType.CONTACT, types.ContentType.TEXT])
async def enter_phone(message: types.Message):
    phone_number = message.text if message.contact is None else message.contact.phone_number
    user_data[message.from_user.id]['phone'] = phone_number

    location = user_data[message.from_user.id]['location']
    size = user_data[message.from_user.id]['size']
    term = user_data[message.from_user.id]['term']
    name = user_data[message.from_user.id]['name']

    # Формуємо заявку
    text = f"Заявка на оренду контейнера:\n" \
           f"Ім'я: {name}\n" \
           f"Телефон: {phone_number}\n" \
           f"Локація: {location}\n" \
           f"Розмір контейнера: {size}\n" \
           f"Термін оренди: {term}"

    await bot.send_message(ADMIN_CHAT_ID, text)
    await message.answer("Дякуємо! Ваша заявка відправлена.")
    await message.answer("Оберіть опцію нижче:", reply_markup=types.ReplyKeyboardMarkup(
        resize_keyboard=True, keyboard=[["📦 Орендувати контейнер", "📍 Перегляд локацій"]]))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
