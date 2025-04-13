import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "7680848123:AAGeVHb8glcUbbb-9IEcdGAauNcG2p2Oeag"
ADMIN_CHAT_ID = '5498505652'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}

# Головне меню
def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📦 Орендувати контейнер", "📍 Перегляд локацій")
    keyboard.add("📞 Зв'язатися з нами")
    return keyboard

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("👍 Вітаємо у MyBox!\nОберіть опцію нижче:", reply_markup=main_menu())

# Кнопка "Перегляд локацій"
@dp.message_handler(lambda message: message.text == "📍 Перегляд локацій")
async def view_locations(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    locations = [
        ("📍 вул. Лугова 9", "https://maps.google.com/?q=50.425689,30.483118"),
        ("📍 вул. Плодова 1", "https://maps.google.com/?q=50.400233,30.457452"),
        ("📍 вул. Дегтярівська 21", "https://maps.google.com/?q=50.457832,30.480274"),
        ("📍 вул. Сім'ї Сосніних 3", "https://maps.google.com/?q=50.434291,30.464987"),
        ("📍 пр-т Лобановського 119", "https://maps.google.com/?q=50.426594,30.495850"),
        ("📍 вул. Сортувальна 5", "https://maps.google.com/?q=50.464835,30.490526"),
        ("📍 вул. Пухівська 4А", "https://maps.google.com/?q=50.422968,30.510332"),
        ("📍 вул. Новокостянтинівська 18", "https://maps.google.com/?q=50.438151,30.497368"),
        ("📍 вул. Бальзака 85А", "https://maps.google.com/?q=50.395106,30.455319"),
        ("📍 вул. Будіндустрії 5", "https://maps.google.com/?q=50.476872,30.464531"),
        ("📍 вул. Бориспільська 9", "https://maps.google.com/?q=50.446179,30.476200"),
        ("📍 вул. Віскозна 1", "https://maps.google.com/?q=50.453824,30.487111"),
        ("📍 вул. Промислова 4", "https://maps.google.com/?q=50.425598,30.508532")
    ]
    for loc, link in locations:
        keyboard.add(types.InlineKeyboardButton(text=loc, url=link))
    await message.answer("Оберіть локацію для перегляду на карті:", reply_markup=keyboard)

# Кнопка "Зв'язатися з нами"
@dp.message_handler(lambda message: message.text == "📞 Зв'язатися з нами")
async def contact_info(message: types.Message):
    await message.answer(
        "📞 Контактна особа: Тарас\n"
        "📱 Телефон: +380 (99) 093 64 37\n"
        "📧 Email: info@mybox.kiev.ua\n"
        "🌐 Сайт: https://mybox.kiev.ua",
        reply_markup=main_menu()
    )

# Початок оренди
@dp.message_handler(lambda message: message.text == "📦 Орендувати контейнер")
async def rent(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("5 футів - 1850 грн", "7.5 футів - 2350 грн")
    keyboard.add("15 футів - 3800 грн", "30 футів - 6650 грн")
    keyboard.add("🔙 На головну")
    await message.answer("Оберіть розмір контейнера з ціною:", reply_markup=keyboard)

@dp.message_handler(lambda message: "футів" in message.text)
async def select_location(message: types.Message):
    user_data[message.from_user.id] = {"size": message.text.split(" - ")[0]}
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(
        "📍 вул. Лугова 9", "📍 вул. Плодова 1", "📍 вул. Дегтярівська 21", "📍 вул. Сім'ї Сосніних 3",
        "📍 пр-т Лобановського 119", "📍 вул. Сортувальна 5", "📍 вул. Пухівська 4А",
        "📍 вул. Новокостянтинівська 18", "📍 вул. Бальзака 85А", "📍 вул. Будіндустрії 5",
        "📍 вул. Бориспільська 9", "📍 вул. Віскозна 1", "📍 вул. Промислова 4"
    )
    keyboard.add("🔙 На головну")
    await message.answer("Оберіть локацію:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text.startswith("📍"))
async def select_months(message: types.Message):
    user_data[message.from_user.id]["location"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*[f"{i} місяців" if i > 1 else "1 місяць" for i in range(1, 13)])
    keyboard.add("🔙 На головну")
    await message.answer("Оберіть термін оренди (1–12 місяців):", reply_markup=keyboard)

@dp.message_handler(lambda message: "місяц" in message.text)
async def ask_name(message: types.Message):
    user_data[message.from_user.id]["months"] = int(message.text.split()[0])
    await message.answer("Введіть ваше ім'я:")

@dp.message_handler(lambda message: message.text.isalpha())
async def ask_phone(message: types.Message):
    user_data[message.from_user.id]["name"] = message.text
    await message.answer("Поділіться номером телефону або введіть вручну:")

@dp.message_handler(lambda message: message.text.startswith("+") or message.text.isdigit())
async def finish(message: types.Message):
    uid = message.from_user.id
    user_data[uid]["phone"] = message.text
    data = user_data[uid]
    prices = {"5 футів": 1850, "7.5 футів": 2350, "15 футів": 3800, "30 футів": 6650}
    total = prices.get(data["size"], 0) * data["months"]
    text = (
        f"✅ Нова заявка:\n👤 Ім'я: {data['name']}\n📞 Телефон: {data['phone']}\n"
        f"📦 Контейнер: {data['size']}\n📍 Локація: {data['location']}\n"
        f"📅 Місяців: {data['months']}\n💰 Сума: {total} грн"
    )
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
    await message.answer("✅ Дякуємо! Ваша заявка відправлена.", reply_markup=main_menu())

# Обробка кнопки "На головну"
@dp.message_handler(lambda message: message.text == "🔙 На головну")
async def back_to_main(message: types.Message):
    await message.answer("↩️ Повернення в головне меню:", reply_markup=main_menu())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
