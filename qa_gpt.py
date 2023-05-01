import openai
import requests
from typing import List, Dict, Union

from configs import OPENAI_API_KEY, OPENAI_CHAT_COMPLETION_URL, OPENAI_CHAT_COMPLETION_MODEL

openai.api_key = OPENAI_API_KEY


def chat_completion(messages: List[Dict]):
    resp = openai.ChatCompletion.create(model=OPENAI_CHAT_COMPLETION_MODEL,
                                        messages=messages)
    # print(resp)
    if "error" in resp:
        print(resp)
        return None
    return resp.get("choices")[0].get("message").get("content")


def extract_answer(documents: List[str], question: str):

    system_message = {
        "role":
        "system",
        "content":
        "You are a Question Answering model. The user will provide a document in triple backticks and a question in tiple quotes. Based on the question and the document extract the answer if the answer is there if not reply, ```I cannot find an answer! Sorry```"
    }
    qa = {
        "role":
        "user",
        "content":
        f'''Document: ```{'. '.join([d for d in documents])}``` Question: "{question}"'''
    }
    messages = [system_message, qa]
    answer = chat_completion(messages)
    return answer
