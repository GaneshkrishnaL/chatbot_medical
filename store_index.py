import os
import logging
from dotenv import load_dotenv
from pinecone.grpc import PineconeGRPC as Pinecone

from pinecone import ServerlessSpec

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore


from src.helper import load_pdf, split_clinical_docs, split_product_catalog

logging.basicConfig(level=logging.INFO)


#############################################
# Load env variables
#############################################
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=PINECONE_API_KEY)


#############################################
# Index names
#############################################
CLINICAL_INDEX = "clinical-index"
PRODUCT_INDEX = "product-index"


#############################################
# Step 1: Load PDF data
#############################################

logging.info("📥 Loading PDFs...")

clinical_docs = load_pdf("Data/Medical_book.pdf")
product_docs  = load_pdf("Data/Product_catalog.pdf")


#############################################
# Step 2: Create chunks
#############################################

logging.info("🔪 Chunking clinical data...")
clinical_chunks = split_clinical_docs(clinical_docs)

logging.info("🔪 Extracting product metadata lines...")
product_chunks = split_product_catalog(product_docs)


#############################################
# Step 3: Embeddings
#############################################

logging.info("🧠 Loading embeddings...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


#############################################
# Step 4: Create Pinecone indexes
#############################################

def create_index(name):
    if name not in pc.list_indexes().names():
        pc.create_index(
            name=name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        logging.info(f"📦 Created index: {name}")

create_index(CLINICAL_INDEX)
create_index(PRODUCT_INDEX)


#############################################
# Step 5: Upsert data
#############################################

logging.info("⬆️ Uploading clinical data...")
PineconeVectorStore.from_documents(
    documents=clinical_chunks,
    index_name=CLINICAL_INDEX,
    embedding=embeddings
)

logging.info("⬆️ Uploading product data...")
PineconeVectorStore.from_documents(
    documents=product_chunks,
    index_name=PRODUCT_INDEX,
    embedding=embeddings
)

logging.info("✅ Indexing complete.")
