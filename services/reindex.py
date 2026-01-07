from rag import RAGEngine

# Global singleton
rag_engine = None

def init_rag(dataset_path: str):
    global rag_engine
    rag_engine = RAGEngine(dataset_path)

def reindex(dataset_path: str):
    global rag_engine
    rag_engine = RAGEngine(dataset_path)
    print("✅ RAG reindexed")
