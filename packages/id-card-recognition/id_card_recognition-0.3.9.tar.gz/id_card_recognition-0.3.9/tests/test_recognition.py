import unittest
from id_card_recognition.recognition import process_id_card


class TestIDCardRecognition(unittest.TestCase):

    def test_process_id_card(self):
        image_file = "test_image.jpg"
        file_content = "test content"
        model = "moonshot-v1-8k"
        result, tokens_used = process_id_card(image_file, file_content, model)
        self.assertIsNotNone(result)
        self.assertIsInstance(tokens_used, int)


if __name__ == '__main__':
    unittest.main()
