from dotenv import load_dotenv
import os
from src.helper import load_pdf_file, filter_to_minimal_docs, text_split

# pyrefly: ignore [missing-import]
from pinecone import Pinecone, ServerlessSpec
# pyrefly: ignore [missing-import]
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings

load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not PINECONE_API_KEY or not OPENAI_API_KEY:
    raise ValueError("Missing API keys! Set PINECONE_API_KEY and OPENAI_API_KEY in environment variables.")

# Load and process PDF documents
extracted_data = load_pdf_file(data="data/")
filter_data = filter_to_minimal_docs(extracted_data)
text_chunks = text_split(filter_data)

# Load OpenAI embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1024)

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medicalchatbot"  # new index, matches OpenAI embedding dims

existing_indexes = [
    index["name"]
    for index in pc.list_indexes()
]

if index_name not in existing_indexes:

    pc.create_index(
    name=index_name,
    dimension=1024,   # ← changed from 1536
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
