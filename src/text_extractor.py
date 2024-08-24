import os
import pdfplumber
from bidi import get_display
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from logger import logging
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'


def does_pdf_contains_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract text from the current page
            text = page.extract_text()
            # Check if any text is found
            if text and text.strip():
                return True  # PDF contains text
    return False  # PDF does not contain text


def is_image(file_path):
    # List of common image file extensions
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".svg"}
    
    # Extract the file extension from the path and convert to lowercase
    file_extension = os.path.splitext(file_path)[1].lower()
    
    # Check if the extension is in the list of image extensions
    return file_extension in image_extensions


class TextExtraction:
    def __init__(self, file_path: str, is_image: bool) -> None:
        self.file_path = file_path
        self.is_image = is_image
        self.text_dict = {}
        self.clean_text_dict = {}

    def process(self):
        logging.info('TextExtraction.process Started')

        if self.is_image:
            self.extract_text_from_image()
        elif does_pdf_contains_text(self.file_path):
            self.extract_text_from_pdf_text()
        else:
            self.extract_text_from_pdf_image()

        self.preprocess_text()

        logging.info('TextExtraction.process Finished')

        return self.clean_text_dict

    def extract_text_from_image(self):
        # Open the image file
        image = Image.open(self.file_path)
        # Perform OCR on the image with both English and Arabic languages
        text = pytesseract.image_to_string(image, lang='eng+ara')

        self.text_dict["page1"] = text

    def extract_text_from_pdf_text(self):
        with pdfplumber.open(self.file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    self.text_dict[f"page{i+1}"] = text

    def extract_text_from_pdf_image(self):
        pages = convert_from_path(self.file_path)

        # Perform OCR on each page image
        for page_num, page_image in enumerate(pages):
            # Convert image to string with both English and Arabic languages
            page_text = pytesseract.image_to_string(page_image, lang='eng+ara')
            self.text_dict[f"page{page_num + 1}"] = page_text

    def preprocess_text(self):
        for page, text_ in self.text_dict.items():
            # LTR / RTL strings
            # displayed_text = get_display(text_)
            # remove empty strings
            clean_text = [text for text in text_.split("\n") if len(text.strip()) > 0]
            self.clean_text_dict[page] = "\n".join(clean_text)

