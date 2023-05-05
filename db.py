import os
import re
import struct
import duckdb
from typing import List, Dict, Tuple
from tqdm.auto import trange

from configs import DB_PATH


class PDFDB:
    def __init__(self):
        self.connection = duckdb(DB_PATH)

    def __get_inserted_id__(self):
        return self.connection.execute(
            "SELECT last_insert_rowid()").fetchone()[0]


class PDFTable(PDFDB):
    def __init__(self):
        super().__init__()

    def __call__(self, pdf_link: str):
        try:
            self.__insert_pdf__(pdf_link)
            return self.__get_inserted_id__()
        except Exception as err:
            raise Exception(err)

    # def __get_inserted_id__(self):
    #     return self.connection.execute(
    #         "SELECT last_insert_rowid()").fetchone()[0]

    def __insert_pdf__(self, pdf_link: str):
        self.connection.execute(f"""
        INSERT INTO PDF (pdf_link) values ('{pdf_link}')
        """)


class PagesTable(PDFDB):
    def __init__(self):
        super().__init__()

    def __call__(self, content: str, page_no: int, pdf_id: int):
        self.__insert_page_content__(content, page_no, pdf_id)
        return self.__get_inserted_id__()

    def __insert_page_content__(self, content: str, page_no: int, pdf_id: int):
        self.connection.execute(f"""
        INSERT INTO Pages (page_content, page_no, pdf_id)
        VALUES ('{content}', '{page_no}', '{pdf_id}')
        """)

    # def __insert_page_content__(self,
    #                             pdf_id: int,
    #                             pages: List[Dict],
    #                             bs: int = 100):

    #     for ix in range(0, len(pages), bs):

    #         batch_pages = pages[ix:ix + bs]

    #         page_values = ", ".join(
    #             f"('{page['content']}'), ({page['page_no']}), ({pdf_id})"
    #             for page in batch_pages)

    #         self.connection.execute(f"""
    #         INSERT INTO Pages (page_content, page_no, pdf_id) VALUES {page_values}
    #         """)


class ChunksTable(PDFDB):
    def __init__(self):
        super().__init__()

    def __call__(self,
                 pdf_id: int,
                 page_id: int,
                 chunks: List[Dict],
                 bs: int = 100):
        try:
            self.__insert_chunk__(pdf_id, page_id, chunks, bs)
            return True
        except Exception as err:
            raise Exception(err)

    def __encode_embeddings__(self, embedding: List[float]):
        return struct.pack(f"{len(embedding)}f", *embedding)

    def __insert_chunk__(self, pdf_id: int, page_id: int, chunks: List[Dict],
                         bs: int):

        for ix in trange(0, len(chunks), bs):

            chunk_batch = chunks[ix:ix + bs]

            chunk_batch = list(
                map(
                    lambda chunk: self.__encode_embeddings__(
                        chunk.get("embedding")), chunk_batch))

            chunk_values = ", ".join(
                f"('{chunk['chunk_content']}'), ({chunk['embedding'].hex()}), ('{page_id}'), ('{pdf_id}')"
                for chunk in chunk_batch)

            self.connection.execute(f"""
            INSERT INTO Chunks (chunk_content, chunk_embedding, page_id, pdf_id)
            VALUES {chunk_values}
            """)


class Queries(PDFDB):
    def __init__(self):
        super().__init__()

    def __decode_embeddings__(self, chunk_embedding):
        embedding_bytes = bytes.fromhex(chunk_embedding)
        embedding = struct.unpack(f"{len(embedding_bytes // 4)}f",
                                  embedding_bytes)
        return embedding

    def query_chunk_embeddings(self, pdf_id):
        result = self.connection.execute(f"""
        SELECT chunk_embedding, chunk_content FROM Chunks
        WHERE pdf_id = {pdf_id}
        """)
        return list(
            map(
                lambda chunk: {
                    "chunk_embedding": self.__decode_embeddings__(chunk[0]),
                    "chunk_content": chunk[1],
                    "page_no": chunk[2]
                }, result))
