""" import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import FSInputFile
from PIL import Image, ImageDraw, ImageFont

# ==============================
#  CONFIG
# ==============================
BOT_TOKEN = "8492810863:AAFuTTrLIRgMLqKkE_vnOWGpxX-YkACPtu8"  # replace with your bot token
GLASSES_PATH = "assets/glasses.png"
OUTPUT_DIR = "output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "result.png")
os.makedirs(OUTPUT_DIR, exist_ok=True)  # <-- ensures folder exists

WATERMARK_TEXT = "$BMOG"


# Create bot & dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ==============================
#  IMAGE EDIT FUNCTION
# ==============================
def overlay_glasses_and_watermark(user_img_path):
    # Open user photo
    base = Image.open(user_img_path).convert("RGBA")

    # Open glasses
    glasses = Image.open(GLASSES_PATH).convert("RGBA")

    # Resize glasses to 40% width of image
    g_width = base.width // 2
    g_height = int(glasses.height * (g_width / glasses.width))
    glasses = glasses.resize((g_width, g_height))

    # Position glasses in middle
    g_x = (base.width - g_width) // 2
    g_y = base.height // 3
    base.paste(glasses, (g_x, g_y), glasses)

    # Add watermark
    draw = ImageDraw.Draw(base)
    font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), WATERMARK_TEXT, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    draw.text((base.width - text_w - 10, base.height - text_h - 10),
              WATERMARK_TEXT, font=font, fill=(0, 0, 255, 255))

    # Save result
    base.save(OUTPUT_PATH)
    return OUTPUT_PATH

# ==============================
#  HANDLERS
# ==============================

@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👓 Mog My PFP")]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "Welcome to **Blue Mog Bot** 💙🕶️\n\n"
        "Send me a photo or click the button below to mog your PFP with pit viper glasses + $BMOG watermark!",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@dp.message(F.text == "👓 Mog My PFP")
async def ask_photo(message: types.Message):
    await message.answer("Send me the photo you want to mog 🖼️")

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    # Save user photo
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_path = file.file_path
    dest = "user_photo.jpg"
    await bot.download_file(file_path, dest)

    # Process image
    result_img = overlay_glasses_and_watermark(dest)

    # Send back result
    out = FSInputFile(result_img)
    await message.reply_photo(out, caption="You're Mogged! 🕶️💙 #BMOG")

# ==============================
#  MAIN
# ==============================
async def main():
    print("Bot starting…")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
 """

""" import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🔹 Your bot token from BotFather
BOT_TOKEN = "8492810863:AAFuTTrLIRgMLqKkE_vnOWGpxX-YkACPtu8"

# 🔹 Public link to your hosted Mini App (Vercel/Netlify etc.)
WEBAPP_URL = "https://your-vercel-app.vercel.app"

# Create bot + dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# /start command
@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎨 Open Mini App",
                    web_app={"url": WEBAPP_URL}
                )
            ]
        ]
    )

    await message.answer(
        "💙 Welcome to Blue Mog Mini App!\n\nCreate and share your mogged creations.",
        reply_markup=keyboard
    )


async def main():
    print("Bot starting…")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
 """

""" import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    WebAppInfo, MenuButtonWebApp
)

BOT_TOKEN = "8492810863:AAFuTTrLIRgMLqKkE_vnOWGpxX-YkACPtu8"

# === HANDLERS ===
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🎨 Open Blue Mog Mini App",
                web_app=WebAppInfo(url="https://your-miniapp-url.com")
            )]
        ]
    )
    await message.answer(
        "🟦 Welcome to Blue Mog Mini App!\n\nTap below to start mogging 🕶️💙",
        reply_markup=keyboard
    )

# === MAIN ===
async def on_startup(bot: Bot):
    # Persistent bottom-left button
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="Blue Mog Mini App",
            web_app=WebAppInfo(url="https://your-miniapp-url.com")
        )
    )

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    dp.message.register(start_handler, CommandStart())

    await on_startup(bot)

    print("🤖 Bot starting…")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
 """

