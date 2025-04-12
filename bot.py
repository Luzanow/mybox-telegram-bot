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
    # Додаємо три кнопки на повернення
    main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    main_keyboard.add("📦 Орендувати контейнер", "📞 Зв'язатися з нами")
    await message.answer("Повернутись до головного меню ⬇️", reply_markup=main_keyboard)

# Оренда контейнера
@dp.message_handler(lambda msg: msg.text == "📦 Орендувати контейнер")
async def rent_container(message: types.Message):
    user_data[message.from_user.id] = {"location": None}  # Зберігаємо пусту локацію
    # Вибір локації
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    keyboard.add(
        "📍 вул. Лугова 9",
        "📍 вул. Плодова 1",
        "📍 вул. Дегтярівська 21",
        "📍 вул. Сім'ї Сосніних 3",
        "📍 пр-т Лобановського 119"
        "📍 вул. Сортувальна 5"
        "📍 вул. Пухівська 4А"
        "📍 вул. Новокостянтинівська 18"
        "📍 вул. Бальзака 85А"
        "📍 вул. Будіндустрії 5"
        "📍 вул. Бориспільська 9"
        "📍 вул. Віскозна 1"
        "📍 вул. Промислова 4"
    )
    await message.answer("Оберіть локацію:", reply_markup=keyboard)

# Локація вибрана
@dp.message_handler(lambda msg: msg.text.startswith("📍"))
async def location_chosen(message: types.Message):
    user_data[message.from_user.id]["location"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    keyboard.add(
        "5 футів - 1850 грн",
        "7.5 футів - 2350 грн",
        "15 футів - 3800 грн",
        "30 футів - 6650 грн"
    )
    await message.answer("Оберіть розмір контейнера:", reply_markup=keyboard)

# Вибір розміру контейнера
@dp.message_handler(lambda msg: "футів" in msg.text and "грн" in msg.text)
async def choose_months(message: types.Message):
    size = message.text.split(" - ")[0]
    user_data[message.from_user.id]["size"] = size
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=4)
    keyboard.add(*[str(i) for i in range(1, 13)])
    await message.answer("Оберіть термін оренди (в місяцях):", reply_markup=keyboard)

# Введення терміну оренди
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
@dp.message_handler(lambda msg: "+" in msg.text or msg.text.isdigit())
async def handle_manual_phone(message: types.Message):
    user_data[message.from_user.id]["phone"] = message.text
    await send_summary(message)

# Підсумок заявки
async def send_summary(message: types.Message):
    uid = message.from_user.id
    data = user_data[uid]
    size = data["size"]
    months = data["months"]
    name = data["name"]
    phone = data["phone"]
    location = data["location"]  # Локація користувача
    base_price = data["base_price"]
    total = int(base_price * months)  # Вираховуємо без знижки, якщо потрібно - додамо знижку
    text = (
        "✅ Нова заявка:\n"
        f"👤 Ім'я: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"📦 Контейнер: {size}\n"
        f"📅 Місяців: {months}\n"
        f"📍 Локація: {location}\n"
        f"💰 Сума: {total} грн"
    )
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
    await message.answer("✅ Заявку відправлено! Очікуйте дзвінка оператора.", reply_markup=main_keyboard)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
