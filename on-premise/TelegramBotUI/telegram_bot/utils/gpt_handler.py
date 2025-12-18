import ast
import pandas as pd
from scipy import spatial
from openai import OpenAI
import tiktoken

class GPTHandler:
    def __init__(self, api_key: str, embedding_model: str, chat_model: str, system_prompt: str):
        self.client = OpenAI(api_key=api_key)
        self.embedding_model = embedding_model
        self.chat_model = chat_model
        self.system_prompt = system_prompt  

    def load_embeddings(self, planner_path: str, links_path: str) -> pd.DataFrame:
        """Load and merge embeddings from CSV files."""
        sdu_planner = pd.read_csv(planner_path)
        sdu_links = pd.read_csv(links_path)
        sdu_planner['embedding'] = sdu_planner['embedding'].apply(ast.literal_eval)
        sdu_links['embedding'] = sdu_links['embedding'].apply(ast.literal_eval)
        return pd.concat([sdu_planner, sdu_links], ignore_index=True)

    def strings_ranked_by_relatedness(self, query: str, df: pd.DataFrame, top_n: int = 100):
        """Rank strings by relatedness to the query using cosine similarity."""
        query_embedding_response = self.client.embeddings.create(
            model=self.embedding_model,
            input=query,
        )
        query_embedding = query_embedding_response.data[0].embedding
        strings_and_relatednesses = [
            (row["text"], 1 - spatial.distance.cosine(query_embedding, row["embedding"]))
            for _, row in df.iterrows()
        ]
        strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
        return zip(*strings_and_relatednesses[:top_n])

    def num_tokens(self, text: str) -> int:
        """Count the number of tokens in a string."""
        encoding = tiktoken.encoding_for_model(self.chat_model)
        return len(encoding.encode(text))

    def query_message(self, query: str, df: pd.DataFrame, token_budget: int = 3596):
        """Prepare a query message for GPT."""
        strings, _ = self.strings_ranked_by_relatedness(query, df)
        introduction = 'Use the below articles on SDU Data. If the answer cannot be found in the articles, use your own knowledge or write "I could not find an answer."'
        question = f"\n\nQuestion: {query}"
        message = introduction
        for string in strings:
            next_article = f'\n\nSDU article section:\n"""\n{string}\n"""'
            if self.num_tokens(message + next_article + question) > token_budget:
                break
            message += next_article
        return message + question

    def ask(self, query: str, df: pd.DataFrame, token_budget: int = 3596):
        """Answer a query using GPT."""
        message = self.query_message(query, df, token_budget)
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": message},
        ]
        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message.content
