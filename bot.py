import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

API_TOKEN = "7680848123:AAHmbEGQ49ZB8SXTGq4I13mBz9ycIbuV_6k"
ADMIN_CHAT_ID = "@Luzanow"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}

# Старт
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add("📦 Орендувати контейнер")
    keyboard.add("📍 Локації")
    keyboard.add(KeyboardButton("📞 Зв'язатися з нами"))
    await message.answer(“📥 Вітаємо у MyBox!”)
    await message.answer("Оберіть опцію нижче:", reply_markup=keyboard)

# Локації
@dp.message_handler(lambda msg: msg.text == "📍 Локації")
async def send_locations(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    locations = [
        ("\ud83d\udccd вул. Лугова 9", "https://www.google.com/maps?q=вул.+Лугова+9"),
        ("\ud83d\udccd вул. Плодова 1", "https://www.google.com/maps?q=вул.+Плодова+1"),
        ("\ud83d\udccd вул. Дегтярівська 21", "https://www.google.com/maps?q=вул.+Дегтярівська+21"),
        ("\ud83d\udccd вул. Сім'ї Сосніних 3", "https://www.google.com/maps?q=вул.+Сім'ї+Сосніних+3"),
        ("\ud83d\udccd пр-т Лобановського 119", "https://www.google.com/maps?q=пр-т+Лобановського+119"),
        ("\ud83d\udccd вул. Сортувальна 5", "https://www.google.com/maps?q=вул.+Сортувальна+5"),
        ("\ud83d\udccd вул. Пухівська 4А", "https://www.google.com/maps?q=вул.+Пухівська+4А"),
        ("\ud83d\udccd вул. Новокостянтинівська 18", "https://www.google.com/maps?q=вул.+Новокостянтинівська+18"),
        ("\ud83d\udccd вул. Оноре де Бальзака 85А", "https://www.google.com/maps?q=вул.+Оноре+де+Бальзака+85А"),
        ("\ud83d\udccd вул. Будіндустрії 5", "https://www.google.com/maps?q=вул.+Будіндустрії+5"),
        ("\ud83d\udccd вул. Бориспільська 9", "https://www.google.com/maps?q=вул.+Бориспільська+9"),
        ("\ud83d\udccd вул. Віскозна 1", "https://www.google.com/maps?q=вул.+Віскозна+1"),
        ("\ud83d\udccd вул. Промислова 4", "https://www.google.com/maps?q=вул.+Промислова+4")
    ]
    for name, url in locations:
        keyboard.add(InlineKeyboardButton(text=name, url=url))
    await message.answer("Оберіть локацію:", reply_markup=keyboard)

# Зв'язок
@dp.message_handler(lambda msg: msg.text == "📞 Зв'язатися з нами")
async def contact(message: types.Message):
    await message.answer("\ud83d\udcde Телефон: +38 095 93 87 317\n\ud83d\udce7 Email: myboxua55@gmail.com")

# Оренда
@dp.message_handler(lambda msg: msg.text == "📦 Орендувати контейнер")
async def rent_start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add("5 футів (1850 грн)", "7.5 футів (2350 грн)", "15 футів (3800 грн)", "30 футів (6650 грн)")
    await message.answer("Оберіть розмір контейнера:", reply_markup=keyboard)

@dp.message_handler(lambda msg: "футів" in msg.text)
async def ask_months(message: types.Message):
    size = message.text.split(" (")[0]
    user_data[message.from_user.id] = {"size": size}
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    keyboard.add(*[str(i) for i in range(1, 13)])
    await message.answer("Оберіть термін оренди (в місяцях):", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text.isdigit() and 0 < int(msg.text) <= 12)
async def ask_name(message: types.Message):
    user_data[message.from_user.id]["months"] = int(message.text)
    await message.answer("Введіть ваше ім'я:")

@dp.message_handler(lambda msg: msg.text.isalpha())
async def ask_phone(message: types.Message):
    user_data[message.from_user.id]["name"] = message.text
    button = KeyboardButton("Поділитися номером телефону", request_contact=True)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button)
    await message.answer("Поділіться номером або введіть вручну:", reply_markup=keyboard)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def handle_contact(message: types.Message):
    user_data[message.from_user.id]["phone"] = message.contact.phone_number
    await submit_request(message)

@dp.message_handler(lambda msg: msg.text.startswith("+") or msg.text.replace(" ", "").isdigit())
async def handle_phone_text(message: types.Message):
    user_data[message.from_user.id]["phone"] = message.text
    await submit_request(message)

async def submit_request(message: types.Message):
    uid = message.from_user.id
    data = user_data[uid]
    prices = {
        "5 футів": 1850,
        "7.5 футів": 2350,
        "15 футів": 3800,
        "30 футів": 6650
    }
    price = prices[data["size"]] * data["months"]
    discount = 0.05 if data["months"] >= 9 else 0.03 if data["months"] >= 6 else 0.02 if data["months"] >= 3 else 0
    total = int(price * (1 - discount))

    text = f"✅ Нова заявка:\n👤 Ім'я: {data['name']}\n📞 Телефон: {data['phone']}\n📦 Контейнер: {data['size']}\n📅 Місяців: {data['months']}\n💰 Сума зі знижкою: {total} грн"

    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
    await message.answer("✅ Ваша заявка відправлена. Очікуйте відповіді.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
