import json
import argparse
from read_pdf import get_pdf_content
from generate_embedding import OpenAIEmbeddings
from qa import EmbeddingSimilarity
from qa_gpt import extract_answer

# reading file locally
# pdf_content = get_pdf_content(
#     "test_pdfs/self_supervised_learning_fair_meta.pdf")

# reading a pdf from a url

# create an ArgumentParser object
parser = argparse.ArgumentParser()

# add the arguments to the parser
parser.add_argument("--save_answers",
                    type=bool,
                    default=False,
                    help="whether to save the answers")
parser.add_argument("--pdf_path",
                    type=str,
                    default="test_pdfs/self_supervised_learning_fair_meta.pdf",
                    required=True,
                    help="path of the pdf file")

# parse the arguments from the command line
args = parser.parse_args()

# access the arguments
save_answers = args.save_answers
pdf_path = args.pdf_path

# print the arguments
print("Save answers:", save_answers)

pdf_content = get_pdf_content(pdf_path)

# divide the PDF into chunks and generate an embedding
pdf_embedding = OpenAIEmbeddings()
results = pdf_embedding(pdf_content, 1_000)

# similariy object

embedding_similarity = EmbeddingSimilarity(results)

idx = 0
while True:
    question = input("Question: ")
    docs = embedding_similarity(question)
    answer = extract_answer(docs, question)
    idx += 1
    if answer:
        print(answer)
        if save_answers:
            with open(f"{'_'.join(question.split())}_{idx}.json", "w") as fp:
                json.dump(
                    {
                        "question": question,
                        "similar_docs": docs,
                        "answer": answer
                    }, fp)