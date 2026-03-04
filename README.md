# 🚀 Local Tree-Index RAG System (Powered by PageIndex)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B.svg)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Inference-Groq_Llama_3-orange.svg)](https://groq.com/)

An advanced, reasoning-based RAG system designed for high-accuracy document analysis. By implementing a hierarchical tree-indexing strategy, this system overcomes the limitations of traditional vector-based RAG, ensuring precise context retrieval even in dense or complex documents.

---

## 👨‍💻 For Recruiters: Why this Project?
This repository demonstrates professional-grade AI Engineering skills including:
- **Reasoning-based RAG**: Moving beyond simple vector similarity to structured document understanding.
- **Agentic Verification**: Implementing a self-correcting logic (`verify_toc`) that validates AI outputs against ground-truth data.
- **Optimized Inference**: Leveraging Groq LPUs for near-instant indexing and response generation.
- **Clean Architecture**: Modular code structure (Utils, Logic, UI) designed for scalability and maintainability.

---

## 🛠️ Key Features
- **Hierarchical Indexing**: Automatically generates a structured "Tree Map" of PDF documents.
- **Physical Index Tagging**: Uses unique page-anchoring tags to prevent "Lost in the Middle" context issues.
- **Automated Verification**: A secondary validation layer confirms if the AI-identified sections exist on the actual physical pages.
- **Localized RAG**: Optimized for privacy and speed, requiring only a Groq API key.



---

## 📖 Acknowledgments & Originality
This project is an implementation based on the groundbreaking work of the **PageIndex Team**. It adapts the "Vectorless, Reasoning-based RAG" philosophy to a practical, local-first application using Python and Streamlit.


Pageindex is a Project created by Mingtian Zhang, Yu Tang and PageIndex Team,  
"PageIndex: Next-Generation Vectorless, Reasoning-based RAG",  
PageIndex Blog, Sep 2025.

If you find this project useful, please cite the original PageIndex research:
```bibtex
@article{zhang2025pageindex,
  title={PageIndex: Next-Generation Vectorless, Reasoning-based RAG},
  author={Zhang, Mingtian and Tang, Yu and {PageIndex Team}},
  journal={PageIndex Blog},
  year={2025},
  month={September},
  url={[https://github.com/pageindex/pageindex](https://github.com/pageindex/pageindex)}
}
}
🚀 Getting Started
Clone & Setup:

Bash
git clone [https://github.com/YOUR_USERNAME/local-pageindex-rag.git](https://github.com/YOUR_USERNAME/local-pageindex-rag.git)
cd local-pageindex-rag
pip install -r requirements.txt
Environment Variables:
Create a .env file and add your key:


GROQ_API_KEY=your_key_here

Run Application:

Bash
streamlit run ui_app.py
