import os
import pandas as pd
from dotenv import load_dotenv

from langchain_core.documents import Document

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

print("Loading environment variables...")
load_dotenv()

pinecone_api_key = "pcsk_6QT4hh_7uY2wY8DdDkJdZuyib2W7e9xiN8n7CRaDbQUDKk76uMe8xFMyHiLFaqvcUbYwna"
if not pinecone_api_key:
    raise ValueError("PINECONE_API_KEY not found. Please set it in your .env file.")

CSV_FILE_PATH = "books.csv"
PINECONE_INDEX_NAME = "langchain-books-pure-v1"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

print(f"Loading first 100 rows from '{CSV_FILE_PATH}' using pandas...")
try:
    df = pd.read_csv(
        CSV_FILE_PATH,
        nrows=100,
        on_bad_lines='skip'
    ).fillna('')

    print(f"Loaded {len(df)} rows. Now creating LangChain Document objects...")

    documents = []
    for index, row in df.iterrows():
        page_content = f"Title: {row['title']}; Authors: {row['authors']}"
        
        metadata = row.to_dict()
        
        doc = Document(page_content=page_content, metadata=metadata)
        documents.append(doc)

except FileNotFoundError:
    print(f"Error: The file '{CSV_FILE_PATH}' was not found.")
    exit()

print(f"Successfully created {len(documents)} Document objects.")

print(f"Initializing embedding model: '{EMBEDDING_MODEL}'...")
embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

EMBEDDING_DIMENSION = 384
print(f"Embedding model loaded. Vector dimension: {EMBEDDING_DIMENSION}")

print("Initializing Pinecone client...")
pc = Pinecone(api_key=pinecone_api_key)

if PINECONE_INDEX_NAME not in pc.list_indexes().names():
    print(f"Index '{PINECONE_INDEX_NAME}' not found. Creating a new one...")
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=EMBEDDING_DIMENSION,
        metric='cosine',
        spec={'serverless': {'cloud': 'aws', 'region': 'us-east-1'}}
    )
    print("Index created successfully.")
else:
    print(f"Index '{PINECONE_INDEX_NAME}' already exists. Connecting to it.")

print("Embedding documents and uploading to Pinecone...")
vectorstore = PineconeVectorStore.from_documents(
    documents=documents,
    index_name=PINECONE_INDEX_NAME,
    embedding=embeddings
)

print("\n✅ Success! Your data has been embedded and stored in Pinecone.")
print(f"Total documents added: {len(documents)}")
print(f"Pinecone Index: '{PINECONE_INDEX_NAME}'")

print("\n--- Running a verification similarity search ---")
query = "A book about a young wizard in a magic school"
results = vectorstore.similarity_search(query, k=3)

print(f"Query: '{query}'")
print("Top 3 similar books found:")
for result in results:
    title = result.metadata.get('title', 'N/A')
    authors = result.metadata.get('authors', 'N/A')
    rating = result.metadata.get('average_rating', 'N/A')
    print(f"  - Title: {title}, Authors: {authors}, Rating: {rating}")