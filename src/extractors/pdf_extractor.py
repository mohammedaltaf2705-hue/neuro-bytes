from typing import Optional, List
import io
try:
    import PyPDF2
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False


class PDFExtractor:
    """Extract text from PDF documents"""
    
    def __init__(self):
        if not PDF_AVAILABLE:
            raise ImportError("PDF libraries not available. Install PyPDF2 and pdfplumber.")
        self.method = 'pdfplumber'  # Default method
    
    def extract_from_file(self, file_path: str, method: Optional[str] = None) -> str:
        """
        Extract text from a PDF file
        
        Args:
            file_path: Path to the PDF file
            method: Extraction method ('pdfplumber' or 'pypdf2')
            
        Returns:
            Extracted text
        """
        method = method or self.method
        
        try:
            if method == 'pdfplumber':
                return self._extract_with_pdfplumber(file_path)
            elif method == 'pypdf2':
                return self._extract_with_pypdf2(file_path)
            else:
                raise ValueError(f"Unknown extraction method: {method}")
        except Exception as e:
            raise Exception(f"Error extracting PDF: {str(e)}")
    
    def extract_from_bytes(self, pdf_bytes: bytes, method: Optional[str] = None) -> str:
        """
        Extract text from PDF bytes
        
        Args:
            pdf_bytes: PDF file as bytes
            method: Extraction method ('pdfplumber' or 'pypdf2')
            
        Returns:
            Extracted text
        """
        method = method or self.method
        
        try:
            if method == 'pdfplumber':
                return self._extract_bytes_with_pdfplumber(pdf_bytes)
            elif method == 'pypdf2':
                return self._extract_bytes_with_pypdf2(pdf_bytes)
            else:
                raise ValueError(f"Unknown extraction method: {method}")
        except Exception as e:
            raise Exception(f"Error extracting PDF from bytes: {str(e)}")
    
    def _extract_with_pdfplumber(self, file_path: str) -> str:
        """Extract text using pdfplumber"""
        text_parts = []
        
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        
        return '\n\n'.join(text_parts)
    
    def _extract_bytes_with_pdfplumber(self, pdf_bytes: bytes) -> str:
        """Extract text from bytes using pdfplumber"""
        text_parts = []
        
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        
        return '\n\n'.join(text_parts)
    
    def _extract_with_pypdf2(self, file_path: str) -> str:
        """Extract text using PyPDF2"""
        text_parts = []
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        
        return '\n\n'.join(text_parts)
    
    def _extract_bytes_with_pypdf2(self, pdf_bytes: bytes) -> str:
        """Extract text from bytes using PyPDF2"""
        text_parts = []
        
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        
        return '\n\n'.join(text_parts)
    
    def get_metadata(self, file_path: str) -> dict:
        """
        Extract PDF metadata
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dictionary of metadata
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata = pdf_reader.metadata
                
                return {
                    'title': metadata.get('/Title', ''),
                    'author': metadata.get('/Author', ''),
                    'subject': metadata.get('/Subject', ''),
                    'creator': metadata.get('/Creator', ''),
                    'producer': metadata.get('/Producer', ''),
                    'creation_date': metadata.get('/CreationDate', ''),
                    'num_pages': len(pdf_reader.pages)
                }
        except Exception as e:
            return {'error': str(e)}
