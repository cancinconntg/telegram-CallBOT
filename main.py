# -*- coding: utf-8 -*-
import os

from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from pymongo import MongoClient
from pyrogram import Client
from tgvoip_pyrogram import VoIPFileStreamService

from bot.bot import Bot

load_dotenv()


# constants
# ---------
BOT_SESSION_NAME = "AQCXkx4cYtxiBHlQe3Jy3bEwWDKR2Ic9Qhs9ZxdWDq661TsW8cVn9MNyDjAaNf8sTZ0NyIyWDyynPa_qQTYKfCKKp6T8I6pOVJ_4mp1y_Yklq91ZC5pZKNz8nWjot6ZIfmMSGAVJCBdfMCwPAoQ2jdcK6OhxtSCKe9HqzHfDSCBHrTTLGwsjSuIoO7LWjOyGAm0a-_IAOVJ8MYgdox1MvkYg5QGaRigNn2DzN_1xy6jLA6RyOgxbgzOub_f2Opzas8l77Ol9Ana-BBjMO2_vNcCg29bPDT63iSkWkit-FD2NREmm9j9Da598mpcIk84lVmvVlzfwb7mm0c1HpAY4ZoUlZzBLXgE"
USER_SESSION_NAME = "AQAB9_FoFJ1jHpeE_gSzKp8AbrZOmT-BZzz_ZZD94uoslq83lH7M3KOSbQY236_1fjLdIkV2ouhEUd0pMNRN-zRHvRHaF4lC1M-Pe2C_vbt9_1XvZ8IEEgVu-z-mqgGTgAJly5nVVhsv_NkAlk0ov6Y3dY_attEIM_B-k-i7SQTtkuenOfbTiSEz6gvIra9UnGJ6hBT57WEIT06Cp-9bONH4cn-AP7NLPRdf0hH8qNMBCdxkbG25aYmW4MSvcRCZSXGGEIDDF9CVAkrJ1qEG36-h32M7jl8UTWlQtVRt2Za64Zn-RDWvAS3LzHpP0gQwIEXFA-0YPTznkwiGRz_T1xavYknMbwA"
APP_ID = "3381924"
APP_HASH = "b2bc3786b7fea440bb2e0a8ff39a09f9"
MONGO_URI = "mongodb+srv://erich:erich@cluster0.b3rfv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
BOT_NAME = "Hrr"
USER_NAME = "Can"
DB_NAME = "Cluster0"


def main():

    print("Creating the scheduler...")
    scheduler = BackgroundScheduler()
    scheduler.start()

    print("Connecting to the database...")
    db_client = MongoClient(MONGO_URI)
    database = db_client[DB_NAME]

    print("Instantiating the Pyrogram bot client...")
    pyrogram_bot_client = Client(
        session_name=BOT_SESSION_NAME, api_id=APP_ID, api_hash=APP_HASH
    )

    print("Instantiating the Pyrogram user client...")
    pyrogram_user_client = Client(
        session_name=USER_SESSION_NAME, api_id=APP_ID, api_hash=APP_HASH
    )

    voip_service = VoIPFileStreamService(pyrogram_user_client, receive_calls=False)

    print("Instantiating the bot...")

    # prov test group. TODO manage with database and admin commands.
    whitelist = []
    with open("whitelist", "r+") as f:
        for line in f.readlines():
            whitelist.append(int(line))

    bot = Bot(
        name=BOT_NAME,
        user_name=USER_NAME,
        bot_client=pyrogram_bot_client,
        user_client=pyrogram_user_client,
        database=database,
        scheduler=scheduler,
        voip_service=voip_service,
        whitelisted_chats=whitelist,
    )

    bot.load_modules(submodule_advanced_calls=True)
    bot.run()


if __name__ == "__main__":
    main()