# if not MINIAPP_URL:
#     raise ValueError("❌ MINIAPP_URL is missing. Please set it in .env")



import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    WebAppInfo, MenuButtonWebApp
)
from keep_alive import keep_alive 


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MINIAPP_URL = os.getenv("MINIAPP_URL",)

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN is missing. Please set it in .env")



async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="👓 Mog My PFP",
                web_app=WebAppInfo(url=MINIAPP_URL)
            )],
            [
                InlineKeyboardButton(
                    text="📈 $BMOG Chart",
                    url="https://dexscreener.com/base/0x16a2EA8d47D9b062f8f4918bD5a4bB7BF0762951"
                ),
                InlineKeyboardButton(
                    text="🐦 Twitter",
                    url="https://x.com/bluemoggroup"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💬 Community",
                    url="https://t.me/BlueMogTG"
                ),
                InlineKeyboardButton(
                    text="🌐 Website",
                    url="https://hodl.fyi/t/bluemog"
                )
            ]
        ]
    )


    await message.answer(
        "🟦 Welcome to <b>Blue Mog Bot</b>!\n\n"
        "✨ Tap below to mog your PFP, join the fun, and spread $BMOG everywhere 🕶️💙",
        reply_markup=keyboard
    )



async def on_startup(bot: Bot):
 
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="Blue Mog Mini App",
            web_app=WebAppInfo(url=MINIAPP_URL)
        )
    )

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    dp.message.register(start_handler, CommandStart())

    await on_startup(bot)

    print("🤖 Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    keep_alive() 
    asyncio.run(main())

   


# import os
# import asyncio
# import logging
# from dotenv import load_dotenv
# from aiogram import Bot, Dispatcher, types
# from aiogram.filters import CommandStart
# from aiogram.types import (
#     InlineKeyboardMarkup, InlineKeyboardButton,
#     WebAppInfo, MenuButtonWebApp
# )

# # Load environment variables
# load_dotenv()

# BOT_TOKEN = os.getenv("BOT_TOKEN")
# MINIAPP_URL = os.getenv("MINIAPP_URL", "https://your-miniapp-url.com")

# if not BOT_TOKEN:
#     raise ValueError("❌ BOT_TOKEN is missing. Please set it in .env")


# # === HANDLERS ===
# async def start_handler(message: types.Message):
#     keyboard = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(
#                 text="👓 Mog My PFP",
#                 web_app=WebAppInfo(url=MINIAPP_URL)
#             )],
#             [
#                 InlineKeyboardButton(
#                     text="📈 $BMOG Chart",
#                     url="https://dexscreener.com/base/0x16a2EA8d47D9b062f8f4918bD5a4bB7BF0762951"
#                 ),
#                 InlineKeyboardButton(
#                     text="🐦 Twitter",
#                     url="https://x.com/bluemoggroup"
#                 )
#             ],
#             [
#                 InlineKeyboardButton(
#                     text="💬 Community",
#                     url="https://t.me/BlueMogTG"
#                 ),
#                 InlineKeyboardButton(
#                     text="🌐 Website",
#                     url="https://hodl.fyi/t/bluemog"
#                 )
#             ]
#         ]
#     )

#     await message.answer(
#         "🟦 Welcome to <b>Blue Mog Bot</b>!\n\n"
#         "✨ Tap below to mog your PFP, join the fun, and spread $BMOG everywhere 🕶️💙",
#         reply_markup=keyboard
#     )


# # === STARTUP ===
# async def on_startup(bot: Bot):
#     await bot.set_chat_menu_button(
#         menu_button=MenuButtonWebApp(
#             text="Blue Mog Mini App",
#             web_app=WebAppInfo(url=MINIAPP_URL)
#         )
#     )


# # === MAIN ===
# async def main():
#     logging.basicConfig(level=logging.INFO)
#     bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
#     dp = Dispatcher()

#     dp.message.register(start_handler, CommandStart())

#     await on_startup(bot)

#     print("🤖 Bot is running...")
#     await dp.start_polling(bot)


# if __name__ == "__main__":
#     asyncio.run(main())




