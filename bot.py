 import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "7680848123:AAHmbEGQ49ZB8SXTGof4l13mBz9vcIbuV_6k"
ADMIN_CHAT_ID = "@Luzanow"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📦 Орендувати контейнер", "📍 Локації", "📞 Зв'язатися з нами")
    await message.answer("🖐 Вітаємо у MyBox!", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text == "📍 Локації")
async def send_locations(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    locations = [
        ("📍 вул. Лугова 9", "https://www.google.com/maps?q=вул.+Лугова+9,+Київ"),
        ("📍 вул. Плодова 1", "https://www.google.com/maps?q=вул.+Плодова+1,+Київ"),
        ("📍 вул. Дегтярівська 21", "https://www.google.com/maps?q=вул.+Дегтярівська+21,+Київ"),
        ("📍 вул. Сім'ї Сосніних 3", "https://www.google.com/maps?q=вул.+Сім'ї+Сосніних+3,+Київ"),
        ("📍 пр-т Лобановського 119", "https://www.google.com/maps?q=проспект+Лобановського+119,+Київ"),
        ("📍 вул. Сортувальна 5", "https://www.google.com/maps?q=вул.+Сортувальна+5,+Київ"),
        ("📍 вул. Пухівська 4А", "https://www.google.com/maps?q=вул.+Пухівська+4А,+Київ"),
        ("📍 вул. Новокостянтинівська 18", "https://www.google.com/maps?q=вул.+Новокостянтинівська+18,+Київ"),
        ("📍 вул. Оноре де Бальзака 85А", "https://www.google.com/maps?q=вул.+Оноре+де+Бальзака+85А,+Київ"),
        ("📍 вул. Будіндустрії 5", "https://www.google.com/maps?q=вул.+Будіндустрії+5,+Київ"),
        ("📍 вул. Бориспільська 9", "https://www.google.com/maps?q=вул.+Бориспільська+9,+Київ"),
        ("📍 вул. Віскозна 1", "https://www.google.com/maps?q=вул.+Віскозна+1,+Київ"),
        ("📍 вул. Промислова 4", "https://www.google.com/maps?q=вул.+Промислова+4,+Київ"),
    ]
    for name, url in locations:
        keyboard.add(types.InlineKeyboardButton(name, url=url))
    await message.answer("Оберіть локацію:", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text == "📞 Зв'язатися з нами")
async def contact(message: types.Message):
    await message.answer("📞 Телефон: +38 095 93 87 317
📧 Email: myboxua55@gmail.com")

@dp.message_handler(lambda msg: msg.text == "📦 Орендувати контейнер")
async def rent_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("5 футів", "7.5 футів", "15 футів", "30 футів")
    await message.answer("Оберіть розмір контейнера:", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text in ["5 футів", "7.5 футів", "15 футів", "30 футів"])
async def ask_months(message: types.Message):
    user_data[message.from_user.id] = {"size": message.text}
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*(str(i) for i in range(1, 13)))
    await message.answer("Оберіть термін оренди (в місяцях):", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text.isdigit())
async def ask_name(message: types.Message):
    user_data[message.from_user.id]["months"] = int(message.text)
    await message.answer("Введіть ваше ім'я:")

@dp.message_handler(lambda msg: msg.text.isalpha())
async def ask_phone(message: types.Message):
    user_data[message.from_user.id]["name"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    contact_button = types.KeyboardButton("📱 Поділитись номером телефону", request_contact=True)
    keyboard.add(contact_button)
    await message.answer("Поділіться номером або введіть вручну:", reply_markup=keyboard)

@dp.message_handler(content_types=types.ContentType.CONTACT)
@dp.message_handler(lambda msg: "+" in msg.text or msg.text.isdigit())
async def finish(message: types.Message):
    uid = message.from_user.id
    phone = message.contact.phone_number if message.contact else message.text
    user_data[uid]["phone"] = phone
    size = user_data[uid]["size"]
    months = user_data[uid]["months"]
    name = user_data[uid]["name"]

    prices = {
        "5 футів": 1850,
        "7.5 футів": 2350,
        "15 футів": 3800,
        "30 футів": 6650
    }
    base_price = prices[size] * months
    discount = 0.05 if months >= 9 else 0.03 if months >= 6 else 0.02 if months >= 3 else 0
    total = int(base_price * (1 - discount))

    text = f"✅ Нова заявка:
👤 Ім'я: {name}
📞 Телефон: {phone}
📦 Контейнер: {size}
📅 Місяців: {months}
💰 Сума зі знижкою: {total} грн"
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
    await message.answer("✅ Заявку відправлено! Очікуйте дзвінок найближчим часом.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
