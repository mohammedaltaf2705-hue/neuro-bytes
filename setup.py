from setuptools import setup, find_packages

setup(
    name="neuro-bytes-medical-extraction",
    version="1.0.0",
    description="Medical data extraction system for extracting structured information from medical documents",
    author="Neuro Bytes",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "pydantic>=2.5.0",
        "python-multipart>=0.0.6",
        "spacy>=3.7.2",
        "PyPDF2>=3.0.1",
        "pdfplumber>=0.10.3",
        "pytesseract>=0.3.10",
        "Pillow>=10.1.0",
        "python-dateutil>=2.8.2",
        "regex>=2023.10.3",
        "uvicorn>=0.24.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
