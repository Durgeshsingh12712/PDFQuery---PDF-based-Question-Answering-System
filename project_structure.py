import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "pdfQuery"

list_of_files = [
    "config/config.py",
    f"{project_name}/__init__.py",
    f"{project_name}/services/__init__.py",
    f"{project_name}/services/llm_service.py",
    f"{project_name}/models/__init__.py",
    f"{project_name}/models/vector_store.py",
    f"{project_name}/exceptions/__init__py",
    f"{project_name}/exceptions/exception.py",
    f"{project_name}/logging/__init__.py",
    f"{project_name}/logging/logger.py",
    "vector_db/.gitkeep",
    "templates/index.html",
    "static/css/style.css",
    "static/js/script.js",
    ".env",
    "app.py",
    "Dockerfile",
    "requirements.txt",
    "setup.py"
]

for filepath in list_of_files:
    filepath = Path(filepath)

    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating Directory: {filedir} for the file {filename}")

    if(not os.path.exists(filename)) or (os.path.getsize(filename)  == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating Empty File: {filename}")
    
    else:
        logging.info(f"{filename} is already Created")