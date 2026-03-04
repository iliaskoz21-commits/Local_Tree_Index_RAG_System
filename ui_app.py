import streamlit as st
import os
import pymupdf
from dotenv import load_dotenv
from groq import Groq
import page_index

load_dotenv()

st.set_page_config(page_title="AI Engineer Local RAG", layout="wide")
st.title("📄 Local Tree-Index RAG System (Verified)")

MODEL = "llama-3.3-70b-versatile"

@st.cache_resource
def get_groq():
    """Caches the Groq client connection."""
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

client = get_groq()

uploaded_file = st.sidebar.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    if "tree" not in st.session_state:
        with st.status("🛠️ Building & Verifying Local Tree..."):
            # Local PDF Parsing via PyMuPDF
            doc = pymupdf.open(stream=uploaded_file.read(), filetype="pdf")
            pages = [[p.get_text(), p.number + 1] for p in doc]
            
            # Create and Verify Tree structure
            tree = page_index.process_no_toc(pages, model=MODEL)
            
            st.session_state.tree = tree
            st.session_state.pages = pages
            st.success("Verified Tree Ready!")

if "tree" in st.session_state:
    st.sidebar.subheader("Document Structure")
    for item in st.session_state.tree:
        # VERIFICATION ICON
        icon = "✅" if item.get('verified') else "⚠️"
        
        # FIX: Handle float strings like '1.1' by converting to float first, then int
        try:
            struct_level = int(float(item.get('structure', 1)))
        except (ValueError, TypeError):
            struct_level = 1
            
        # Calculate indentation based on hierarchy level
        level_space = "　" * (struct_level - 1) 
        st.sidebar.write(f"{level_space}{icon} {item['title']} (P.{item['physical_index']})")
    
    if prompt := st.chat_input("Ask a question about the document..."):
        st.chat_message("user").write(prompt)
        
        # SMART RETRIEVAL: Find relevant page based on tree titles
        selected_page = 1
        for item in st.session_state.tree:
            if item['title'].lower() in prompt.lower():
                selected_page = item['physical_index']
                break
        
        # Extract context from selected page
        context = st.session_state.pages[selected_page - 1][0]
        
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "You are an AI Engineer Assistant. Answer in Greek based on the context."},
                    {"role": "user", "content": f"Context: {context}\n\nQuestion: {prompt}"}
                ]
            )
            st.write(response.choices[0].message.content)