import PyPDF2
import requests
import io


def is_url_or_file_path(string: str):
    return string.startswith("http://") or string.startswith(
        "https://") or string.startswith("www.")


def read_pdf_from_url(url: str):
    response = requests.get(url)

    # check if the request was successful (status code 200)
    if response.status_code == 200:
        # create a PdfReader object using the response content
        pdf = io.BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf)

        return pdf_reader
    return None


def read_pdf_from_local(file_path: str):
    with open(file_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        return pdf_reader


def get_pdf_content_from_url(url: str):
    pdf_data = []
    pdf_reader = read_pdf_from_url(url)
    if not pdf_reader:
        raise Exception("Invalid URL")
    num_pages = len(pdf_reader.pages)
    # num_pages = pdf_reader.getNumPages()

    # Loop through each page and extract the text
    for page_num in range(num_pages):
        # Get the page object
        page_obj = pdf_reader.pages[page_num]
        # page_obj = pdf_reader.getPage(page_num)

        # Extract the text from the page
        text = page_obj.extract_text()

        # Print the text
        # print('Page', page_num + 1, ':\n', text)

        pdf_data.append({"page_no": page_num + 1, "content": text})

    return pdf_data


def get_pdf_content_from_local(file_path: str):

    pdf_data = []

    # pdf_reader = read_pdf_from_url(file_path) if is_url_or_file_path(
    #     file_path) else read_pdf_from_local(file_path)

    # if pdf_reader:

    with open(file_path, 'rb') as pdf_file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Get the number of pages in the PDF file
        num_pages = len(pdf_reader.pages)
        # num_pages = pdf_reader.getNumPages()

        # Loop through each page and extract the text
        for page_num in range(num_pages):
            # Get the page object
            page_obj = pdf_reader.pages[page_num]
            # page_obj = pdf_reader.getPage(page_num)

            # Extract the text from the page
            text = page_obj.extract_text()

            # Print the text
            # print('Page', page_num + 1, ':\n', text)

            pdf_data.append({"page_no": page_num + 1, "content": text})

        return pdf_data


def get_pdf_content(path: str):
    if is_url_or_file_path(path):
        return get_pdf_content_from_url(path)
    return get_pdf_content_from_local(path)


if __name__ == "__main__":
    import json
    print(
        is_url_or_file_path(
            "test_pdfs/self_supervised_learning_fair_meta.pdf"))
    # pdf_data = get_pdf_content(
    #     "./test_pdfs/self_supervised_learning_fair_meta.pdf")
    # with open("./self_supervised_learning_fair_meta_content.json", "w") as fp:
    #     json.dump(pdf_data, fp, indent=4)