import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "7680848123:AAHmbEGQ49ZB8SXTGof4l3mbZ9vcIbuV_6k"
ADMIN_CHAT_ID = 'YOUR_TELEGRAM_ID'  # Заміни на свій Telegram ID

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Старт
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📦 Орендувати контейнер", "📍 Локації", "📞 Зв'язатися з нами")
    await message.answer("🖐 Вітаємо у MyBox!")
    
await message.answer("Обeрiть опцiю нижче:")


# Локації
@dp.message_handler(lambda message: message.text == "📍 Локації")
async def send_locations(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("📍 Лугова 9", url="https://goo.gl/maps/lu9"))
    keyboard.add(types.InlineKeyboardButton("📍 Плодова 1", url="https://goo.gl/maps/pl1"))
    keyboard.add(types.InlineKeyboardButton("📍 Дегтярівська 21", url="https://goo.gl/maps/dg21"))
    await message.answer("Оберіть локацію:", reply_markup=keyboard)

# Зв'язок
@dp.message_handler(lambda message: message.text == "📞 Зв'язатися з нами")
async def contact(message: types.Message):
    await message.answer("📲 Телефон: +38 095 93 87 317
📧 Email: myboxua55@gmail.com")

# Оренда
user_data = {}

@dp.message_handler(lambda message: message.text == "📦 Орендувати контейнер")
async def rent(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("5 футів", "7.5 футів", "15 футів", "30 футів")
    await message.answer("Оберіть розмір контейнера:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in ["5 футів", "7.5 футів", "15 футів", "30 футів"])
async def ask_months(message: types.Message):
    user_data[message.from_user.id] = {"size": message.text}
    await message.answer("Введіть термін оренди (в місяцях):")

@dp.message_handler(lambda message: message.text.isdigit())
async def ask_name(message: types.Message):
    user_data[message.from_user.id]["months"] = int(message.text)
    await message.answer("Введіть ваше ім'я:")

@dp.message_handler(lambda message: message.text.isalpha())
async def ask_phone(message: types.Message):
    user_data[message.from_user.id]["name"] = message.text
    await message.answer("Введіть ваш номер телефону:")

@dp.message_handler(lambda message: "+" in message.text or message.text.isdigit())
async def finish(message: types.Message):
    uid = message.from_user.id
    user_data[uid]["phone"] = message.text
    size = user_data[uid]["size"]
    months = user_data[uid]["months"]
    name = user_data[uid]["name"]
    phone = user_data[uid]["phone"]

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

    text = f"✅ Нова заявка:
👤 Ім'я: {name}
📞 Телефон: {phone}
📦 Контейнер: {size}
📅 Місяців: {months}
💰 Сума зі знижкою: {total} грн"

    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
    await message.answer("✅ Дякуємо! Заявку надіслано. Ми зв'яжемось з вами найближчим часом.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
