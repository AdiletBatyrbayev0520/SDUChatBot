import asyncio
from create_bot import bot, dp, scheduler, pg_db
from aiogram import Router, F
from aiogram.types import Message
from handlers.start import start_router
import logging
from utils.gpt_handler import GPTHandler
from decouple import config
# GPT-related configurations
GPT_API_KEY = config('GPT_API')
EMBEDDING_MODEL = "text-embedding-ada-002"
CHAT_MODEL = "ft:gpt-4o-mini-2024-07-18:personal:sdubot:AJHQiny8"
SDU_PLANNER_PATH = "telegram_bot/RAG_data/sdu_planned_embedded.csv"
SDU_LINKS_PATH = "telegram_bot/RAG_data/links_dataset_embedded.csv"

system_prompt = """You are a helpful bot assistant that helps students find the answers 
to questions related to SDU university. Please follow these guidelines:

1. If a student greets you, respond warmly and return the greeting.

2. If you cannot find an answer in the provided articles or are unsure about the answer, 
draw from your own knowledge related to SDU. If you lack sufficient information, kindly 
suggest that the student visit the Advising Desk for assistance.

3. For questions that involve emotional or personal issues, respond with empathy and 
understanding. Acknowledge their feelings and provide gentle support.

4. Maintain strict confidentiality regarding any personal information shared by students.

5. If a question is unrelated to the university or its services, politely remind the 
student that questions should pertain to SDU.

Be informative, supportive, and humanized in your responses."""

gpt_handler = GPTHandler(
    api_key=GPT_API_KEY,
    embedding_model=EMBEDDING_MODEL,
    chat_model=CHAT_MODEL,
    system_prompt=system_prompt,
)

logger = logging.getLogger(__name__)

gpt_router = Router()

@gpt_router.message()
async def handle_gpt_query(message: Message):
    user_query = message.text.strip()
    try:
        response = gpt_handler.ask(user_query, concatenated)
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

    # Load embeddings
    try:
        global concatenated
        concatenated = gpt_handler.load_embeddings(SDU_PLANNER_PATH, SDU_LINKS_PATH)
        logger.info("Embeddings loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load embeddings: {e}")
        await pg_db.disconnect()
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

if __name__ == "__main__":
    asyncio.run(main())
