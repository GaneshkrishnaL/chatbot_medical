from flask import Flask, request, render_template
from dotenv import load_dotenv
import os, re

from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from src.prompt import SYSTEM_PROMPT


load_dotenv()

# Load env keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


########################################
# Load Pinecone indexes
########################################

CLINICAL_INDEX = "clinical-index"
PRODUCT_INDEX  = "product-index"

from langchain_community.embeddings import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

clinical_vs = PineconeVectorStore.from_existing_index(
    index_name=CLINICAL_INDEX, embedding=embeddings
)

product_vs = PineconeVectorStore.from_existing_index(
    index_name=PRODUCT_INDEX, embedding=embeddings
)

clinical_retriever = clinical_vs.as_retriever(k=3)
product_retriever  = product_vs.as_retriever(k=3)


########################################
# Dual retrieval logic
########################################

def dual_retrieve(query):
    prod_docs = product_retriever.invoke(query)
    clin_docs = clinical_retriever.invoke(query)
    return prod_docs + clin_docs


########################################
# Create RAG chain
########################################

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{input}")
])

llm = OpenAI(temperature=0.2)
qa_chain = create_stuff_documents_chain(llm, prompt)


########################################
# Flask app
########################################

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    if request.method == "POST":
        query = request.form["query"]

        docs = dual_retrieve(query)
        result = qa_chain.invoke({
            "input": query,
            "context": docs
        })
        answer = result

    return render_template("chat.html", answer=answer)


if __name__ == "__main__":
    app.run(debug=True)
