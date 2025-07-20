import sys
from pathlib import Path
from setuptools import setup, find_packages

if sys.version_info < (3, 10):
    print("Error: PDFQuery requires Python 3.10 or higher")
    sys.exit(1)

def read_readme():
    """Read README.md file for long description."""
    readme_path = Path(__file__).parent / "README.md"
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "PDFQuery - PDF-Based Question Answering System using RAG with Langchain and Openai API"

def read_requirements():
    """Read requirements from requirements.txt file."""
    requirements_path = Path(__file__).parent / "requirements.txt"
    if requirements_path.exists():
        with open(requirements_path, "r", encoding="utf-8") as f:
            requirements = []
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("-"):
                    requirements.append(line)
            return requirements
         
    return [
        "Flask",
        "langchain",
        "langchain-openai",
        "langchain-community",
        "langchain-groq",
        "chromadb",
        "PyPDF2",
        "pdfplumber",
        "python-dotenv",
        "sentence-transformers",
        "requests",
        "Werkzeug",
        "huggingface-hub",
        "transformers",
        "torch",
        "numpy",
        "Jinja2",
        "urllib3",
        "charset-normalizer",
        "idna",
        "certifi"
    ]

dev_requirements = [
    "pytest",
    "pytest-cov",
    "black",
    "flake8",
    "isort",
    "pre-commit",
    "pytest-flask",
    "pytest-mock"
]

docker_requirements = [
    "gunicorn",
    "gevent"
]

setup(
    name="pdfQuery",
    version="0.1.0",
    author="Durgesh Singh",
    author_email="durgeshsingh12712@gmail.com",
    description="PDF-Based Question Answering System using RAG with Langchain and Openai API",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Durgeshsingh12712/PDFQuery---PDF-based-Question-Answering-System",
    project_urls={
        "Bug Tracker": "https://github.com/Durgeshsingh12712/PDFQuery---PDF-based-Question-Answering-System/issues",
        "Source": "https://github.com/Durgeshsingh12712/PDFQuery---PDF-based-Question-Answering-System",
        "Documentation": "https://github.com/Durgeshsingh12712/PDFQuery---PDF-based-Question-Answering-System/blob/main/README.md"
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Text Processing :: Markup :: HTML",
        "Framework :: Flask"
    ],
    keywords="PDF question-answering RAG langchain openai ai ml flask webapp",
    python_requires=">=3.10",
    install_requires=read_requirements(),
    include_package_data=True,
    extras_require={
        'dev': dev_requirements,
        'docker': docker_requirements,
        'all': dev_requirements + docker_requirements
    },
    zip_safe=False,
    platforms=["any"],
    license="MIT",
    maintainer="Durgesh Singh",
    maintainer_email="durgeshsingh12712@gmail.com",

    package_data={
        'pdfQuery': [
            'templates/*.html',
            'static/css/*.css', 
            'static/js/*.js'
        ]
    }
)