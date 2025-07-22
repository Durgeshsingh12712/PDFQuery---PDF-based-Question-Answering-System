# from langchain_groq import ChatGroq
from langchain_openai import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from config import Config
from pdfQuery.logging import logger

class LLMService:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.llm = OpenAI(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=1000,
            api_key=Config.OPENAI_API_KEY
        )

        # self.llm = ChatGroq(
        #     model_name = "llama3-8b-8192",
        #     temperature=0.7,
        #     groq_api_key=Config.GROQ_API_KEY,
        # )

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )

        self.prompt = PromptTemplate(
            template="""You are a helpful assistant that answers questions based on the provided document context. 
            Use the following pieces of context to answer the question at the end. 
            If you don't know the answer based on the context, just say that you don't know. 
            Don't try to make up an answer.

            Context:
            {context}

            Question: {question}

            Please provide a clear, concise answer based on the context above:""",
            input_variables=["context", "question"]
        )
        
        self.chain = ConversationalRetrievalChain.from_llm(
            llm = self.llm,
            retriever = self.vector_store.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            ),
            memory=self.memory,
            return_source_documents=True
        )
    
    def get_response(self, query):
        """Get Response from the LLM for a given Query"""
        try:
            logger.debug(f"Processing query: {query}")

            response = self.chain({"question": query})

            answer = response.get("answer", "I could not Generate an answer.")

            if 'source_documents' in response:
                logger.debug(f"Retrieved {len(response['source_documents'])} source documents.")
                for i, doc in enumerate(response['source_documents']):
                    logger.debug(f"Source Document {i+1}: {doc.metadata.get('source', 'Unknown Source')}")
            
            return answer
        except Exception as e:
            logger.error(f"Error getting LLM response: {str(e)}")
            return "I encountered an error while processing your request. Please try again later."
    
    def clear_memory(self):
        """Clear the conversation memory"""
        self.memory.clear()
        logger.debug("Conversation memory cleared.")
    
    def get_conversation_history(self):
        """Get the conversation history"""
        return self.memory.chat_memory.messages