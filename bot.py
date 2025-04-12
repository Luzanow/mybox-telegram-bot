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
    keyboard.add("📦 Орендувати контейнер")
    keyboard.add("📍 Локації")
    keyboard.add("📞 Зв'язатися з нами")
    await message.answer("🖐 Вітаємо у MyBox!", reply_markup=keyboard)
    await message.answer("Оберіть опцію нижче:")

# Локації
@dp.message_handler(lambda msg: msg.text == "📍 Локації")
async def send_locations(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    locations = [
        ("📍 вул. Лугова 9", "https://goo.gl/maps/RXYw27unXxyQUt3e8"),
        ("📍 вул. Плодова 1", "https://goo.gl/maps/62kct7CeJwTX9MgJ6"),
        ("📍 вул. Дегтярівська 21", "https://goo.gl/maps/J4JQ7ZDbZK1UQjRg9"),
        ("📍 вул. Сім'ї Сосніних 3", "https://goo.gl/maps/QSnCBrsEGyDoYNnV6"),
        ("📍 пр-т Лобановського 119", "https://goo.gl/maps/nZCmFREu4VmXKRAo6"),
        ("📍 вул. Сортувальна 5", "https://goo.gl/maps/fdDfY71j1AW7iNPm7"),
        ("📍 вул. Пухівська 4А", "https://goo.gl/maps/TzDzo39NS58sbRk29"),
        ("📍 вул. Новокостянтинівська 18", "https://goo.gl/maps/fgJuJSCixUWo6PYJ6"),
        ("📍 вул. Оноре де Бальзака 85А", "https://goo.gl/maps/DHyoqLECRasV2qBP9"),
        ("📍 вул. Будіндустрії 5", "https://goo.gl/maps/qy9gz6czFPfZNGVA8"),
        ("📍 вул. Бориспільська 9", "https://goo.gl/maps/kx6ZBAzhqMkD9Rwv6"),
        ("📍 вул. Віскозна 1", "https://goo.gl/maps/ULPRNKU5cJZYHk5b9"),
        ("📍 вул. Промислова 4", "https://goo.gl/maps/HWYxwXktnsCwvxmh9"),
    ]
    for name, url in locations:
        keyboard.add(types.InlineKeyboardButton(text=name, url=url))
    await message.answer("Оберіть локацію:", reply_markup=keyboard)

# Зв'язок
@dp.message_handler(lambda msg: msg.text == "📞 Зв'язатися з нами")
async def contact(message: types.Message):
    await message.answer("📞 Телефон: +38 095 93 87 317\n📧 Email: myboxua55@gmail.com")

# Оренда
@dp.message_handler(lambda msg: msg.text == "📦 Орендувати контейнер")
async def rent_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("5 футів", "7.5 футів", "15 футів", "30 футів")
    await message.answer("Оберіть розмір контейнера:", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text in ["5 футів", "7.5 футів", "15 футів", "30 футів"])
async def ask_months(message: types.Message):
    user_data[message.from_user.id] = {"size": message.text}
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*[str(i) for i in range(1, 13)])
    await message.answer("Оберіть термін оренди (в місяцях):", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text.isdigit() and 1 <= int(msg.text) <= 12)
async def ask_name(message: types.Message):
    user_data[message.from_user.id]["months"] = int(message.text)
    await message.answer("Введіть ваше ім'я:")

@dp.message_handler(lambda msg: msg.text.isalpha())
async def ask_phone(message: types.Message):
    user_data[message.from_user.id]["name"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = types.KeyboardButton("Поділитися номером", request_contact=True)
    keyboard.add(button)
    await message.answer("Поділіться номером або введіть вручну:", reply_markup=keyboard)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def handle_contact(message: types.Message):
    user_data[message.from_user.id]["phone"] = message.contact.phone_number
    await send_order(message)

@dp.message_handler(lambda msg: msg.text.startswith("+380") or msg.text.replace(" ", "").isdigit())
async def handle_manual_phone(message: types.Message):
    user_data[message.from_user.id]["phone"] = message.text
    await send_order(message)

async def send_order(message: types.Message):
    uid = message.from_user.id
    if "months" not in user_data[uid]:
        await message.answer("Помилка: термін оренди не вказано. Спробуйте знову.")
        return

    data = user_data[uid]
    prices = {
        "5 футів": 1850,
        "7.5 футів": 2350,
        "15 футів": 3800,
        "30 футів": 6650,
    }
    price = prices[data["size"]] * data["months"]
    discount = 0
    if data["months"] >= 9:
        discount = 0.05
    elif data["months"] >= 6:
        discount = 0.03
    elif data["months"] >= 3:
        discount = 0.02

    total = int(price * (1 - discount))
    text = f"✅ Нова заявка:\n👤 Ім'я: {data['name']}\n📞 Телефон: {data['phone']}\n📦 Контейнер: {data['size']}\n📅 Місяців: {data['months']}\n💰 Сума зі знижкою: {total} грн"
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
    await message.answer("✅ Заявка надіслана! Очікуйте дзвінка від нашого менеджера.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
