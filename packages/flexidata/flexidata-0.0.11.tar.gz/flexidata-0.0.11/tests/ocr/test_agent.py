import unittest
from flexidata.ocr.agent import OCRAgentFactory
from flexidata.utils.constants import OCREngine

class TestAgent(unittest.TestCase):
    def test_get_ocr_agent_with_valid_engine(self):
        ocr_factory = OCRAgentFactory()
        agent = ocr_factory.get_ocr_agent(OCREngine.PADDLE)
        self.assertIsNotNone(agent)

    def test_get_ocr_agent_with_no_engine(self):
        # Assuming the function returns a default agent when no engine is specified
        ocr_factory = OCRAgentFactory()
        agent = ocr_factory.get_ocr_agent(None)
        self.assertIsNotNone(agent)

    def test_get_ocr_agent_with_invalid_engine(self):
        # Assuming the function raises an exception for invalid engines
        ocr_factory = OCRAgentFactory()
        with self.assertRaises(Exception):
            ocr_factory.get_ocr_agent('invalid_engine')

if __name__ == "__main__":
    unittest.main()

