import pytesseract as tesseract
import cv2
import re

def extract_text(image_file):
    """
    The return value is a __dict__ with 2 keys 
    - "text"
    - "headings"

    Args:
        image_file (image_file): the image file to extract text from

    Returns:
        __dict__: it returns a dictionary with the extracted text and headings
                    extracted from the text.
    """
    heading_regex = r"^[A-Z0-9][^.]*[\n]$"
    image = cv2.imread(image_file)
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply the threshold
    _thresh_value, threshed_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    
    extracted_text = tesseract.image_to_string(threshed_image)
    headings = re.findall(heading_regex, extracted_text, re.MULTILINE)
    
    return { "text": extract_text, "headings": headings }
