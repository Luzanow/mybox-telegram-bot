import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "7680848123:AAHmbEGQ49ZB8SXTGof4l3mbZ9vcIbuV_6k"
ADMIN_CHAT_ID = "@Luzanow"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}

# Старт
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        types.KeyboardButton("📦 Орендувати контейнер"),
        types.KeyboardButton("📍 Локації"),
        types.KeyboardButton("📞 Зв'язатися з нами")
    )
    await message.answer("🖐 Вітаємо у MyBox!", reply_markup=keyboard)
    await message.answer("Оберіть опцію нижче:")

# Локації
@dp.message_handler(lambda msg: msg.text == "📍 Локації")
async def send_locations(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    locations = [
        ("📍 вул. Лугова 9", "https://www.google.com/maps?q=вул.+Лугова+9"),
        ("📍 вул. Плодова 1", "https://www.google.com/maps?q=вул.+Плодова+1"),
        ("📍 вул. Дегтярівська 21", "https://www.google.com/maps?q=вул.+Дегтярівська+21"),
        ("📍 вул. Сім'ї Сосніних 3", "https://www.google.com/maps?q=вул.+Сім'ї+Сосніних+3"),
        ("📍 пр-т Лобановського 119", "https://www.google.com/maps?q=Лобановського+119"),
        ("📍 вул. Сортувальна 5", "https://www.google.com/maps?q=вул.+Сортувальна+5"),
        ("📍 вул. Пухівська 4А", "https://www.google.com/maps?q=вул.+Пухівська+4А"),
        ("📍 вул. Новокостянтинівська 18", "https://www.google.com/maps?q=вул.+Новокостянтинівська+18"),
        ("📍 вул. Бальзака 85А", "https://www.google.com/maps?q=вул.+Бальзака+85А"),
        ("📍 вул. Будіндустрії 5", "https://www.google.com/maps?q=вул.+Будіндустрії+5"),
        ("📍 вул. Бориспільська 9", "https://www.google.com/maps?q=вул.+Бориспільська+9"),
        ("📍 вул. Віскозна 1", "https://www.google.com/maps?q=вул.+Віскозна+1"),
        ("📍 вул. Промислова 4", "https://www.google.com/maps?q=вул.+Промислова+4")
    ]
    for name, url in locations:
        keyboard.add(types.InlineKeyboardButton(name, url=url))
    await message.answer("Оберіть локацію:", reply_markup=keyboard)

# Контакт
@dp.message_handler(lambda msg: msg.text == "📞 Зв'язатися з нами")
async def contact(message: types.Message):
    await message.answer("📞 Телефон: +38 095 93 87 317\n📧 Email: myboxua55@gmail.com")

# Оренда
@dp.message_handler(lambda msg: msg.text == "📦 Орендувати контейнер")
async def rent_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    keyboard.add("5 футів", "7.5 футів", "15 футів", "30 футів")
    await message.answer("Оберіть розмір контейнера:", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text in ["5 футів", "7.5 футів", "15 футів", "30 футів"])
async def ask_months(message: types.Message):
    user_data[message.from_user.id] = {"size": message.text}
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=4)
    keyboard.add(*[str(i) for i in range(1, 13)])
    await message.answer("Оберіть термін оренди (в місяцях):", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text.isdigit() and 0 < int(msg.text) <= 12)
async def ask_name(message: types.Message):
    user_data[message.from_user.id]["months"] = int(message.text)
    await message.answer("Введіть ваше ім'я:")

@dp.message_handler(lambda msg: msg.text.isalpha())
async def ask_phone(message: types.Message):
    user_data[message.from_user.id]["name"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton("📱 Поділитись номером телефону", request_contact=True))
    await message.answer("Поділіться номером або введіть вручну:", reply_markup=keyboard)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def confirm_phone(message: types.Message):
    user_data[message.from_user.id]["phone"] = message.contact.phone_number
    await send_summary(message)

@dp.message_handler(lambda msg: msg.text.startswith("+") or msg.text.replace(" ", "").isdigit())
async def confirm_manual_phone(message: types.Message):
    user_data[message.from_user.id]["phone"] = message.text
    await send_summary(message)

async def send_summary(message):
    uid = message.from_user.id
    data = user_data[uid]
    size = data["size"]
    months = data["months"]
    name = data["name"]
    phone = data["phone"]

    prices = {
        "5 футів": 1850,
        "7.5 футів": 2350,
        "15 футів": 3800,
        "30 футів": 6650
    }
    price = prices[size] * months
    discount = 0
    if months >= 9:
        discount = 0.05
    elif months >= 6:
        discount = 0.03
    elif months >= 3:
        discount = 0.02

    total = int(price * (1 - discount))

    text = f"\u2705 Нова заявка:\n\n"
    text += f"\U0001F464 Ім'я: {name}\n"
    text += f"\U0001F4DE Телефон: {phone}\n"
    text += f"\U0001F4E6 Контейнер: {size}\n"
    text += f"\U0001F4C5 Місяців: {months}\n"
    text += f"\U0001F4B0 Сума зі знижкою: {total} грн"

    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
    await message.answer("\u2705 Дякуємо! Заявка надіслана. Ми зв'яжемось з вами найближчим часом.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
