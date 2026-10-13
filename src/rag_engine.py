import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document

class SalesRAGEngine:
    def __init__(self, summaries):
        """Initializes local embeddings and Gemini LLM."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            raise ValueError("Invalid GOOGLE_API_KEY in .env file.")

        # Local HuggingFace embedding (Free)
        print("Loading local embedding model...")
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        # Convert summaries to LangChain Document objects
        docs = [
            Document(page_content=item["summary"], metadata={"store_id": item["store_id"]})
            for item in summaries
        ]

        # FAISS Vector Index
        self.vector_store = FAISS.from_documents(docs, self.embeddings)

        # Gemini LLM (Free Tier)
        self.llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash", google_api_key=api_key)

    def query(self, question: str) -> str:
        """Retrieves relevant context and queries Gemini."""
        relevant_docs = self.vector_store.similarity_search(question, k=2)
        context = "\n".join([doc.page_content for doc in relevant_docs])

        prompt = f"""
You are an expert E-Commerce Sales Analyst assistant.
Answer the following user question using ONLY the provided database KPI context below.

Context:
{context}

Question: {question}

Answer:"""

        response = self.llm.invoke(prompt)
        response = self.llm.invoke(prompt)
        
        # If response.content is a list of blocks/dicts, extract the text field
        if isinstance(response.content, list):
            return "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in response.content])
        
        return response.content
    