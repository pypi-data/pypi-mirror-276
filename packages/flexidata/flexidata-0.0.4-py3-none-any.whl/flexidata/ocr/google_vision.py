from google.cloud import vision
import io
from flexidata.utils.text import TextType
from flexidata.utils.constants import OCREngine
from PIL import Image
from typing import List, Dict, Any
import numpy as np
from google.cloud.vision import Paragraph, TextAnnotation
from flexidata.text_processing.text_block import TextBlock, TextBlockMetadata


class GoogleVisionOCR:
    def __init__(self) -> None:
        """
        Initializes the GoogleVisionOCR class by setting up a client for the Google Vision API.
        """
        self.client = vision.ImageAnnotatorClient()

    def image_to_text(
        self,
        image: np.ndarray,
        lang: str = "eng",
        page_number=None,
        file_path=None,
        filetype=None,
    ) -> List[Dict[str, Any]]:
        """
        Converts an image to text using Google Vision's document text detection.

        Args:
            image (np.ndarray): The image data as a numpy array.
            lang (str): The language code to be used by the OCR engine.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each containing text and its metadata.
        """
        # Convert np.array to PIL Image
        pil_image = Image.fromarray(image)

        # Convert PIL Image to bytes
        with io.BytesIO() as output:
            pil_image.save(output, format="JPEG")
            content = output.getvalue()

        image = vision.Image(content=content)

        # Use document_text_detection for better recognition of structured text
        response = self.client.document_text_detection(image=image)
        ocr_data = response.full_text_annotation
        elements = self.get_text_with_metadata(
            ocr_data, lang, page_number, file_path, filetype
        )
        return elements

    def get_text_with_metadata(
        self,
        ocr_data: TextAnnotation,
        lang: str = "en",
        page_number=None,
        file_path=None,
        filetype=None,
    ) -> List[Dict[str, Any]]:
        """
        Extracts text and its associated metadata from the OCR data.

        Args:
            ocr_data (TextAnnotation): The annotated text data from the OCR process.
            lang (str): The language of the text.

        Returns:
            List[Dict[str, Any]]: A list of text elements with associated metadata.
        """
        elements = []
        for page in ocr_data.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    text = self.get_paragraph_text(paragraph)
                    vertices = paragraph.bounding_box.vertices
                    x1, y1 = vertices[0].x, vertices[0].y
                    x2, y2 = vertices[2].x, vertices[2].y
                    metadata = TextBlockMetadata(
                        file_path=file_path,
                        languages=[lang],
                        filetype=filetype,
                        page_number=page_number,
                        bbox=[x1, y1, x2, y2],
                        extraction_source=OCREngine.GOOGLE_VISION,
                    )
                    element = TextBlock(text=text, metadata=metadata)
                    elements.append(element)
        return elements

    def get_paragraph_text(self, paragraph: Paragraph) -> str:
        """
        Extracts the full text from a paragraph object, handling different types of breaks.

        Args:
            paragraph (Paragraph): A paragraph of text as identified by the OCR.

        Returns:
            str: The concatenated text of the paragraph.
        """
        final_paragraph = ""
        line = ""
        for word in paragraph.words:
            for symbol in word.symbols:
                line += symbol.text
                # Add space after words depending on the detected break type
                if (
                    symbol.property.detected_break.type_
                    == TextAnnotation.DetectedBreak.BreakType.SPACE
                ):
                    line += " "
                if (
                    symbol.property.detected_break.type_
                    == TextAnnotation.DetectedBreak.BreakType.EOL_SURE_SPACE
                ):
                    line += " "
                    final_paragraph += line
                    line = ""
                if (
                    symbol.property.detected_break.type_
                    == TextAnnotation.DetectedBreak.BreakType.LINE_BREAK
                ):
                    final_paragraph += line
                    line = ""
        return final_paragraph
