import os, sys, tempfile, uuid
from datetime import datetime

from flask import (
    Flask,
    request,
    render_template,
    jsonify, session
)

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from config import Config
from pdfQuery.logging import logger
from pdfQuery.exceptions.exception import PDFQueryException
from pdfQuery.models import VectorStore
from pdfQuery.services import LLMService


app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

vector_store = VectorStore(Config.VECTOR_DB_PATH)
llm_service = LLMService(vector_store)

@app.route('/')
def index():
    """Render the main page"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        session['qa_history'] = []
    return render_template('index.html')

def process_document(file):
    """Process Document based on file type and return text chunks"""
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, file.filename)

    try:
        # Save File Temporarily
        file.save(temp_path)
        logger.debug(f"File saved Temporarily at: {temp_path}")

        # Progress based on file type
        if file.filename.lower().endswith('.pdf'):
            loader = PyPDFLoader(temp_path)
            documents = loader.load()

        elif file.filename.lower().endswith('.txt'):
            loader = TextLoader(temp_path, encoding='utf-8')
            documents = loader.load()
        else:
            raise ValueError("Unsupported file type. Only PDF and TXT files are supported.")
        
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        text_chunks = text_splitter.split_documents(documents)

        # Add MetaData to Chunks
        for i, chunk in enumerate(text_chunks):
            chunk.metadata['source'] = file.filename
            chunk.metadata['chunk_id'] = i

        logger.debug(f"Documents Processed into {len(text_chunks)} chunks")
        return text_chunks
    
    except Exception as e:
        logger.error(f"Error Processing Document: {str(e)}")
        raise PDFQueryException(f"Error Processing Document: {str(e)}", sys)
    
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)

@app.route('/upload', methods=['POST'])
def upload_document():
    """Document Upload and Processing"""
    try:
        logger.debug("Upload endpoin called")

        if 'file' not in request.files:
            logger.warning("NO file in request")
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            logger.warning("Empty Filename")
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file size (20mb limit as per requirements)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        if file_size > 20 * 1024 * 1024:
            return jsonify({'error': 'File size exceed 20MB'}), 400
        
        # Check file Extenstion
        if not file.filename.lower().endswith(('.txt', '.pdf')):
            logger.warning(f'Unsupported file type: {file.filename}')
            return jsonify({'error': 'Only .txt and .pdf files are supported'}), 400
        
        logger.debug(f"Processing File: {file.filename}")

        # Process the document
        try:
            text_chunks = process_document(file)
            logger.debug(f"Document Processed into {len(text_chunks)} chunks")
        except PDFQueryException as e:
            logger.error(f"Error processing Document: {str(e)}")
            return jsonify({'error': f'Error Processing document: {str(e)}'}), 500
        
        # Add to Vector Store
        try:
            vector_store.add_documents(text_chunks)
            logger.debug(f"Document processed into {len(text_chunks)} chunks")
        except Exception as e:
            logger.error(f"Error Adding to vector store")
            return jsonify({'error': f'Error adding to vectore store: {str(e)}'}), 500
        
        return jsonify({
            'message': 'File Uploaded and Processed Successfully',
            'filename': file.filename,
            'chunks_processed': len(text_chunks),
            'file_size': f"{file_size / (1024*1024):.2f} MB"
        })
    
    except PDFQueryException as e:
        logger.error(f"Unexpected Error: {str(e)}")
        return jsonify({'error': f'Unexpected Error: {str(e)}'}), 500


@app.route('/query', methods = ['POST'])
def query():
    """Handle User Question"""
    try:
        data = request.json
        if 'question' not  in data:
            return jsonify({'error': 'No Question Provide'}), 400
        
        question = data['question'].strip()
        if not question:
            return jsonify({'error': 'Question cannot be empty'}), 400
        
        logger.debug(f"Processing Question: {question}")

        # Get Response from LLM Service
        response = llm_service.get_response(question)

        # Store in session history
        if 'qa_history' not in session:
            session['qa_history'] = []

        session['qa_history'].append({
            'question': question,
            'answer': response,
            'timestamp': datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        })

        # Keep only last 10 Q&A pairs
        if len(session['qa_history']) > 10:
            session['qa_history'] = session['qa_history'][-10:]

        session.modified = True

        return jsonify({
            'response': response,
            'question': question
        })
    
    except Exception as e:
        logger.error(f"Error Processing Query: {str(e)}")
        return jsonify({'error': f'Error Processing Query: {str(e)}'}), 500
    

@app.route('/history', methods=['GET'])
def get_history():
    """Get Session Q&A History"""
    try:
        history = session.get('qa_history', [])
        return jsonify({'history': history})
    
    except Exception as e:
        logger.error(f"Error Retrieving History: {str(e)}")
        return jsonify({'error': f"Error Retrieving History: {str(e)}"}), 500
    

@app.route('/clear', methods= ['POST'])
def clear_session():
    """Clear session Data and vector store"""
    try:
        session.clear()
        # Note: In a production system, you'd want to clear only the user's data
        # For now, This clears the entire vectore store
        vector_store.clear()

        return jsonify({'message': 'Session cleared successfully'})
    except Exception as e:
        logger.error(f"Error clearing session: {str(e)}")
        return jsonify({'error': f'Error Clearing Session: {str(e)}'}), 500
    

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error_code=404, error_message= "Page not found"), 404
 
@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_code=500, error_message="Internal server error"), 500

@app.route('/health')
def health_check():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)