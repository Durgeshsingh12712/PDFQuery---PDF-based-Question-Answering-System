# PDFQuery---PDF-based-Question-Answering-System

A Flask-based web application that allows users to upload PDF documents and ask questions about their content using Retrieval-Augmented Generation (RAG) with LangChain and OPENAI API.

## **HOmepage with Demo Video**
[![PDFQuery Demo - PDF Question Answering with AI](https://img.youtube.com/vi/dwjgm9phkOU/maxresdefault.jpg)](https://youtu.be/dwjgm9phkOU)

## Features

- **PDF Upload**: Upload PDF and TXT files (up to 20MB)
- **Question Answering**: Ask natural language questions about uploaded documents
- **RAG Pipeline**: Uses LangChain for document processing and OPENAI API for answer generation
- **Session Management**: Maintains Q&A history during the session
- **Responsive UI**: Modern, mobile-friendly interface built with Bootstrap
- **Real-time Chat**: Interactive chat interface with loading indicators
- **Error Handling**: Comprehensive error handling and user feedback

## Tech Stack

- **Backend**: Python 3.10, Flask
- **AI/ML**: LangChain, OpenAI API, OpenAI Embeddings
- **Vector Store**: ChromaDB
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Document Processing**: PyPDF2, pdfplumber
- **Deployment**: Docker, Docker Compose

## Prerequisites

- Python 3.10 or higher
- OPENAI API key (sign up at [OPENAI](https://platform.openai.com/))
- Docker (optional, for containerized deployment)

## Installation

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <https://github.com/Durgeshsingh12712/PDFQuery---PDF-based-Question-Answering-System>
   cd PDFQuery---PDF-based-Question-Answering-System
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI API key
   ```

5. **Create required directories**
   ```bash
   mkdir -p logs vector_db templates
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

   The application will be available at `http://localhost:8080`

### Docker Setup

1. **Build and run with Docker Compose**
   ```bash
   # Set your OPENAI API key in .env file first
   docker-compose up --build
   ```

2. **Or build and run manually**
   ```bash
   docker build -t pdfquery .
   docker run -p 8080:8080 -e OPENAI_API_KEY=your_api_key_here pdfquery
   ```

## Usage

1. **Upload Document**: Click on the upload area or drag and drop a PDF/TXT file
2. **Wait for Processing**: The system will extract text and create embeddings
3. **Ask Questions**: Type your questions in the chat interface
4. **Get Answers**: The system will provide answers based on the document content
5. **View History**: See your previous questions and answers in the chat
6. **Clear Session**: Use the clear button to reset everything

## Project Structure

```
PDFQuery---PDF-based-Question-Answering-System/
├── app.py                          
├── setup.py
├── requirements.txt
├── Dockerfile
├── .env
├── config/
│   └── config.py
├── pdfQuery/
│   ├── __init__.py
│   ├── services/
│   │   ├── __init__.py          
│   │   └── llm_service.py
│   ├── models/
│   │   ├── __init__.py          
│   │   └── vector_store.py
│   ├── exceptions/
│   │   ├── __init__.py          
│   │   └── exception.py
│   └── logging/
│       ├── __init__.py          
│       └── logger.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
└── vector_db/

```

## API Endpoints

- `GET /` - Main application page
- `POST /upload` - Upload and process documents 
- `POST /query` - Ask questions about uploaded documents
- `GET /history` - Retrieve Q&A history
- `POST /clear` - Clear session and vector store

## Configuration

The application can be configured through environment variables:

- `OPENAI_API_KEY` - OpenAI API key (required)
- `PINECONE_API_KEY` - Pinecone Api Key (optional)
- `GROQ_API_KEY` - Your Groq API key (optional alternative)
- `FLASK_ENV` - Flask environment (development/production)
- `FLASK_SECRET_KEY` - Flask session secret key

## Features in Detail

### Document Processing
- Supports PDF and TXT files
- 20MB file size limit
- Text extraction and chunking
- Vector embeddings using HuggingFace models

### Question Answering
- Uses OPENAI GPT-NANO-4.1 model for answer generation
- Retrieval-Augmented Generation (RAG) pipeline
- Context-aware responses
- Conversation memory

### User Interface
- Drag-and-drop file upload
- Real-time chat interface
- Progress indicators
- Error handling with user feedback
- Responsive design for mobile devices

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure your Openai API key is correctly set in the .env file
   - Check if the API key has sufficient credits

2. **Upload Failures**
   - Check file size (must be under 20MB)
   - Ensure file format is PDF or TXT
   - Check network connectivity

3. **Performance Issues**
   - Large documents may take time to process
   - Consider splitting very large documents

### Logs

Application logs are stored in the `logs/` directory with timestamps. Check these files for detailed error information.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open-source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the application logs
3. Create an issue in the repository

## Future Enhancements

- User authentication and persistent storage
- Multi-language support
- PDF preview functionality
- Advanced search capabilities
- Export conversation history
- Integration with other LLM providers

## **CICD**
![My Image](https://github.com/Durgeshsingh12712/Data-All/blob/main/pdfquery/Homepage.png)
