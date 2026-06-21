import os

from pypdf import PdfReader

from rag import add_document

# Absolute path is safer for debugging
DATA_FOLDER = r"C:\Users\Administrator\Desktop\legal-rag-assistant\data"


def chunk_text(text, chunk_size=1000, overlap=200):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks


def ingest_pdf(pdf_path):

    filename = os.path.basename(pdf_path)

    print(f"\nOpening PDF: {filename}")

    try:

        reader = PdfReader(pdf_path)

        print(f"Pages found: {len(reader.pages)}")

        for page_number, page in enumerate(reader.pages):

            print(f"Reading page {page_number + 1}")

            text = page.extract_text()

            if not text:

                print("No text found on this page.")

                continue

            print(f"Characters extracted: {len(text)}")

            chunks = chunk_text(text)

            print(f"Created {len(chunks)} chunks")

            for i, chunk in enumerate(chunks):

                chunk_id = f"{filename}_{page_number}_{i}"

                metadata = {
                    "file": filename,
                    "page": page_number + 1
                }

                add_document(
                    chunk_id,
                    chunk,
                    metadata
                )

                print(f"Added chunk: {chunk_id}")

    except Exception as e:

        print(f"ERROR while processing {filename}")
        print(e)


def ingest_all():

    print("Current working directory:")
    print(os.getcwd())

    print("\nChecking data folder:")
    print(DATA_FOLDER)

    if not os.path.exists(DATA_FOLDER):

        print("DATA FOLDER DOES NOT EXIST")

        return

    files = os.listdir(DATA_FOLDER)

    print("\nFiles found:")
    print(files)

    if len(files) == 0:

        print("NO FILES FOUND")

        return

    for filename in files:

        print(f"\nFound file: {filename}")

        if filename.lower().endswith(".pdf"):

            print(f"Processing: {filename}")

            pdf_path = os.path.join(
                DATA_FOLDER,
                filename
            )

            ingest_pdf(pdf_path)

        else:

            print(f"Skipping non-PDF: {filename}")

    print("\nFinished indexing.")


if __name__ == "__main__":

    ingest_all()