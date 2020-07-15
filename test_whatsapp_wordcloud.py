#!/usr/bin/env python3

import unittest
from whatsapp_wordcloud import _punctuation_cleaner
from whatsapp_wordcloud import text_cleaner
from  whatsapp_wordcloud import contact_text_separator

class TestWhatsappWordcloud(unittest.TestCase):

    def test_punctuation_cleaner(self):
        testcase = ["Hola", "como,", "está", "usted?", "-se", " siente", "bien."]
        expected = ["Hola", "como", "está", "usted", "se", "siente", "bien"]
        self.assertEqual(_punctuation_cleaner(testcase), expected)

    def test_text_cleaner(self):
        testcase = "Hola, como está usted? -se siente bien."
        expected = ["hola", "como", "está", "usted", "se", "siente", "bien"]
        self.assertEqual(text_cleaner(testcase), expected)

    def test_contact_text_separtor(self):
        self.maxDiff = None

        testcase = "test files\\testfile_01.txt"
        expected = {'contacto 1': "Hola, ¿alguien sabe por qué el sol sale por las mañanas? Interesante, muchas gracias, estuve mucho tiempo buscando la respuesta ",
                    'contacto 2': "Saludos, la respuesta es muy sencilla: Porque hay un momento  del día en el que tiene que ser por la mañana, entonces le toca salir, para ver más información puede entrar a https://elsolsaliohoy.? No hay problema . ",
                    'contacto 3': "Eso es: falso "}
        self.assertEqual(contact_text_separator(testcase), expected)

if __name__ == "__main__":
    unittest.main()

