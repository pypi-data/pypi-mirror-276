from typing import Union
import numpy as np
from PIL import Image
from flexidata.utils.constants import OCREngine
import pandas as pd
from typing import List, Dict, Any
from flexidata.text_processing.text_block import TextBlock, TextBlockMetadata

try:
    import pytesseract
except ImportError as e:
    raise ImportError(f"Failed to import pytesseract: {str(e)}") from e


class TesseractOCR:
    def __init__(self) -> None:
        """Initializes the TesseractOCR object."""
        pass

    def image_to_text(
        self,
        image: Union[Image.Image, np.ndarray],
        lang: str = "eng",
        page_number=None,
        file_path=None,
        filetype=None,
    ) -> List[Dict[str, Any]]:
        """
        Converts an image to text using Tesseract OCR, handling both PIL Image objects and numpy arrays.

        Args:
            image (Union[Image.Image, np.ndarray]): The image to be processed, which can be either
                a PIL Image object or a numpy array.
            lang (str): The language to use for OCR processing. Defaults to 'eng'.

        Returns:
            str: The extracted text from the image as a string.
        """
        # Convert numpy array to PIL Image if necessary
        if isinstance(image, np.ndarray):
            # Ensure the array is in a format suitable for conversion to an Image
            if image.ndim == 3 and image.shape[2] in [
                3,
                4,
            ]:  # Check for 3 (RGB) or 4 (RGBA) channels
                image = Image.fromarray(image)
            else:
                raise ValueError(
                    "Unsupported numpy array shape for image conversion to PIL Image."
                )

        elif not isinstance(image, Image.Image):
            raise TypeError("The image must be a PIL.Image.Image or numpy.ndarray.")

        # Perform OCR using pytesseract
        ocr_data = pytesseract.image_to_data(
            image, lang=lang, output_type=pytesseract.Output.DATAFRAME
        )
        elements = self.get_text_with_metadata(
            ocr_data, lang, page_number, file_path, filetype
        )
        return elements

    def get_text_with_metadata(
        self,
        ocr_data,
        lang: str = "en",
        page_number=None,
        file_path=None,
        filetype=None,
    ):
        ocr_data = ocr_data[ocr_data.conf != "-1"]
        ocr_data["text"] = ocr_data["text"].fillna("").astype(str)
        # Calculate the 'right' and 'bottom' coordinates for each word
        ocr_data["right"] = ocr_data["left"] + ocr_data["width"]
        ocr_data["bottom"] = ocr_data["top"] + ocr_data["height"]

        # Group by the hierarchical structure up to the line level and join the words
        grouped_text = (
            ocr_data.groupby(["page_num", "block_num", "par_num", "line_num"])
            .agg(
                {
                    "text": " ".join,
                    "left": "min",
                    "top": "min",
                    "right": "max",
                    "bottom": "max",
                }
            )
            .reset_index()
        )
        page_elements = []
        for index, ocr_row in grouped_text.iterrows():
            text = ocr_row["text"]
            cleaned_text = str(text) if not isinstance(text, str) else text.strip()
            if cleaned_text:
                bbox = [
                    ocr_row["left"],
                    ocr_row["top"],
                    ocr_row["right"],
                    ocr_row["bottom"],
                ]
                metadata = TextBlockMetadata(
                    file_path=file_path,
                    languages=lang,
                    filetype=filetype,
                    page_number=page_number,
                    bbox=bbox,
                    extraction_source=OCREngine.TESSERACT,
                )
                element = TextBlock(text=cleaned_text, metadata=metadata)

                page_elements.append(element)

        return page_elements
