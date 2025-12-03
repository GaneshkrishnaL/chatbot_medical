import re
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


###############################
# Load PDF files
###############################

def load_pdf(path: str):
    """
    Loads a PDF file and returns LangChain Document objects.
    """
    loader = PyPDFLoader(path)
    return loader.load()


###############################
# Split clinical data
###############################

def split_clinical_docs(documents):
    """
    Breaks clinical knowledge PDFs (like Gale) into chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=50
    )
    return splitter.split_documents(documents)


###############################
# Split product catalog 
# with structured metadata
###############################

def split_product_catalog(documents):
    """
    Extract structured lines from product catalog PDF such as:
    Item #, NDC, HCPCS, Manufacturer, Product name.
    """

    product_chunks = []

    for doc in documents:
        lines = doc.page_content.split("\n")

        for line in lines:
            # Look for NDC like "50242-0136-01"
            ndc = re.findall(r"\d{5}-\d{4}-\d{2}", line)
            hcpcs = re.findall(r"[A-Z]\d{4}", line)

            # Only keep useful lines
            if ndc or hcpcs:
                metadata = {
                    "page": doc.metadata.get("page"),
                    "source": "product_catalog",
                    "ndc": ndc[0] if ndc else "UNKNOWN",
                    "hcpcs": hcpcs[0] if hcpcs else "UNKNOWN"
                }

                product_chunks.append(
                    Document(page_content=line.strip(), metadata=metadata)
                )

    return product_chunks
