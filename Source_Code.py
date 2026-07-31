#!/usr/bin/env python
# coding: utf-8

# In[23]:


from langchain_community.document_loaders import (
    PyMuPDFLoader,
    TextLoader,
    UnstructuredPowerPointLoader,
    Docx2txtLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from uuid import uuid4
from langchain_classic.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
import tempfile
import os
import streamlit as st



# In[24]:


dir_path = Path("../Untitled Folder/data")
EMBEDDINGMODEL = "Alibaba-NLP/gte-base-en-v1.5"
VECTORSTORE_DIR = Path("resources/vectorstore")
COLLECTION_NAME = "multifile"

load_dotenv()


# In[25]:


llm =None
vector_store = None

def initialise_components():

    global llm, vector_store
    
    # ---------------- LLM ----------------
    if llm is None:

        groq_key = st.secrets["GROQ_API_KEY"]

        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.9,
            max_tokens=500,
            api_key=groq_key
        )
    # ---------------- VECTOR STORE ----------------
    if vector_store is None:
        ef = HuggingFaceEmbeddings(
            model_name="BAAI/bge-base-en-v1.5",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        vector_store = Chroma(
            collection_name="real_estate",
            embedding_function=ef,
            persist_directory=str(VECTORSTORE_DIR),
        )

# In[26]:


def process_all_pdfs(uploaded_files):

    yield "Initialisings compoments (LLM & Vector Store)"

    initialise_components()

    vector_store.reset_collection()

    yield "Loading all the documents"
    # Loading all the documents
    all_documents = []

    for file in uploaded_files:
        yield f"📄 Processing {file.name}..."

        # Get file extension
        suffix = Path(file.name).suffix.lower()

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(file.getvalue())
            temp_path = tmp_file.name

        # Load according to file type
        if suffix == ".pdf":
            docs = PyMuPDFLoader(temp_path).load()

        elif suffix == ".txt":
            docs = TextLoader(temp_path, encoding="utf-8").load()

        elif suffix == ".docx":
            docs = Docx2txtLoader(temp_path).load()

        elif suffix == ".pptx":
            docs = UnstructuredPowerPointLoader(temp_path).load()

        else:
            docs = []

        for doc in docs:
            doc.metadata["source"] = file.name

        all_documents.extend(docs)

        # Remove temporary file
        os.remove(temp_path)


    yield f"Total documents loaded: {len(all_documents)}"


    yield "Splitting the text into chunks"
    #Splitting the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        separators = ["\n\n","\n","."," ",""],
        chunk_size = 700,
        chunk_overlap = 100

    )

    chunks = text_splitter.split_documents(all_documents)
    print(f'Total number of chunks received from {len(all_documents)} : {len(chunks)}')

    yield "Adding Chunks to Vector Database"
    uuids = [str(uuid4()) for _ in range(len(chunks))]
    vector_store.add_documents(chunks, ids = uuids)

    print(f"Successfully added {len(chunks)} chunks!")

    yield "✅ Vector Database initialized successfully"


# In[27]:

def generate_answer(query):
    global vector_store, llm

    # Make sure components exist
    initialise_components()

    if vector_store is None:
        raise RuntimeError("Please process documents first.")

    chain = RetrievalQAWithSourcesChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(search_kwargs={"k": 4})
    )

    result = chain.invoke({"question": query})

    answer = result.get("answer", "No answer generated.")
    sources = result.get("sources", "")

    # Keep answer short (2-3 lines)
    answer = " ".join(answer.split())

    return answer, sources

# In[ ]:


if __name__ == "__main__":

    process_all_pdfs(r"D:\complete01\rag Based Chatbot\data")

    answer, sources = generate_answer(" What happens if required materials are missing at the application deadline?")

    print(f'Answer: {answer}')
    print(f'Sources: {sources}')



