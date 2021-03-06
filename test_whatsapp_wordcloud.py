#!/usr/bin/env python3

import unittest
import re
from whatsapp_wordcloud import _punctuation_cleaner
from whatsapp_wordcloud import text_cleaner
from whatsapp_wordcloud import contact_text_separator
from whatsapp_wordcloud import color_generator
from whatsapp_wordcloud import file_finder
from whatsapp_wordcloud import word_counter
from whatsapp_wordcloud import colorgroup_generator

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

    def test_color_generator(self):
        testcase = color_generator({'contact_01': "text",
                                    'contact_02': "text",
                                    'contact_03': "text",
                                    'contact_04': "text"})
        self.assertGreaterEqual(len(testcase), 4)
        for case in testcase:
            self.assertRegex(case,r"^#\w{6}")

    def test_file_finder_one_extension(self):
        testcase = file_finder("test files\\test_filefinder", ".2")
        expected = [["testfile_03.2", "test files\\test_filefinder\\testfile_03.2"], ["testfile_04.2", "test files\\test_filefinder\\testfile_04.2"]]
        self.assertEqual(testcase, expected)

    def test_file_finder_multiple_extensions(self):
        testcase = file_finder("test files\\test_filefinder", (".1", ".3"))
        expected = [["testfile_02.1", "test files\\test_filefinder\\testfile_02.1"], ["testfile_05.3", "test files\\test_filefinder\\testfile_05.3"]]
        self.assertEqual(testcase, expected)
    
    def test_file_finder_all_extensions(self):
        testcase = file_finder("test files\\test_filefinder")
        expected = [["testfile_02.1", "test files\\test_filefinder\\testfile_02.1"],["testfile_03.2", "test files\\test_filefinder\\testfile_03.2"], ["testfile_04.2", "test files\\test_filefinder\\testfile_04.2"], ["testfile_05.3", "test files\\test_filefinder\\testfile_05.3"]]
        self.assertEqual(testcase, expected)

    def test_word_counter(self):
        testcase = {'contact_01': ["hola", "como", "esta"],
                    'contact_02': ["hola", "bien", "y", "ud"],
                    'contact_03': ["bien", "como", "esta", "su", "familia"]}
        expected = {'hola': 2, 'como': 2, 'esta': 2, 'bien': 2, 'y': 1, 'ud': 1, 'su': 1, 'familia': 1}
        self.assertEqual(word_counter(testcase), expected)

    def test_colorgroup_generator(self):
        testcase = colorgroup_generator({'contact_01': "Hola, rojo fuego",
                                        'contact_02': "Vida feliz",
                                        'contact_03': "Gato purpura tierno, fantástico",
                                        'contact_04': "Intenta dos veces"})
        expected = [["hola", "rojo", "fuego"], ["vida", "feliz"], ["gato", "purpura", "tierno", "fantástico"], ["intenta", "dos", "veces"]]
        for case in testcase.keys():
            self.assertRegex(case,r"^#\w{6}")
        for index, case in enumerate(testcase.values()):
            self.assertEqual(case, expected[index])
    
if __name__ == "__main__":
    unittest.main()

