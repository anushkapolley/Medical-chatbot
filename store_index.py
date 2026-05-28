from dotenv import load_dotenv
import os
from src.helper import load_pdf_file, filter_to_minimal_docs, text_split, download_embeddings

from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")


# Load and process PDF documents
extracted_data = load_pdf_file(data="data/")
filter_data = filter_to_minimal_docs(extracted_data)
text_chunks = text_split(filter_data)

# Load HuggingFace embeddings
embeddings = download_embeddings()

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medical-chatbot"

existing_indexes = [
    index["name"]
    for index in pc.list_indexes()
]

if index_name not in existing_indexes:

    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ),
    )

# Store embeddings in Pinecone
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name,
    embedding=embeddings,
)

print("Pinecone index created and documents uploaded successfully!")