import numpy as np
from typing import List, Dict, Union

from embedding_request import generate_embeddings


class EmbeddingSimilarity:
    def __init__(self, pdf_embeddings: List[Dict]):
        self.pdf_embeddings = pdf_embeddings
        self.embeddings = self.__parse_embeddings__()
        self.mag_emb = np.linalg.norm(self.embeddings, axis=1)

    def __call__(self, question: str, top_similar: int = 5):
        question_embedding = self.__get_question_embedding__(question)
        similar_doc_indices = self.__get_similar_embeddings_indices__(
            question_embedding, top_similar)
        similar_docs = self.__fetch_documents_from_indices__(
            similar_doc_indices)
        return similar_docs

    def __parse_embeddings__(self):
        return np.array(
            list(map(lambda emb: emb.get("embedding"), self.pdf_embeddings)))

    def __get_question_embedding__(self, question: str):
        question_emb = generate_embeddings([question])[0]
        return question_emb.get("embedding")

    def __get_similar_embeddings_indices__(self, question_embedding: List,
                                           top_similar: int):
        mag_ques = np.linalg.norm(question_embedding)
        emb_mat = np.dot(self.embeddings, question_embedding)
        cosine_sim = emb_mat / (self.mag_emb * mag_ques)
        return np.argsort(cosine_sim)[::-1][:top_similar]

    def __fetch_documents_from_indices__(self, indices: List[int]):
        return [self.pdf_embeddings[ix].get("document") for ix in indices]