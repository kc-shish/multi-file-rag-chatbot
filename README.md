# 📚 Multi-file RAG Chatbot

A **Streamlit-based Retrieval-Augmented Generation (RAG) chatbot** that enables users to upload **PDF, TXT, DOCX, and PPTX documents**, process them into a **Chroma vector database**, and ask natural-language questions powered by **Groq Llama 3.3 70B**.

---

## 🚀 Features

* 📄 Upload and process **multiple documents**

* 🧠 Generate embeddings with **HuggingFace Embeddings**

* 💾 Store and retrieve vectors using **ChromaDB**

* 🤖 Ask questions about uploaded documents

* 💬 Maintain **chat history** with `st.session_state.messages`

* 📄 Display **source document citations**

* ⚡ Fast inference using **Groq Llama 3.3 70B**

---

## 🛠️ Tech Stack

| Component        | Technology                      |
| ---------------- | ------------------------------- |
| Frontend         | Streamlit                       |
| Framework        | LangChain                       |
| Vector Store     | ChromaDB                        |
| LLM              | Groq                            |
| Embeddings       | HuggingFace                     |
| Document Parsing | PyMuPDF, Docx2txt, Unstructured |

---

## 📂 Project Structure

```
multi-file-rag-chatbot/
├── main_UI.py              # Streamlit user interface
├── Source_Code.py          # RAG pipeline and document processing
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (local only)
├── data/                   # Optional sample documents
└── resources/
    └── vectorstore/        # Persistent Chroma vector database
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get your API key from: [https://console.groq.com/keys](https://console.groq.com/keys)

> ⚠️ **Important:** Never commit `.env` to GitHub.

---

## 📦 Installation

### 1. Clone the repository

```
git clone https://github.com/kc-shish/multi-file-rag-chatbot.git
cd multi-file-rag-chatbot
```

### 2. Create a virtual environment

**Windows**

```
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```
streamlit run main_UI.py
```

The app will be available at:

```
http://localhost:8501
```

---

## 📖 Usage

1. Launch the Streamlit app.

2. Upload one or more documents.

3. Click **⚙️ Process Files**.

4. Wait for the vector database to be created.

5. Ask questions in the chat interface.

6. View answers along with **source document references**.

---

## 📄 Supported File Types

<table><tbody><tr><td><span>Type</span></td><td><span>Supported</span></td></tr><tr><td><span>PDF</span></td><td><span>✅</span></td></tr><tr><td><span>TXT</span></td><td><span>✅</span></td></tr><tr><td><span>DOCX</span></td><td><span>✅</span></td></tr><tr><td><span>PPTX</span></td><td><span>✅</span></td></tr></tbody></table>

---

## 💬 Chat Memory System

The chatbot preserves conversation history during the active Streamlit session using `**st.session_state.messages**`.

### Example

```
if "messages" not in st.session_state:
    st.session_state.messages = []

st.session_state.messages.append({
    "role": "user",
    "content": query
})

st.session_state.messages.append({
    "role": "assistant",
    "content": full_response
})
```

### Clear History

```
with st.sidebar:
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
```

### Benefits

* ✅ ChatGPT-style conversation flow

* ✅ Preserves previous questions and answers

* ✅ Maintains context visibility during the session

* ✅ Automatically survives Streamlit reruns

> ℹ️ The history is **session-based** and is cleared when the browser session or Streamlit server is restarted.

---

## ⚙️ Example Questions

* *What additional materials may be required for some scholarships?*

* *How do named scholarships affect need-based grants?*

* *Who selects scholarship recipients?*

* *What is required to renew a named scholarship?*

---

## 📋 Requirements

```
streamlit
langchain-community
langchain-text-splitters
langchain-chroma
langchain-groq
langchain-huggingface
chromadb
python-dotenv
pymupdf
docx2txt
unstructured[pptx]
```

---

## 🌟 Future Improvements

* 🔐 User authentication

* 🧠 Persistent chat memory

* 📂 Drag-and-drop document management

* 🔍 Hybrid search (BM25 + vector search)

* ☁️ Deployment on **Streamlit Community Cloud** or **HuggingFace Spaces**

---

## 👨‍💻 Author

**Aashish Kumar Chetan**

🔗 GitHub: [https://github.com/kc-shish](https://github.com/kc-shish)

---

## 📜 License

This project is licensed under the **Apache License 2.0**.

See the LICENSE file for details.
