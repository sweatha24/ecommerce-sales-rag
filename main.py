import os
from dotenv import load_dotenv
from config.database import DatabaseManager
from src.analytics import SalesAnalytics
from src.rag_engine import SalesRAGEngine

def main():
    load_dotenv()

    print("==================================================")
    print(" 🛒 E-Commerce Sales Analytics & RAG Engine")
    print("==================================================")
    
    # Connect and summarize
    db_mgr = DatabaseManager()
    db = db_mgr.connect()
    analytics = SalesAnalytics(db)
    summaries = analytics.generate_store_summary_text()
    
    print("\n[+] Initializing RAG Vector Engine...")
    rag = SalesRAGEngine(summaries)
    print("[+] Engine ready!\n")

    # Interactive Loop
    while True:
        try:
            user_query = input("Ask a question about store sales (or type 'exit' to quit): ").strip()
            if not user_query:
                continue
            if user_query.lower() in ["exit", "quit", "q"]:
                print("Exiting RAG Engine. Goodbye!")
                break

            answer = rag.query(user_query)
            print(f"\n💡 AI Answer:\n{answer}\n")
            print("-" * 50)
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()