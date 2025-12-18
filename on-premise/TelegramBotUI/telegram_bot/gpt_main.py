from utils.gpt_handler import GPTHandler
from decouple import config

GPT_API_KEY = config("GPT_API")
EMBEDDING_MODEL = "text-embedding-ada-002"
CHAT_MODEL = "ft:gpt-4o-mini-2024-07-18:personal:sdubot:AJHQiny8"
SDU_PLANNER_PATH = "sdu_planned_embedded.csv"
SDU_LINKS_PATH = "links_dataset_embedded.csv"
# system_prompt = "You are a helpful bot assistant for SDU students."
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

def main():
    gpt_handler = GPTHandler(GPT_API_KEY, EMBEDDING_MODEL, CHAT_MODEL, system_prompt)
    concatenated = gpt_handler.load_embeddings(SDU_PLANNER_PATH, SDU_LINKS_PATH)

    while True:
        query = input("User: ")
        if query.lower() == "exit":
            break
        response = gpt_handler.ask(query, concatenated)
        print(f"Bot: {response}")

if __name__ == "__main__":
    main()
    