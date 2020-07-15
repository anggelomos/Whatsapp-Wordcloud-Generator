#!/usr/bin/env python3

import unittest
from whatsapp_wordcloud import _punctuation_cleaner
from whatsapp_wordcloud import text_cleaner

class TestWhatsappWordcloud(unittest.TestCase):

    def test_punctuation_cleaner(self):
        testcase = ["Hola", "como,", "está", "usted?", "-se", " siente", "bien."]
        expected = ["Hola", "como", "está", "usted", "se", "siente", "bien"]
        self.assertEqual(_punctuation_cleaner(testcase), expected)

    def test_text_cleaner(self):
        testcase = "Hola, como está usted? -se siente bien."
        expected = ["hola", "como", "está", "usted", "se", "siente", "bien"]
        self.assertEqual(text_cleaner(testcase), expected)

if __name__ == "__main__":
    unittest.main()

