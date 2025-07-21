import os, shutil, chromadb
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from config import Config
# from langchain_pinecone import PineconeVectorStore
# from pinecone import Pinecone, ServerlessSpec
# from langchain_openai import OpenAIEmbeddings

class VectorStore:
    def __init__(self, path, index_name, namespace=None):
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


## For Pinecone
# class VectorStore:
#     def __init__(self, index_name, namespace=None):
#         self.index_name = Config.index_name
#         self.namespace = namespace

#         # self.embeddings = OpenAIEmbeddings(
#         #     model="text-embedding-3-small",
#         #     openai_api_key=Config.OPENAI_API_KEY
#         # )
#         self.embeddings = HuggingFaceEmbeddings()

#         self.pc = Pinecone(api_key=Config.PINECONE_API_KEY)
        
#         self.vector_store = PineconeVectorStore(
#             index=self.index_name,
#             embedding=self.embeddings,
#             namespace=self.namespace
#         )
    
#     def create_index_if_not_exists(self):
#         """Create Pinecone index if it does not exists"""
#         existing_indexes = [index.name for index in self.pc.list_indexes()]

#         if self.index_name not in existing_indexes:
#             self.pc.create_index(
#                 name = self.index_name,
#                 dimension=1536,
#                 metric='cosine',
#                 spec=ServerlessSpec(
#                     cloud='aws',
#                     region='us-east-1'
#                 )
                
#             )
    
#     def add_documents(self, documents):
#         """Add documents to Pinecone index"""
#         self.vector_store.add_documents(documents, namespace=self.namespace)

#     def similarity_search(self, query, k=4, filter=None):
#         """Search for similar documents"""
#         return self.vector_store.similarity_search(
#             query, 
#             k=k, 
#             filter=filter,
#             namespace=self.namespace
#         )

#     def clear(self, ids=None, delete_all=False, filter=None):
#         """Delete documents from Pinecone index"""
#         self.vector_store.delete(
#             ids=ids,
#             delete_all=delete_all,
#             namespace=self.namespace
#         )