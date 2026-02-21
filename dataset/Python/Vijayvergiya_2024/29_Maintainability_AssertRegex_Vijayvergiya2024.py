"""
Source: Vijayvergiya et al. (2024), Figure 1
Language: Python
Category: Maintainability / Unit Testing
Description: Testing for exceptions without verifying the error message.
AI Suggestion: Use self.assertRaisesRegex instead of self.assertRaises to verify the error text.
"""
import unittest

def get_url_to_bytes(url, allow_file_url=False):
    if not allow_file_url and url.startswith("file://"):
        raise ValueError("File URL not explicitly allowed: " + url)
    return b"fake_data"

class TestUrlLoading(unittest.TestCase):
    def test_file_url_not_allowed(self):
        fake_file_url = "file://fake_image.png"
        
        # הקוד המקורי - בודק רק את סוג השגיאה
        with self.assertRaises(ValueError):
            get_url_to_bytes(fake_file_url, allow_file_url=False)
