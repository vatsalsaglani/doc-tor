import json
import asyncio
import aiohttp
from typing import List, Dict
from configs import *
from tqdm.auto import tqdm, trange


async def http_post(url: str, input_text):
    async with aiohttp.ClientSession() as session:
        async with session.post(url,
                                json={
                                    "input": input_text,
                                    "model": OPENAI_EMBEDDING_MODEL
                                },
                                headers={
                                    "Authorization":
                                    f"Bearer {OPENAI_API_KEY}",
                                    "Content-Type": "application/json",
                                    "Accept": "application/json"
                                }) as response:
            return await response.json()


async def __generate_embeddings__(input_texts: List[str]):
    tasks = [
        asyncio.create_task(http_post(OPENAI_API_URL, input_text))
        for input_text in input_texts
    ]
    # results = await asyncio.gather(*tasks)
    results = []
    with tqdm(total=len(tasks)) as pbar:
        for coro in asyncio.as_completed(tasks):
            result = await coro
            results.append(result)
            pbar.update(1)
    # print(json.dumps(results, indent=4))
    return [{
        "id": ix,
        "document": input_texts[ix],
        "embedding": results[ix].get("data")[0].get("embedding")
    } for ix in range(len(results))]


def generate_embeddings(input_texts: List[str]):
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(__generate_embeddings__(input_texts))
    return results


# if __name__ == "__main__":
#     op = generate_embeddings([
#         "using Python aiohttp and fastapi how to make async post requests with different input for different requests and return the response in a variable",
#         "To make asynchronous POST requests with different input for different requests and return the response in a variable using Python's aiohttp and FastAPI, you can use the following code:"
#     ])
#     print(op)
