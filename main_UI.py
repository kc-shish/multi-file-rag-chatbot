
import streamlit as st
from Source_Code import process_all_pdfs, generate_answer

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Multi-file RAG Chatbot",
    page_icon="📚",
    layout="wide"
)

# -------------------------------------------------
# TITLE
# -------------------------------------------------
st.title("📚 Multi-file Ingestion Chatbot via RAG")

# -------------------------------------------------
# SESSION STATE FOR CHAT HISTORY
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
with st.sidebar:

    st.markdown("## 📤 Upload Documents")

    uploaded_files = st.file_uploader(
        "Choose files",
        type=["pdf", "txt", "docx", "pptx"],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.success(f"{len(uploaded_files)} file(s) selected")

    st.divider()

    st.markdown("## 📁 Uploaded Files")

    if uploaded_files:
        for f in uploaded_files:
            st.write(f"📄 {f.name}")

        if st.button(
            "⚙️ Process Files →",
            use_container_width=True
        ):
            status_placeholder = st.sidebar.empty()

            for status in process_all_pdfs(uploaded_files):
                status_placeholder.info(status)

            status_placeholder.success(
                "Files processed successfully!"
            )
    else:
        st.write("No files uploaded")

    st.divider()

    if st.button(
        "🗑️ Clear Chat History",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

# -------------------------------------------------
# CHAT AREA
# -------------------------------------------------
st.markdown("## 💬 Chat with Your Documents")

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# -------------------------------------------------
# CHAT INPUT
# -------------------------------------------------
query = st.chat_input(
    "Ask a question about your uploaded documents..."
)

if query:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(query)

    # Generate assistant response
    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        try:
            answer, sources = generate_answer(query)

            full_response = answer

            if sources:
                full_response += (
                    f"\n\n📄 **Sources:** {sources}"
                )

            response_placeholder.markdown(full_response)

            # Save assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response
            })

        except RuntimeError as e:
            response_placeholder.warning(str(e))
