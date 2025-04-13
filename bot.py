import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "7680848123:AAHqNizmx3hOXmjVOmzdnwQCenlXHTWX8OA"
ADMIN_CHAT_ID = '5498505652'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📦 Орендувати контейнер", "📍 Перегляд локацій", "📞 Зв'язатися з нами")
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
    keyboard.add("5 футів - 1850 грн", "7.5 футів - 2350 грн", "15 футів - 3800 грн", "30 футів - 6650 грн")
    await message.answer("Оберіть розмір контейнера з ціною:", reply_markup=keyboard)

@dp.message_handler(lambda message: "футів" in message.text)
async def select_location(message: types.Message):
    user_data[message.from_user.id] = {"size": message.text.split(" - ")[0]}
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("\ud83d\udccd вул. Лугова 9", "\ud83d\udccd вул. Плодова 1")
    await message.answer("Оберіть локацію:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text.startswith("📍"))
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
    keyboard.add("\ud83d\udce6 \u041e\u0440\u0435\u043d\u0434\u0443\u0432\u0430\u0442\u0438 \u043a\u043e\u043d\u0442\u0435\u0439\u043d\u0435\u0440", "\ud83d\udccd \u041f\u0435\u0440\u0435\u0433\u043b\u044f\u0434 \u043b\u043e\u043a\u0430\u0446\u0456\u0439", "\ud83d\udcde \u0417\u0432'\u044f\u0437\u0430\u0442\u0438\u0441\u044f \u0437 \u043d\u0430\u043c\u0438")
    await message.answer("\u2705 \u0414\u044f\u043a\u0443\u0454\u043c\u043e! \u0412\u0430\u0448\u0430 \u0437\u0430\u044f\u0432\u043a\u0430 \u0432\u0456\u0434\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0430.", reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
