
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyDXnO8N7EUyQz5QT-7qa-3BsBNkGH6rxlk"



from typing import List

# Loaders
from langchain_community.document_loaders import PyPDFLoader, TextLoader

# Splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Gemini Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# FAISS DB
from langchain_community.vectorstores import FAISS

# Gemini LLM
from langchain_google_genai import ChatGoogleGenerativeAI

# LCEL RAG components
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document


# ---------------------------
# CONFIG
# ---------------------------
PERSIST_DIR = "./faiss_index"
EMBED_MODEL = "models/text-embedding-004"
LLM_MODEL = "models/gemini-2.5-flash"



# ---------------------------
# LOAD DOCS
# ---------------------------
def load_documents(paths: List[str]) -> List[Document]:
    docs=[]
    for p in paths:
        if p.lower().endswith(".pdf"):
            docs.extend(PyPDFLoader(p).load())
        else:
            docs.extend(TextLoader(p, encoding="utf-8").load())
    return docs


# ---------------------------
# SPLIT DOCS
# ---------------------------
def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=240
    )
    return splitter.split_documents(docs)


# ---------------------------
# BUILD / LOAD FAISS DB
# ---------------------------
def build_faiss_index(docs):
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBED_MODEL)
    vectordb = FAISS.from_documents(docs, embeddings)
    vectordb.save_local(PERSIST_DIR)
    return vectordb


def load_faiss_index():
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBED_MODEL)
    return FAISS.load_local(
        PERSIST_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )


# ---------------------------
# BUILD RAG CHAIN (LCEL)
# ---------------------------
def build_rag_chain(retriever):

    system_prompt = (
        "Use ONLY the provided context to answer the question.\n"
        "If the answer is not present, say 'I don't know'.\n"
        "Keep the answer under three sentences.\n\nContext:\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        temperature=0
    )

    doc_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, doc_chain)

    return rag_chain


# ---------------------------
# MAIN EXECUTION
# ---------------------------
if __name__ == "__main__":

    sop_files = [
        "./data/SOP_1.pdf",
        "./data/SOP_2.pdf",
        "./data/SOP_3.pdf",
        
    ]

    print("Loading documents...")
    docs_raw = load_documents(sop_files)

    print("Splitting...")
    docs_split = split_documents(docs_raw)

    print("Building FAISS index...")
    vectordb = build_faiss_index(docs_split)

    print("Loading FAISS index...")
    vectordb = load_faiss_index()

    retriever = vectordb.as_retriever(search_kwargs={"k": 4})

    print("Building RAG chain...")
    rag_chain = build_rag_chain(retriever)

    print("Gemini RAG Assistant Ready!")

    while True:
        q = input("\nAsk a question (or type exit): ")
        if q.lower()=="exit":
            break

        result = rag_chain.invoke({"input": q})

        print("\nANSWER:")
        print(result["answer"])

        # print("\nCONTEXT USED:")
        # for i, doc in enumerate(result["context"]):
        #     print(f"\n[{i}] {doc.page_content[:250]}...")



