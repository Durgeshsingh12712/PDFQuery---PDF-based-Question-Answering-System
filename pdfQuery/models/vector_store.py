import os, shutil, chromadb
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_openai import OpenAIEmbeddings

class VectorStore:
    def __init__(self, path):
        self.path = path
        # self.embeddings = OpenAIEmbeddings(
        #     model="text-embedding-3-small",
        #     openai_api_key=Config.OPENAI_API_KEY
        # )
        self.embeddings = HuggingFaceEmbeddings()
        self.vector_store = Chroma(
            persist_directory=path,
            embedding_function=self.embeddings,
        )
    
    def add_documents(self, documents):
        self.vector_store.add_documents(documents)
        self.vector_store.persist()
    
    def similarity_search(self, query, k=4):
        """Search for similar documents"""
        return self.vector_store.similarity_search(query, k=k)
    
    def clear(self):
        """Clear all documents from the vector store"""
        try:
            if os.path.exists(self.path):
                shutil.rmtree(self.path)
            
            self.vector_store = Chroma(
                persist_directory=self.path,
                embedding_function=self.embeddings
            )
        except Exception as e:
            print(f"Error clearing vector store: {str(e)}")
    
    def get_collection_info(self):
        """Get information about current collection"""
        try:
            collection = self.vector_store._collection
            return {
                'count': collection.count(),
                'name': collection.name
            }
        except Exception as e:
            print(f"Error getting collection info: {str(e)}")
            return {'count': 0, 'name': 'unknown'}