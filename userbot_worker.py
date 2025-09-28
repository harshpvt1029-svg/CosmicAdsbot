from telethon import TelegramClient, events, sync
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import save_account, get_accounts
import os

API_ID = int(os.getenv("24945402"))
API_HASH = os.getenv("6118e50f5dc4e3a955e50b22cf673ae2")

# Start user session + OTP
async def start_userbot_session(callback, user_id):
    msg = await callback.message.reply("Send your number in international format (+91xxxxxx)")
    # Here normally you would wait for user reply with phone
    # Then send OTP using Telethon, get session, save session in MongoDB
    await callback.message.reply("✅ Account added (OTP part to be implemented)")
