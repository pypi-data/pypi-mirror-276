from typing import Type
from flexidata.utils.constants import OCREngine
from flexidata.config.config import Config

config = Config()
class OCRAgentFactory:
    def __init__(self):
        self.engine_map = {
            OCREngine.TESSERACT: "flexidata.ocr.tesseract.TesseractOCR",
            OCREngine.PADDLE: "flexidata.ocr.paddle.CustomPaddleOCR",
            OCREngine.GOOGLE_VISION: "flexidata.ocr.google_vision.GoogleVisionOCR",
        }

    def get_ocr_agent(self, engine: OCREngine = None) -> Type:
        """
        Dynamically imports and returns an OCR agent class based on the specified engine.

        Args:
            engine (OCREngine): The OCR engine type from the OCREngine enumeration, defaults to configuration if None.

        Returns:
            An instance of the OCR agent class corresponding to the specified engine.

        Raises:
            ValueError: If the specified engine is not supported.
            ImportError: If there's an issue importing the required OCR module.
        """
        if engine is None:
            engine = config.get("OCR_ENGINE", OCREngine.PADDLE)
        
        try:
            # Split the fully qualified class name to module and class name
            module_path, class_name = self.engine_map[engine].rsplit('.', 1)
            print(f"module_path={module_path} class_name={class_name}")
            # Dynamically import the module containing the OCR class
            module = __import__(module_path, fromlist=[class_name])
            # Create and return an instance of the OCR class
            return getattr(module, class_name)()
        except KeyError:
            raise ValueError(f"Unsupported OCR engine: {engine}")
        except ImportError as e:
            raise ImportError(f"Could not import the required OCR module: {e}")
        
    def get_current_engine(self) -> OCREngine:
        """
        Returns the current OCR engine set in the configuration.

        Returns:
            OCREngine: The currently set OCR engine.
        """
        return config.get("OCR_ENGINE", OCREngine.PADDLE)

