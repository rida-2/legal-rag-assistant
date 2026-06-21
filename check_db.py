import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    name="legal_cases"
)

docs = collection.get()

print("Total chunks:", len(docs["documents"]))

pages = set()

for meta in docs["metadatas"]:
    pages.add(
        (meta["file"], meta["page"])
    )

print("Total unique pages:", len(pages))

files = set()

for meta in docs["metadatas"]:
    files.add(meta["file"])

print("Total documents:", len(files))

print("\nPages per file:\n")

page_count = {}

for meta in docs["metadatas"]:

    file = meta["file"]

    if file not in page_count:
        page_count[file] = set()

    page_count[file].add(meta["page"])

for file, pages in page_count.items():

    print(
        f"{file}: {len(pages)} pages"
    )