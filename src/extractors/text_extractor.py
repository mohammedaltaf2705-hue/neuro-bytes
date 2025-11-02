from typing import Optional
import re


class TextExtractor:
    """Extract and clean text from plain text sources"""
    
    def __init__(self):
        self.encoding = 'utf-8'
    
    def extract_from_string(self, text: str) -> str:
        """
        Extract and clean text from a string
        
        Args:
            text: Input text string
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        cleaned_text = self._clean_text(text)
        return cleaned_text
    
    def extract_from_file(self, file_path: str) -> str:
        """
        Extract text from a text file
        
        Args:
            file_path: Path to the text file
            
        Returns:
            Extracted text
        """
        try:
            with open(file_path, 'r', encoding=self.encoding, errors='ignore') as f:
                text = f.read()
            return self._clean_text(text)
        except Exception as e:
            raise Exception(f"Error reading text file: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep medical notation
        text = re.sub(r'[^\w\s\-\+\.\,\:\;\(\)\/\%\°\']', '', text)
        
        # Normalize line breaks
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Remove multiple consecutive newlines
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        return text.strip()
    
    def extract_sections(self, text: str) -> dict:
        """
        Extract common medical document sections
        
        Args:
            text: Input text
            
        Returns:
            Dictionary of sections
        """
        sections = {}
        
        # Common section headers
        section_patterns = {
            'patient_info': r'(?i)(patient\s+information|demographics|patient\s+details)',
            'chief_complaint': r'(?i)(chief\s+complaint|presenting\s+complaint|cc)',
            'history': r'(?i)(history\s+of\s+present\s+illness|hpi|medical\s+history)',
            'medications': r'(?i)(medications?|current\s+medications|drugs)',
            'allergies': r'(?i)(allergies|adverse\s+reactions)',
            'vitals': r'(?i)(vital\s+signs|vitals)',
            'physical_exam': r'(?i)(physical\s+exam|examination|pe)',
            'assessment': r'(?i)(assessment|diagnosis|impression)',
            'plan': r'(?i)(plan|treatment\s+plan|recommendations)',
            'labs': r'(?i)(lab\s+results|laboratory|test\s+results)',
        }
        
        for section_name, pattern in section_patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                start = match.end()
                # Find the next section or end of text
                next_section = None
                for other_pattern in section_patterns.values():
                    next_match = re.search(other_pattern, text[start:])
                    if next_match:
                        if next_section is None or next_match.start() < next_section:
                            next_section = next_match.start()
                
                if next_section:
                    section_text = text[start:start + next_section]
                else:
                    section_text = text[start:]
                
                sections[section_name] = section_text.strip()
                break
        
        return sections
