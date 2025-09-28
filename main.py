from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from db import get_user, add_user, get_admins
from userbot_worker import start_userbot_session

BOT_TOKEN = os.getenv("8388938837:AAFLBd4BHMUnbwelsqcXbsjtuz6t7-nTZoc")
API_ID = int(os.getenv("24945402"))
API_HASH = os.getenv("6118e50f5dc4e3a955e50b22cf673ae2")
OWNER = os.getenv("@LordHarsh")
ADMINS = os.getenv("@Sherrbst,@King_Bst34").split(",")

bot = Client("controller_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --------- START COMMAND ---------
@bot.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    user = get_user(user_id)
    if not user:
        add_user(user_id)
    # Buttons: Force Join Channel/Group
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Join Channel", url="https://t.me/CosmicAdsPro")],
        [InlineKeyboardButton("Privacy Policy", url=os.getenv("https://gist.github.com/harshpvt1029-svg/504fba01171ef14c81f9f7143f5349c5#file-privacy-policy"))],
        [InlineKeyboardButton("I Have Read ✅", callback_data="open_dashboard")]
    ])
    await message.reply("Welcome! Please join our channel and read privacy policy first.", reply_markup=markup)

# -------- DASHBOARD BUTTONS --------
@bot.on_callback_query()
async def callbacks(client, callback):
    data = callback.data
    user_id = callback.from_user.id

    if data == "open_dashboard":
        # Show Dashboard buttons
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Accounts", callback_data="add_accounts")],
            [InlineKeyboardButton("🗂 My Accounts", callback_data="my_accounts")],
            [InlineKeyboardButton("✏️ Set Ad Message", callback_data="set_ad")],
            [InlineKeyboardButton("⏱ Set Time Intervals", callback_data="set_interval")],
            [InlineKeyboardButton("▶️ Start/Stop Ad", callback_data="start_stop")],
            [InlineKeyboardButton("➕ Add Groups", callback_data="add_groups")],
            [InlineKeyboardButton("💎 Premium", callback_data="premium")],
            [InlineKeyboardButton("📞 Support", callback_data="support")],
            [InlineKeyboardButton("Logout", callback_data="logout")]
        ])
        await callback.message.edit("📊 Dashboard", reply_markup=markup)

    # Other callbacks → we call functions from userbot_worker.py
    elif data == "add_accounts":
        await start_userbot_session(callback, user_id)
    elif data == "premium":
        await callback.message.edit(f"💎 Premium Info:\n{os.getenv('PREMIUM_LINK')}")
    elif data == "support":
        admins = "\n".join([f"@{a}" for a in ADMINS])
        await callback.message.edit(f"📞 Support Admins:\n{admins}")
    elif data.startswith("approve_"):
        username = data.split("_")[1]
        await callback.message.edit(f"✅ User @{username} approved by admin.")

bot.run()
