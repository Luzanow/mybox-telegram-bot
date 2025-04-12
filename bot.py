import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "7680848123:AAHmbEGQ49ZB8SXTGof4l3mbZ9vcIbuV_6k"
ADMIN_CHAT_ID = 5498505652  # Ваш Telegram ID

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}

# Стартова команда
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
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
        ("📍 вул. Лугова 9", "https://www.google.com/maps?q=вул.+Лугова+9,+Київ"),
        ("📍 вул. Плодова 1", "https://www.google.com/maps?q=вул.+Плодова+1,+Київ"),
        ("📍 вул. Дегтярівська 21", "https://www.google.com/maps?q=вул.+Дегтярівська+21,+Київ"),
        ("📍 вул. Сім'ї Сосніних 3", "https://www.google.com/maps?q=вул.+Сім'ї+Сосніних+3,+Київ"),
        ("📍 пр-т Лобановського 119", "https://www.google.com/maps?q=просп.+Лобановського+119,+Київ"),
        ("📍 вул. Сортувальна 5", "https://www.google.com/maps?q=вул.+Сортувальна+5,+Київ"),
        ("📍 вул. Пухівська 4А", "https://www.google.com/maps?q=вул.+Пухівська+4А,+Київ"),
        ("📍 вул. Новокостянтинівська 18", "https://www.google.com/maps?q=вул.+Новокостянтинівська+18,+Київ"),
        ("📍 вул. Бальзака 85А", "https://www.google.com/maps?q=вул.+Бальзака+85А,+Київ"),
        ("📍 вул. Будіндустрії 5", "https://www.google.com/maps?q=вул.+Будіндустрії+5,+Київ"),
        ("📍 вул. Бориспільська 9", "https://www.google.com/maps?q=вул.+Бориспільська+9,+Київ"),
        ("📍 вул. Віскозна 1", "https://www.google.com/maps?q=вул.+Віскозна+1,+Київ"),
        ("📍 вул. Промислова 4", "https://www.google.com/maps?q=вул.+Промислова+4,+Київ"),
    ]
    for name, url in locations:
        keyboard.add(types.InlineKeyboardButton(text=name, url=url))
    await message.answer("Оберіть локацію:", reply_markup=keyboard)

# Контактна інформація
@dp.message_handler(lambda msg: msg.text == "📞 Зв'язатися з нами")
async def contact(message: types.Message):
    await message.answer("📞 Телефон: +38 095 93 87 317\n📧 Email: myboxua55@gmail.com")

# Початок процесу оренди
@dp.message_handler(lambda msg: msg.text == "📦 Орендувати контейнер")
async def rent_start(message: types.Message):
    user_data[message.from_user.id] = {}
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    # Кнопки з розмірами контейнерів та цінами
    keyboard.add("5 футів - 1850 грн", "7.5 футів - 2350 грн",
                 "15 футів - 3800 грн", "30 футів - 6650 грн")
    await message.answer("Оберіть розмір контейнера:", reply_markup=keyboard)

# Вибір терміну оренди
@dp.message_handler(lambda msg: "футів" in msg.text)
async def ask_months(message: types.Message):
    size = message.text.split(" - ")[0]
    user_data[message.from_user.id]["size"] = size
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=4)
    keyboard.add(*[str(i) for i in range(1, 13)])
    await message.answer("Оберіть термін оренди (в місяцях):", reply_markup=keyboard)

# Введення імені
@dp.message_handler(lambda msg: msg.text.isdigit() and 1 <= int(msg.text) <= 12)
async def ask_name(message: types.Message):
    user_data[message.from_user.id]["months"] = int(message.text)
    await message.answer("Введіть ваше ім'я:")

# Введення імені завершено; тепер введення номера
@dp.message_handler(lambda msg: msg.text.isalpha())
async def ask_phone(message: types.Message):
    user_data[message.from_user.id]["name"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = types.KeyboardButton("📱 Поділитися номером телефону", request_contact=True)
    keyboard.add(button)
    await message.answer("Поділіться номером або введіть вручну:", reply_markup=keyboard)

# Отримання контакту (номер телефону)
@dp.message_handler(content_types=types.ContentType.CONTACT)
async def receive_contact(message: types.Message):
    user_data[message.from_user.id]["phone"] = message.contact.phone_number
    await send_summary(message)

# Введення номера вручну
@dp.message_handler(lambda msg: msg.text and ("+" in msg.text or msg.text.replace(" ", "").isdigit()))
async def receive_manual_phone(message: types.Message):
    user_data[message.from_user.id]["phone"] = message.text
    await send_summary(message)

# Підсумок заявки
async def send_summary(message: types.Message):
    uid = message.from_user.id
    data = user_data[uid]
    prices = {
        "5 футів": 1850,
        "7.5 футів": 2350,
        "15 футів": 3800,
        "30 футів": 6650
    }
    size = data["size"]
    months = data["months"]
    name = data["name"]
    phone = data["phone"]
    base_price = prices[size] * months
    discount = 0.05 if months >= 9 else 0.03 if months >= 6 else 0.02 if months >= 3 else 0
    total = int(base_price * (1 - discount))
    summary = (
        "✅ Нова заявка:\n"
        f"👤 Ім'я: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"📦 Контейнер: {size}\n"
        f"📅 Місяців: {months}\n"
        f"💰 Сума зі знижкою: {total} грн"
    )
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=summary)
    await message.answer("✅ Заявку відправлено! Очікуйте дзвінка оператора.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
