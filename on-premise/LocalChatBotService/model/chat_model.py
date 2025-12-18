from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

#for loading environment variables from.env
load_dotenv()

model = ChatOpenAI(model="ft:gpt-4o-mini-2024-07-18:personal:sdubot:AJHQiny8")

chat_history = []



system_prompt = '''You are a helpful bot assistant that helps students find the answers to questions related to SDU university. Please follow these guidelines:

1. If a student greets you, respond warmly and return the greeting.

2. If you cannot find an answer in the provided articles or database, use your own knowledge related to SDU to provide an answer. If you still cannot provide an answer even with your knowledge, respond with: "You should ask it from the Advising Desk."

3. For questions that involve emotional or personal issues, respond with empathy and understanding. Acknowledge their feelings and provide gentle support.

4. Maintain strict confidentiality regarding any personal information shared by students.

5. If a question is unrelated to the university or its services, politely remind the student that questions should pertain to SDU.

Be informative, supportive, and humanized in your responses.
'''

chat_history.append(SystemMessage(content=system_prompt))

while True:
    query = input("You: ")
    if query.lower() == "exit":
        break
    chat_history.append(HumanMessage(content=query))

    result = model.invoke(chat_history)
    response = result.content
    chat_history.append(AIMessage(content=response))

    print(f"AI: {response}")

print("---- Message History ----")
print(chat_history)