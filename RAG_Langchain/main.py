# rag_project.py

# Import necessary components from LangChain and other libraries
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA


# --- Step 1: Prepare your Documents ---
# A small set of documents containing information about Python.
documents = [
    "Python is a popular programming language known for its readability and simplicity.",
    "Python has many libraries for data analysis, web development, machine learning, and more.",
    "Python supports multiple programming paradigms including procedural, object-oriented, and functional programming."
]

# --- Step 2: Embed the Documents ---
# Use a Hugging Face embedding model to convert documents to embeddings.
# Here we use 'all-MiniLM-L6-v2' from Sentence Transformers.
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create a FAISS vector store from the documents using the embeddings.
vectorstore = FAISS.from_texts(documents, embeddings) 
eknjoewqnijofcnioejwcn= 1

# --- Step 3: Set Up the Retriever ---
# Convert the vector store into a retriever, which can fetch relevant documents based on a query.
retriever = vectorstore.as_retriever()

# --- Step 4: Set Up the Hugging Face LLM ---
import transformers

# Create a Transformers pipeline for text generation using an open source model.
# Here, 'distilgpt2' is used for demonstration purposes.
generation_pipeline = transformers.pipeline(
    "text-generation",
    model="distilgpt2",
    tokenizer="distilgpt2",
    max_new_tokens=100  # Limit the response length for this demo.
)

# Wrap the pipeline in LangChain's HuggingFacePipeline to integrate with the chain.
llm = HuggingFacePipeline(pipeline=generation_pipeline)

# --- Step 5: Create the RetrievalQA Chain ---
# Combine the retriever and the LLM in a RetrievalQA chain.
# The "stuff" chain type is a simple method where all retrieved documents are stuffed into the prompt.
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")

# --- Step 6: Run a Query through the RAG System ---
# Define a query that asks about Python's features.
query = "What are the main features of Python?"

# Execute the chain: It retrieves relevant documents and then generates an answer using the LLM.
response = qa_chain.run(query)

# Print the generated response.
print("Response:", response)
