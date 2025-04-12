import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import KeyboardButton

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
        ("📍 вул. Лугова 9", "https://maps.app.goo.gl/RXYw27unXxyQUt3e8"),
        ("📍 вул. Плодова 1", "https://maps.app.goo.gl/62kct7CeJwTX9MgJ6"),
        ("📍 вул. Дегтярівська 21", "https://maps.app.goo.gl/J4JQ7ZDbZK1UQjRg9"),
        ("📍 вул. Сім'ї Сосніних 3", "https://maps.app.goo.gl/QSnCBrsEGyDoYNnV6"),
        ("📍 пр-т Валерія Лобановського 119", "https://maps.app.goo.gl/nZCmFREu4VmXKRAo6"),
        ("📍 вул. Сортувальна 5", "https://maps.app.goo.gl/fdDfY71j1AW7iNPm7"),
        ("📍 вул. Пухівська 4А", "https://maps.app.goo.gl/TzDzo39NS58sbRk29"),
        ("📍 вул. Новокостянтинівська 18", "https://maps.app.goo.gl/fgJuJSCixUWo6PYJ6"),
        ("📍 вул. Оноре де Бальзака 85А", "https://maps.app.goo.gl/DHyoqLECRasV2qBP9"),
        ("📍 вул. Будіндустрії 5", "https://maps.app.goo.gl/qy9gz6czFPfZNGVA8"),
        ("📍 вул. Бориспільська 9", "https://maps.app.goo.gl/kx6ZBAzhqMkD9Rwv6"),
        ("📍 вул. Віскозна 1", "https://maps.app.goo.gl/ULPRNKU5cJZYHk5b9"),
        ("📍 вул. Промислова 4", "https://maps.app.goo.gl/HWYxwXktnsCwvxmh9"),
    }
    for name, url in locations.items():
        keyboard.add(types.InlineKeyboardButton(name, url=url))
    await message.answer("Оберіть локацію:", reply_markup=keyboard)

# Контакт
@dp.message_handler(lambda msg: msg.text == "📞 Зв'язатися з нами")
async def contact(message: types.Message):
    await message.answer("📞 Телефон: +38 095 93 87 317\n📧 Email: myboxua55@gmail.com")

# Оренда
@dp.message_handler(lambda msg: msg.text == "📦 Орендувати контейнер")
async def rent_start(message: types.Message):
    sizes = ["5 футів", "7.5 футів", "15 футів", "30 футів"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for size in sizes:
        keyboard.add(size)
    await message.answer("Оберіть розмір контейнера:", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text in ["5 футів", "7.5 футів", "15 футів", "30 футів"])
async def choose_months(message: types.Message):
    user_data[message.from_user.id] = {"size": message.text}
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=4)
    buttons = [str(i) for i in range(1, 13)]
    keyboard.add(*buttons)
    await message.answer("Оберіть термін оренди (в місяцях):", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text.isdigit() and 1 <= int(msg.text) <= 12)
async def ask_name(message: types.Message):
    user_data[message.from_user.id]["months"] = int(message.text)
    await message.answer("Введіть ваше ім’я:")

@dp.message_handler(lambda msg: msg.text.isalpha())
async def ask_phone(message: types.Message):
    user_data[message.from_user.id]["name"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    contact_btn = KeyboardButton("📱 Поділитись номером", request_contact=True)
    keyboard.add(contact_btn).add("✏️ Ввести вручну")
    await message.answer("Поділіться номером або введіть вручну:", reply_markup=keyboard)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_contact(message: types.Message):
    user_data[message.from_user.id]["phone"] = message.contact.phone_number
    await finish_order(message)

@dp.message_handler(lambda msg: msg.text.startswith("+") or msg.text.replace(" ", "").isdigit())
async def get_phone_manual(message: types.Message):
    user_data[message.from_user.id]["phone"] = message.text
    await finish_order(message)

async def finish_order(message: types.Message):
    uid = message.from_user.id
    data = user_data.get(uid, {})
    size = data.get("size")
    months = data.get("months")
    name = data.get("name")
    phone = data.get("phone")

    prices = {
        "5 футів": 1850,
        "7.5 футів": 2350,
        "15 футів": 3800,
        "30 футів": 6650
    }
    base = prices[size] * months
    discount = 0
    if months >= 9:
        discount = 0.05
    elif months >= 6:
        discount = 0.03
    elif months >= 3:
        discount = 0.02
    total = int(base * (1 - discount))

    text = f"✅ Нова заявка:\n👤 Ім’я: {name}\n📞 Телефон: {phone}\n📦 Контейнер: {size}\n📅 Місяців: {months}\n💰 Сума зі знижкою: {total} грн"
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
    await message.answer("✅ Дякуємо! Заявка надіслана. Очікуйте дзвінка!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
