# 👩‍⚕️ Doc-tor 👨‍⚕️

Doc-tor is a command-line tool that allows you to ask questions about a PDF document and get answers using OpenAI Embeddings API and GPT Chat Completion API. It uses Numpy for getting similarity between the question and the document content.

## Installation

To install Doc-tor, simply clone this repository and install the required packages using pip:

```
git clone https://github.com/your-username/doc-tor.git
cd doc-tor
pip install -r requirements.txt
```

# .env File

Before using Doc-tor, you need to create a `.env` file in the root directory of the project. This file should contain the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key. This is required to use the OpenAI Embeddings API and GPT Chat Completion API. You can obtain your API key from the OpenAI website (https://platform.openai.com/account/api-keys).
- `OPENAI_API_URL`: The URL of the OpenAI Embeddings API. This should be set to `"https://api.openai.com/v1/embeddings"`.
- `OPENAI_EMBEDDING_MODEL`: The name of the OpenAI Embeddings model to use. This should be set to `"text-embedding-ada-002"`.
- `OPENAI_CHAT_COMPLETION_API`: The API endpoint of the OpenAI GPT Chat Completion API. This should be set to `"https://api.openai.com/v1/completions"`.
- `OPENAI_CHAT_COMPLETION_MODEL`: The name of the OpenAI GPT model to use for chat completion. This should be set to `"text-davinci-002"`.

Here's an example `.env` file:

```
OPENAI_API_KEY=your-openai-api-key
OPENAI_API_URL="https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL="text-embedding-ada-002"
OPENAI_CHAT_COMPLETION_API="https://api.openai.com/v1/completions"
OPENAI_CHAT_COMPLETION_MODEL="text-davinci-002"
```


Note that you should replace `your-openai-api-key` with your actual OpenAI API key. This file should be kept confidential and not shared with anyone else.



## Usage

To use Doc-tor, simply run the `run.py` script and provide the path of the PDF file that you want to query:


```
python run.py --pdf_path /path/to/your/pdf
```



You can then ask questions about the PDF document and get answers in real-time. If you want to save the answers to a file, you can use the `--save_answers` flag:

```
python main.py --pdf_path /path/to/your/pdf --save_answers True
```


This will save the answers to separate JSON files in the current directory.

## Implementation

Doc-tor uses OpenAI Embeddings API to generate embeddings for the PDF document, which are then used to calculate the similarity between the document content and the user's question. The `qa_gpt.py` module uses GPT Chat Completion API to answer the question based on the most similar part of the document content. No vector database is used as it is not needed for local use. LangChain is also not used, as the code is straightforward.

## Future Improvements

Some improvements that could be made to Doc-tor in the future include:

- Using Redis or a similar in-memory data store to cache the embeddings for faster querying in production.
- Dealing with higher context length to enable answering more complex questions.
- Adding support for more document formats, such as Microsoft Word and Google Docs.

## License

Doc-tor is licensed under the MIT License. See the `LICENSE` file for more information.
