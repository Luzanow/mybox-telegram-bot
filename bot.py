import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "7680848123:AAHqNizmx3hOXmjVOmzdnwQCenlXHTWX8OA"
ADMIN_CHAT_ID = 5498505652

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}

# Старт
main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
main_keyboard.add(
    "📦 Орендувати контейнер",
    "📍 Локації",
    "📞 Зв'язатися з нами"
)

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.answer("🖐 Вітаємо у MyBox!", reply_markup=main_keyboard)
    await message.answer("Оберіть опцію нижче:")

# Локації
@dp.message_handler(lambda msg: msg.text == "📍 Локації")
async def send_locations(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    locations = [
        ("📍 вул. Лугова 9", "https://www.google.com/maps?q=вул.+Лугова+9,+Київ"),
        ("📍 вул. Плодова 1", "https://www.google.com/maps?q=вул.+Плодова+1,+Київ"),
        ("📍 вул. Дегтярівська 21", "https://www.google.com/maps?q=вул.+Дегтярівська+21,+Київ")
    ]
    for name, url in locations:
        keyboard.add(types.InlineKeyboardButton(text=name, url=url))
    await message.answer("Оберіть локацію:", reply_markup=keyboard)
    await message.answer("Повертаємо головне меню ⬇️", reply_markup=main_keyboard)

# Контакт
@dp.message_handler(lambda msg: msg.text == "📞 Зв'язатися з нами")
async def contact_info(message: types.Message):
    await message.answer("📞 Телефон: +38 095 93 87 317\n📧 Email: myboxua55@gmail.com", reply_markup=main_keyboard)

# Оренда
@dp.message_handler(lambda msg: msg.text == "📦 Орендувати контейнер")
async def rent_container(message: types.Message):
    user_data[message.from_user.id] = {}
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    keyboard.add(
        "5 футів - 1850 грн",
        "7.5 футів - 2350 грн",
        "15 футів - 3800 грн",
        "30 футів - 6650 грн"
    )
    await message.answer("Оберіть розмір контейнера:", reply_markup=keyboard)

@dp.message_handler(lambda msg: "футів" in msg.text and "грн" in msg.text)
async def choose_months(message: types.Message):
    size, price = message.text.split(" - ")
    user_data[message.from_user.id]["size"] = size.strip()
    user_data[message.from_user.id]["base_price"] = int(price.replace("грн", "").strip())
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=4)
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
    button = types.KeyboardButton("📱 Поділитися номером телефону", request_contact=True)
    keyboard.add(button)
    await message.answer("Поділіться номером або введіть вручну:", reply_markup=keyboard)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def handle_contact(message: types.Message):
    user_data[message.from_user.id]["phone"] = message.contact.phone_number
    await send_summary(message)

@dp.message_handler(lambda msg: msg.text and ("+" in msg.text or msg.text.replace(" ", "").isdigit()))
async def handle_manual_phone(message: types.Message):
    user_data[message.from_user.id]["phone"] = message.text
    await send_summary(message)

async def send_summary(message):
    uid = message.from_user.id
    data = user_data[uid]
    size = data["size"]
    months = data["months"]
    name = data["name"]
    phone = data["phone"]
    base_price = data["base_price"]
    discount = 0.05 if months >= 9 else 0.03 if months >= 6 else 0.02 if months >= 3 else 0.0
    total = int(base_price * months * (1 - discount))
    text = (
        "✅ Нова заявка:\n"
        f"👤 Ім'я: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"📦 Контейнер: {size}\n"
        f"📅 Місяців: {months}\n"
        f"💸 Знижка: {int(discount * 100)}%\n"
        f"💰 Сума зі знижкою: {total} грн"
    )
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
    await message.answer("✅ Заявку відправлено! Очікуйте дзвінка.", reply_markup=main_keyboard)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
