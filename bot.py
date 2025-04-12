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
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📦 Орендувати контейнер", "📍 Локації", "📞 Зв'язатися з нами")
    await message.answer("🖐 Вітаємо у MyBox!")
    await message.answer("Оберіть опцію нижче:", reply_markup=keyboard)

# Локації
@dp.message_handler(lambda msg: msg.text == "📍 Локації")
async def send_locations(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    locations = [
        ("📍 вул. Лугова 9", "https://www.google.com/maps?q=50.489004,30.459238"),
        ("📍 вул. Плодова 1", "https://www.google.com/maps?q=50.472710,30.638128"),
        ("📍 вул. Дегтярівська 21", "https://www.google.com/maps?q=50.454166,30.460875"),
        ("📍 вул. Сім'ї Сосніних 3", "https://www.google.com/maps?q=50.430764,30.399173"),
        ("📍 пр-т Валерія Лобановського 119", "https://www.google.com/maps?q=50.406703,30.501627"),
        ("📍 вул. Сортувальна 5", "https://www.google.com/maps?q=50.448929,30.724776"),
        ("📍 вул. Пухівська 4А", "https://www.google.com/maps?q=50.511623,30.665562"),
        ("📍 вул. Новокостянтинівська 18", "https://www.google.com/maps?q=50.482849,30.500137"),
        ("📍 вул. Оноре де Бальзака 85А", "https://www.google.com/maps?q=50.513399,30.614991"),
        ("📍 вул. Будіндустрії 5", "https://www.google.com/maps?q=50.438273,30.620470"),
        ("📍 вул. Бориспільська 9", "https://www.google.com/maps?q=50.411243,30.682428"),
        ("📍 вул. Віскозна 1", "https://www.google.com/maps?q=50.407437,30.643321"),
        ("📍 вул. Промислова 4", "https://www.google.com/maps?q=50.419772,30.681408"),
    ]
    for name, url in locations:
        keyboard.add(types.InlineKeyboardButton(name, url=url))
    await message.answer("Оберіть локацію:", reply_markup=keyboard)

# Зв'язок
@dp.message_handler(lambda msg: msg.text == "📞 Зв'язатися з нами")
async def contact(message: types.Message):
    await message.answer("📞 Телефон: +38 095 93 87 317\n📧 Email: myboxua55@gmail.com")

# Оренда
@dp.message_handler(lambda msg: msg.text == "📦 Орендувати контейнер")
async def rent_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("5 футів - 1850 грн", "7.5 футів - 2350 грн")
    keyboard.add("15 футів - 3800 грн", "30 футів - 6650 грн")
    await message.answer("Оберіть розмір контейнера:", reply_markup=keyboard)

@dp.message_handler(lambda msg: "футів" in msg.text)
async def rent_duration(message: types.Message):
    user_data[message.from_user.id] = {"size": message.text}
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*[str(i) for i in range(1, 13)])
    await message.answer("Оберіть термін оренди (в місяцях):", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text.isdigit())
async def ask_name(message: types.Message):
    user_data[message.from_user.id]["months"] = int(message.text)
    await message.answer("Введіть ваше ім'я:")

@dp.message_handler(lambda msg: msg.text.isalpha())
async def ask_phone(message: types.Message):
    user_data[message.from_user.id]["name"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    request_contact = types.KeyboardButton("📱 Поділитись номером", request_contact=True)
    keyboard.add(request_contact)
    await message.answer("Поділіться номером або введіть вручну:", reply_markup=keyboard)

@dp.message_handler(content_types=["contact", "text"])
async def send_summary(message: types.Message):
    uid = message.from_user.id
    phone = message.contact.phone_number if message.contact else message.text
    user_data[uid]["phone"] = phone

    size = user_data[uid]["size"]
    months = user_data[uid]["months"]
    name = user_data[uid]["name"]

    prices = {
        "5 футів - 1850 грн": 1850,
        "7.5 футів - 2350 грн": 2350,
        "15 футів - 3800 грн": 3800,
        "30 футів - 6650 грн": 6650
    }
    base_price = prices[size] * months
    discount = 0.05 if months >= 9 else 0.03 if months >= 6 else 0.02 if months >= 3 else 0
    total = int(base_price * (1 - discount))

    text = f"✅ Нова заявка:\n👤 Ім'я: {name}\n📞 Телефон: {phone}\n📦 Контейнер: {size}\n📅 Місяців: {months}\n💰 Сума зі знижкою: {total} грн"

    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
    await message.answer("✅ Заявка надіслана! Очікуйте відповіді 👷")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
