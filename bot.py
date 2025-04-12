import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "7680848123:AAHmbEGQ49ZB8SXTGof4l3mbZ9vcIbuV_6k"
ADMIN_CHAT_ID = 5498505652  # Ваш Telegram ID (не @username)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}

# /start
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True, row_width=2
    )
    keyboard.add(
        "📦 Орендувати контейнер",
        "📍 Локації",
        "📞 Зв'язатися з нами"
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

# Зв'язатися з нами
@dp.message_handler(lambda msg: msg.text == "📞 Зв'язатися з нами")
async def contact_info(message: types.Message):
    await message.answer("📞 Телефон: +38 095 93 87 317\n📧 Email: myboxua55@gmail.com")

# Оренда контейнера
@dp.message_handler(lambda msg: msg.text == "📦 Орендувати контейнер")
async def rent_container(message: types.Message):
    # Зберігаємо пустий словник під цього користувача
    user_data[message.from_user.id] = {}
    # Кнопки з розміром і ціною: "<розмір> - <ціна> грн"
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True, row_width=2
    )
    keyboard.add(
        "5 футів - 1850 грн",
        "7.5 футів - 2350 грн",
        "15 футів - 3800 грн",
        "30 футів - 6650 грн"
    )
    await message.answer("Оберіть розмір контейнера:", reply_markup=keyboard)

# Користувач обрав розмір контейнера
@dp.message_handler(lambda msg: "футів" in msg.text and "грн" in msg.text)
async def choose_months(message: types.Message):
    # Наприклад, "5 футів - 1850 грн" -> size="5 футів", price=1850
    size_part, price_part = message.text.split("-")
    size_part = size_part.strip()  # "5 футів"
    price_value = int(price_part.replace("грн", "").strip())  # 1850

    user_data[message.from_user.id]["size"] = size_part
    user_data[message.from_user.id]["base_price"] = price_value

    # Пропонуємо термін оренди (1..12) кнопками
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True, row_width=4
    )
    keyboard.add(*(str(i) for i in range(1, 13)))
    await message.answer("Оберіть термін оренди (в місяцях):", reply_markup=keyboard)

# Користувач обрав кількість місяців (1..12)
@dp.message_handler(lambda msg: msg.text.isdigit() and 1 <= int(msg.text) <= 12)
async def ask_name(message: types.Message):
    user_data[message.from_user.id]["months"] = int(message.text)
    await message.answer("Введіть ваше ім'я:")

# Користувач вводить ім'я (строка)
@dp.message_handler(lambda msg: msg.text.isalpha())
async def ask_phone(message: types.Message):
    user_data[message.from_user.id]["name"] = message.text

    # Пропонуємо поділитись або ввести номер вручну
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    )
    share_btn = types.KeyboardButton(
        "📱 Поділитися номером телефону", request_contact=True
    )
    keyboard.add(share_btn)
    await message.answer("Поділіться номером або введіть вручну:", reply_markup=keyboard)

# Якщо користувач поділився номером
@dp.message_handler(content_types=types.ContentType.CONTACT)
async def handle_contact(message: types.Message):
    user_data[message.from_user.id]["phone"] = message.contact.phone_number
    await finish_order(message)

# Якщо користувач вводить номер вручну (+380..)
@dp.message_handler(lambda msg: msg.text and ("+" in msg.text or msg.text.replace(" ", "").isdigit()))
async def handle_manual_phone(message: types.Message):
    user_data[message.from_user.id]["phone"] = message.text
    await finish_order(message)

# Завершення заявки
async def finish_order(message: types.Message):
    uid = message.from_user.id
    data = user_data[uid]

    size = data["size"]           # "5 футів"
    base_price = data["base_price"]  # 1850 (int)
    months = data["months"]       # 1..12 (int)
    name = data["name"]
    phone = data["phone"]

    # Обчислення знижки
    discount = 0.0
    if months >= 9:
        discount = 0.05
    elif months >= 6:
        discount = 0.03
    elif months >= 3:
        discount = 0.02

    total = int(base_price * months * (1 - discount))

    text = (
        "✅ Нова заявка:\n"
        f"👤 Ім'я: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"📦 Контейнер: {size}\n"
        f"📅 Місяців: {months}\n"
        f"💰 Сума зі знижкою: {total} грн"
    )

    # Надсилаємо адміну
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
    # Надсилаємо користувачу підтвердження
    await message.answer("✅ Заявку відправлено! Очікуйте дзвінка оператора.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
