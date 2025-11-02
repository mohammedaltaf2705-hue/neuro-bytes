from typing import Optional
import io

try:
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


class ImageExtractor:
    """Extract text from images using OCR"""
    
    def __init__(self, tesseract_cmd: Optional[str] = None):
        if not OCR_AVAILABLE:
            raise ImportError("OCR libraries not available. Install Pillow and pytesseract.")
        
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        
        self.config = '--psm 6'  # Assume uniform block of text
    
    def extract_from_file(self, file_path: str, language: str = 'eng') -> str:
        """
        Extract text from an image file
        
        Args:
            file_path: Path to the image file
            language: OCR language (default: 'eng')
            
        Returns:
            Extracted text
        """
        try:
            image = Image.open(file_path)
            return self._extract_from_image(image, language)
        except Exception as e:
            raise Exception(f"Error extracting text from image: {str(e)}")
    
    def extract_from_bytes(self, image_bytes: bytes, language: str = 'eng') -> str:
        """
        Extract text from image bytes
        
        Args:
            image_bytes: Image file as bytes
            language: OCR language (default: 'eng')
            
        Returns:
            Extracted text
        """
        try:
            image = Image.open(io.BytesIO(image_bytes))
            return self._extract_from_image(image, language)
        except Exception as e:
            raise Exception(f"Error extracting text from image bytes: {str(e)}")
    
    def _extract_from_image(self, image: Image.Image, language: str = 'eng') -> str:
        """
        Extract text from a PIL Image object
        
        Args:
            image: PIL Image object
            language: OCR language
            
        Returns:
            Extracted text
        """
        # Preprocess image for better OCR results
        image = self._preprocess_image(image)
        
        # Perform OCR
        text = pytesseract.image_to_string(
            image,
            lang=language,
            config=self.config
        )
        
        return text.strip()
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR accuracy
        
        Args:
            image: Input PIL Image
            
        Returns:
            Preprocessed PIL Image
        """
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to grayscale
        image = image.convert('L')
        
        # Increase contrast
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        # Increase sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(2.0)
        
        return image
    
    def get_image_info(self, file_path: str) -> dict:
        """
        Get image metadata
        
        Args:
            file_path: Path to the image file
            
        Returns:
            Dictionary of image information
        """
        try:
            image = Image.open(file_path)
            return {
                'format': image.format,
                'mode': image.mode,
                'size': image.size,
                'width': image.width,
                'height': image.height,
                'info': image.info
            }
        except Exception as e:
            return {'error': str(e)}
    
    def extract_with_confidence(self, file_path: str, language: str = 'eng') -> dict:
        """
        Extract text with confidence scores
        
        Args:
            file_path: Path to the image file
            language: OCR language
            
        Returns:
            Dictionary with text and confidence data
        """
        try:
            image = Image.open(file_path)
            image = self._preprocess_image(image)
            
            # Get detailed OCR data
            data = pytesseract.image_to_data(
                image,
                lang=language,
                config=self.config,
                output_type=pytesseract.Output.DICT
            )
            
            # Calculate average confidence
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            # Extract text
            text = pytesseract.image_to_string(image, lang=language, config=self.config)
            
            return {
                'text': text.strip(),
                'confidence': avg_confidence,
                'word_count': len([w for w in data['text'] if w.strip()]),
                'data': data
            }
        except Exception as e:
            return {'error': str(e), 'text': '', 'confidence': 0}
