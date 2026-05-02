import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

EMBEDDINGS = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def process_pdf(pdf_path: str) -> FAISS:
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(pages)

    vectorstore = FAISS.from_documents(chunks, EMBEDDINGS)
    return vectorstore


def query_pdf(vectorstore: FAISS, question: str) -> str:
    if vectorstore is None:
        return "No PDF uploaded yet."

    docs = vectorstore.similarity_search(question, k=3)

    if not docs:
        return "No relevant content found in the PDF."

    result = []
    for i, doc in enumerate(docs, 1):
        result.append(f"[Chunk {i}]:\n{doc.page_content}")

    return "\n\n".join(result)