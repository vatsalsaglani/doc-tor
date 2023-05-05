import duckdb

from configs import DB_PATH


class CreateDB:
    def __init__(self):
        self.connection = duckdb(DB_PATH)

    def __call__(self):
        self.__create_pdf_table__()
        self.__create_pages_table__()
        self.__create_chunks_table__()
        self.__create_question_table__()
        self.__create_indices__()

    def __create_pdf_table__(self):

        try:
            self.connection.execute("""
            CREATE TABLE IF NOT EXISTS PDF (
                pdf_id INTEGER PRIMARY KEY AUTOINCREMENT,
                pdf_link TEXT NOT NULL
            )
            """)
            return True
        except Exception as err:
            raise Exception(err)

    def __create_pages_table__(self):

        try:
            self.connection.execute("""
            CREATE TABLE IF NOT EXISTS Pages (
                page_id INTEGER PRIMARY KEY AUTOINCREMENT,
                page_content TEXT NOT NULL,
                page_no INTEGER NOT NULL,
                pdf_id INTEGER NOT NULL REFERENCES PDF(pdf_id)
            )
            """)
            return True
        except Exception as err:
            raise Exception(err)

    def __create_chunks_table__(self):

        try:
            self.connection.execute("""
            CREATE TABLE IF NOT EXISTS Chunks (
                chunk_id INTEGER PRIMARY KEY AUTOINCREMENT,
                chunk_content TEXT NOT NULL,
                chunk_embedding BLOB NOT NULL,
                page_id INTEGER NOT NULL REFERENCES Pages(page_id),
                pdf_id INTEGER NOT NULL REFERENCES PDF(pdf_id)
            )
            """)
            return True
        except Exception as err:
            raise Exception(err)

    def __create_question_table__(self):

        try:
            self.connection.execute("""
            CREATE TABLE IF NOT EXISTS Questions (
                question_id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_content TEXT NOT NULL,
                question_embedding BLOB NOT NULL
                pdf_id INTEGER NOT NULL REFERENCES PDF(pdf_id)
            )
            """)
            return True
        except Exception as err:
            raise Exception(err)

    def __create_indices__(self):

        try:
            self.connection.execute("""
            ALTER TABLE Chunks ADD COLUMN IF NOT EXISTS pdf_id INTEGER NOT NULL REFERENCES PDF(pdf_id)
            """)

            self.connection.execute("""
            ALTER TABLE Chunks ADD COLUMN IF NOT EXISTS cosine_similarity FLOAT
            """)

            self.connection.execute("""
            ALTER TABLE Questions ADD COLUMN IF NOT EXISTS pdf_id INTEGER NOT NULL REFERENCES PDF(pdf_id)
            """)

            self.connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_chunks_pdf_id ON Chunks(pdf_id)
            """)

            self.connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_chunks_cosine_similarity ON Chunks(cosine_similarity)
            """)

            self.connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_questions_pdf_id ON Questions(pdf_id)
            """)
        except Exception as err:
            raise Exception(err)

            return True