import asyncio
import os
from create_bot import bot, dp, scheduler, pg_db
from aiogram import Router, F
from aiogram.types import Message
from handlers.start import start_router
import logging
from utils.gpt_handler import GPTHandler
from decouple import config
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# GPT-related configurations
EMBEDDING_MODEL = config('EMBEDDING_MODEL')
CHAT_MODEL = config('CHAT_MODEL')
SYSTEM_PROMPT = config('SYSTEM_PROMPT')
CONTEXT_Q__SYSTEM_PROMPT = config('CONTEXT_Q__SYSTEM_PROMPT')
# Vector database path
current_dir = os.path.dirname(os.path.abspath(__file__))
pdf_dir = os.path.join(current_dir, "db_pdf")
persistent_directory = os.path.join(current_dir, "db", "chroma_db_with_metadata")


gpt_handler = GPTHandler(
    persistent_directory=persistent_directory,
    pdf_directory=pdf_dir,
    embedding_model=EMBEDDING_MODEL,
    chat_model=CHAT_MODEL,
    system_prompt=(SYSTEM_PROMPT),
    contextualization_prompt=(CONTEXT_Q__SYSTEM_PROMPT)
)


logger = logging.getLogger(__name__)

gpt_router = Router()

@gpt_router.message()
async def handle_gpt_query(message: Message):
    user_query = message.text.strip()
    try:
        response = gpt_handler.ask(user_query)
        await message.answer(response)
    except Exception as e:
        await message.answer(f"Error processing your request: {e}")

async def main():
    # Connect to the database
    try:
        await pg_db.connect()
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        return

    # Add routers
    dp.include_router(start_router)
    dp.include_router(gpt_router)

    # Start bot polling
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await pg_db.disconnect()
        print("Disconnect")
if __name__ == "__main__":
    asyncio.run(main())
