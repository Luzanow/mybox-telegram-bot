import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "7680848123:AAGeVHb8glcUbbb-9IEcdGAauNcG2p2Oeag"
ADMIN_CHAT_ID = "5498505652"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}

main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add("📦 Орендувати контейнер")
main_menu.add("📍 Перегляд локацій")
main_menu.add("📞 Зв'язатися з нами")

# Старт
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("👍 Вітаємо у MyBox!\nОберіть опцію нижче:", reply_markup=main_menu)

# Перегляд локацій
@dp.message_handler(lambda m: m.text == "📍 Перегляд локацій")
async def view_locations(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    locations = [
        ("📍 Лугова 9", "https://maps.google.com/?q=50.425689,30.483118"),
        ("📍 Плодова 1", "https://maps.google.com/?q=50.400233,30.457452"),
        ("📍 Дегтярівська 21", "https://maps.google.com/?q=50.457832,30.480274"),
        ("📍 Сім'ї Сосніних 3", "https://maps.google.com/?q=50.434291,30.464987"),
        ("📍 Лобановського 119", "https://maps.google.com/?q=50.426594,30.495850"),
        ("📍 Сортувальна 5", "https://maps.google.com/?q=50.464835,30.490526"),
        ("📍 Пухівська 4А", "https://maps.google.com/?q=50.422968,30.510332"),
        ("📍 Новокостянтинівська 18", "https://maps.google.com/?q=50.438151,30.497368"),
        ("📍 Бальзака 85А", "https://maps.google.com/?q=50.395106,30.455319"),
        ("📍 Будіндустрії 5", "https://maps.google.com/?q=50.476872,30.464531"),
        ("📍 Бориспільська 9", "https://maps.google.com/?q=50.446179,30.476200"),
        ("📍 Віскозна 1", "https://maps.google.com/?q=50.453824,30.487111"),
        ("📍 Промислова 4", "https://maps.google.com/?q=50.425598,30.508532")
    ]
    for loc, link in locations:
        keyboard.add(types.InlineKeyboardButton(text=loc, url=link))
    await message.answer("Оберіть локацію для перегляду на мапі:", reply_markup=keyboard)

# Зв’язок
@dp.message_handler(lambda m: m.text == "📞 Зв'язатися з нами")
async def contact(message: types.Message):
    contact_kb = types.InlineKeyboardMarkup()
    contact_kb.add(types.InlineKeyboardButton("📨 Написати в Telegram", url="https://t.me/Taras031990"))
    await message.answer(
        "📞 Контактна особа: Тарас\n📱 Телефон: +380 (95) 938 73 17\n🌐 Сайт: https://mybox.kiev.ua",
        reply_markup=contact_kb
    )

# Оренда
@dp.message_handler(lambda m: m.text == "📦 Орендувати контейнер")
async def rent_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("5 футів - 1850 грн", "7.5 футів - 2350 грн")
    keyboard.add("15 футів - 3800 грн", "30 футів - 6650 грн")
    await message.answer("Оберіть розмір контейнера з ціною:", reply_markup=keyboard)

@dp.message_handler(lambda m: "футів" in m.text)
async def rent_location(message: types.Message):
    user_data[message.from_user.id] = {"size": message.text.split(" - ")[0]}
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    locations = [
        "📍 Лугова 9", "📍 Плодова 1", "📍 Дегтярівська 21", "📍 Сім'ї Сосніних 3", "📍 Лобановського 119",
        "📍 Сортувальна 5", "📍 Пухівська 4А", "📍 Новокостянтинівська 18", "📍 Бальзака 85А",
        "📍 Будіндустрії 5", "📍 Бориспільська 9", "📍 Віскозна 1", "📍 Промислова 4"
    ]
    for loc in locations:
        keyboard.add(loc)
    await message.answer("Оберіть локацію:", reply_markup=keyboard)

@dp.message_handler(lambda m: m.text.startswith("📍"))
async def rent_months(message: types.Message):
    user_data[message.from_user.id]["location"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*[f"{i} місяців" if i > 1 else "1 місяць" for i in range(1, 13)])
    await message.answer("Оберіть термін оренди (1–12 місяців):", reply_markup=keyboard)

@dp.message_handler(lambda m: "місяц" in m.text.lower())
async def rent_name(message: types.Message):
    try:
        user_data[message.from_user.id]["months"] = int(message.text.split()[0])
        await message.answer("Введіть ваше ім'я:")
    except Exception:
        await message.answer("Будь ласка, виберіть термін з кнопок.")

@dp.message_handler(lambda m: m.text.replace(" ", "").isalpha())
async def rent_phone(message: types.Message):
    user_data[message.from_user.id]["name"] = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton("📱 Поділитися номером", request_contact=True))
    keyboard.add("Ввести вручну")
    await message.answer("Поділіться номером або введіть вручну:", reply_markup=keyboard)

@dp.message_handler(content_types=['contact'])
async def contact_received(message: types.Message):
    user_data[message.from_user.id]["phone"] = message.contact.phone_number
    await finalize_application(message)

@dp.message_handler(lambda m: m.text.replace("+", "").isdigit())
async def manual_phone(message: types.Message):
    user_data[message.from_user.id]["phone"] = message.text
    await finalize_application(message)

async def finalize_application(message: types.Message):
    uid = message.from_user.id
    data = user_data.get(uid, {})
    prices = {"5 футів": 1850, "7.5 футів": 2350, "15 футів": 3800, "30 футів": 6650}
    total = prices.get(data.get("size", ""), 0) * data.get("months", 1)

    result = (
        f"✅ Нова заявка:\n"
        f"👤 Ім'я: {data.get('name')}\n"
        f"📞 Телефон: {data.get('phone')}\n"
        f"📦 Контейнер: {data.get('size')}\n"
        f"📍 Локація: {data.get('location')}\n"
        f"🗓️ Місяців: {data.get('months')}\n"
        f"💰 Сума: {total} грн"
    )
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=result)
    await message.answer("✅ Дякуємо! Ваша заявка відправлена.", reply_markup=main_menu)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
