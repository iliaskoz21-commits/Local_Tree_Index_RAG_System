import os
import fitz  # PyMuPDF
import asyncio
from dotenv import load_dotenv
from pageindex import PageIndexClient
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
# 1. Setup PageIndex to use LOCAL Ollama for Indexing
# Ollama's local API (v1) is OpenAI-compatible.
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_API_KEY"] = "ollama"  # Required placeholder for local usage

# Initialize Clients
pi_client = PageIndexClient(api_key=os.getenv("PAGEINDEX_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_text_from_pdf(file_path):
    """Extracts all text from a local PDF file using PyMuPDF."""
    print(f"[*] Reading PDF: {file_path}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found.")
        
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

async def run_rag_pipeline():
    # 1. Define your source document
    # Make sure you have a PDF named 'document.pdf' in your folder!
    pdf_filename = "document.pdf" 
    
    try:
        content = extract_text_from_pdf(pdf_filename)
        
        # 2. Local Indexing Phase
        print("[*] Starting Local Indexing via Ollama (Mistral)...")
        # PageIndex chunks the text and calls your local Mistral model
        index = pi_client.index(text=content, model="mistral")
        
        # 3. User Query
        user_query = "Summarize the main points of this document."
        print(f"[*] Querying: {user_query}")
        
        # 4. Retrieval Phase (Finding relevant snippets)
        results = index.search(user_query, top_k=3)
        context_snippets = "\n".join([r.text for r in results])

        # 5. Generation Phase (Reasoning via Groq)
        print("[*] Generating final answer via Groq (Llama 3.3 70B)...")
        
        response = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful assistant. Use the provided context to answer the user's question accurately."
                },
                {
                    "role": "user", 
                    "content": f"Context:\n{context_snippets}\n\nQuestion: {user_query}"
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.2 # Lower temperature for more factual RAG responses
        )

        # 6. Output the Result
        print("\n" + "="*20 + " ANSWER " + "="*