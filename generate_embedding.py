import os
import re
import json
import tiktoken
from typing import Any, List, Dict, Union

from embedding_request import generate_embeddings


class OpenAIEmbeddings:
    def __init__(self, model_name: str = "text-embedding-ada-002"):
        self.encoding = tiktoken.encoding_for_model(model_name)
        self.flatten = lambda lst: [
            item for sublist in lst for item in sublist
        ]

    def __call__(self,
                 input_pdf_content: List[Dict],
                 chunk_size: int = 5_000) -> Union[List[Dict], None]:
        input_texts = self.__divide_document__(input_pdf_content, chunk_size)
        results = generate_embeddings(
            self.flatten(
                list(map(lambda txt: txt.get("page_divs"), input_texts))))
        return results

    def __divide_document__(self, input_pdf_contents: List[Dict],
                            chunk_size: int):
        return list(
            map(
                lambda input_page_content: self.__divide_page__(
                    input_page_content, chunk_size), input_pdf_contents))

    def __divide_page__(self, input_page_content: Dict, chunk_size: int):
        tokens, num_tokens = self.__tokens_from_string__(
            input_page_content.get("content"))
        # page_divs = []
        input_page_content["page_divs"] = []
        for ix in range(0, len(tokens), chunk_size):
            toks = tokens[ix:ix + chunk_size]
            txt = self.encoding.decode(toks)
            input_page_content["page_divs"].append(txt)
        return input_page_content

    def __tokens_from_string__(self, string: str):
        tokens = self.encoding.encode(string)
        return tokens, len(tokens)


# if __name__ == "__main__":
#     emb = OpenAIEmbeddings()
#     texts = [
#         "using Python aiohttp and fastapi how to make async post requests with different input for different requests and return the response in a variable",
#         "To make asynchronous POST requests with different input for different requests and return the response in a variable using Python's aiohttp and FastAPI, you can use the following code:"
#     ]
#     print(emb(texts))