import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "7680848123:AAGeVHb8glcUbbb-9IEcdGAauNcG2p2Oeag"
ADMIN_CHAT_ID = '5498505652'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📦 Орендувати контейнер")
    keyboard.add("📍 Перегляд локацій")
    keyboard.add("📞 Зв'язатися з нами")
    await message.answer("👍 Вітаємо у MyBox!\nОберіть опцію нижче:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "📍 Перегляд локацій")
async def view_locations(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    locations = [
        ("📍 вул. Лугова 9", "https://maps.google.com/?q=50.425689,30.483118"),
        ("📍 вул. Плодова 1", "https://maps.google.com/?q=50.400233,30.457452")
    ]
    for loc, link in locations:
        keyboard.add(types.InlineKeyboardButton(text=loc, url=link))
    await message.answer("Оберіть локацію для перегляду на карті:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "📦 Орендувати контейнер")
async def rent(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("5 футів - 1850 грн")
    keyboard.add("7.5 футів - 2350 грн")
    keyboard.add("15 футів - 3800 грн")
    keyboard.add("30 футів - 6650 грн")
    await message.answer("Оберіть розмір контейнера з ціною:", reply_markup=keyboard)

@dp.message_handler(lambda message: "футів" in message.text)
async def select_location(message: types.Message):
    user_data[message.from_user.id] = {"size": message.text.split(" - ")[0]}
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("📍 вул. Лугова 9")
    keyboard.add("📍 вул. Плодова 1")
    await message.answer("Оберіть локацію:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text in ["📍 вул. Лугова 9", "📍 вул. Плодова 1"])
async def select_months(message: types.Message):
    user_data[message.from_user.id]["location"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*[f"{i} місяців" if i > 1 else "1 місяць" for i in range(1, 13)])
    await message.answer("Оберіть термін оренди (1–12 місяців):", reply_markup=keyboard)

@dp.message_handler(lambda message: "місяц" in message.text)
async def ask_name(message: types.Message):
    user_data[message.from_user.id]["months"] = int(message.text.split()[0])
    await message.answer("Введіть ваше ім'я:")

@dp.message_handler(lambda message: message.text.isalpha())
async def ask_phone(message: types.Message):
    user_data[message.from_user.id]["name"] = message.text
    await message.answer("Поділіться номером або введіть вручну:")

@dp.message_handler(lambda message: message.text.startswith("+") or message.text.isdigit())
async def finish(message: types.Message):
    uid = message.from_user.id
    user_data[uid]["phone"] = message.text
    data = user_data[uid]
    prices = {"5 футів": 1850, "7.5 футів": 2350, "15 футів": 3800, "30 футів": 6650}
    price = prices.get(data["size"], 0) * data["months"]
    text = f"✅ Нова заявка:\n👤 Ім'я: {data['name']}\n📞 Телефон: {data['phone']}\n📦 Контейнер: {data['size']}\n📍 Локація: {data['location']}\n🗓️ Місяців: {data['months']}\n💰 Сума: {price} грн"
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📦 Орендувати контейнер")
    keyboard.add("📍 Перегляд локацій")
    keyboard.add("📞 Зв'язатися з нами")
    await message.answer("✅ Дякуємо! Ваша заявка відправлена.", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "📞 Зв'язатися з нами")
async def contact_info(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("📞 Подзвонити", url="tel:+380442299090"),
        types.InlineKeyboardButton("🌐 Відвідати сайт", url="https://mybox.kiev.ua")
    )
    await message.answer("Контактна інформація:\n📍 м. Київ, вул. Лугова, 9\n📞 +38 (044) 229-90-90\n📧 info@mybox.kiev.ua", reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
