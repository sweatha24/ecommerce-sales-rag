# 🛒 E-Commerce Sales Analytics & RAG Engine

An end-to-end Retrieval-Augmented Generation (RAG) system that processes sales transaction data from MongoDB Atlas, performs store KPI aggregations, and uses Google Gemini with FAISS vector retrieval to answer natural language sales queries.

## 🏗️ Architecture & Tech Stack

- **Database**: MongoDB Atlas (PyMongo)
- **Vector Search**: FAISS (Facebook AI Similarity Search)
- **Embeddings**: Local HuggingFace (`all-MiniLM-L6-v2`)
- **LLM**: Google Gemini API (`gemini-3.8-flash`)
- **Orchestration**: LangChain

## 🚀 Setup & Execution

1. **Clone the repository and install dependencies**:
   ```bash
