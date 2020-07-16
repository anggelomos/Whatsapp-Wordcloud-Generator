#!/usr/bin/env python3

import subprocess

# Install automatically external modules in case it isn't possible print an error message
try:
    import wordcloud
    from PIL import Image
    from matplotlib import pyplot as plt
    import numpy as np
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    try:
        subprocess.run(["pip3", "install", "-e", "."]) # Installs all the required modules in the setup.py (wordcloud, pillow, matplotlib and numpy)
    except:
        print("Some python modules could not be installed, please install them and run the script again. Required Modules: wordcloud, PIL (or pillow), matplotlib and numpy")

import sys
import re
import os
import random
import collections


class GroupedColorFunc(object):
    """Create a color function object which assigns DIFFERENT SHADES of
       specified colors to certain words based on the color to words mapping.

       Uses wordcloud.get_single_color_func

       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.

       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.color_func_to_words = [
            (wordcloud.get_single_color_func(color), set(words))
            for (color, words) in color_to_words.items()]

        self.default_color_func = wordcloud.get_single_color_func(default_color)

    def get_color_func(self, word):
        """Returns a single_color_func associated with the word"""
        try:
            color_func = next(
                color_func for (color_func, words) in self.color_func_to_words
                if word in words)
        except StopIteration:
            color_func = self.default_color_func

        return color_func

    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)

uninteresting_words_en = {"a", "pm", "was", "at", "her", "of", "also", "although", "with",  "is", "as", "by", "an", "the", "for", "and", "nor", "but", "or", "yet", "and", "so","on", "in", "to", "since", "for", "ago", "before", "past", "I", "me", "he", "she", "herself", "you", "it", "that", "they", "each", "few", "many", "who", "whoever", "whose", "someone", "everybody"}
uninteresting_words_es = {"mi", "hay", "fue","están", "he", "ha", "del", "al", "eso", "era", "ese", "esta", "son", "uno", "qué", "está", "nequi", "sí", "si", "no", "les", "es", "pm", "am", "un", "una", "unos", "unas", "el", "los", "la", "las", "lo", "le", "y", "e", "ni", "que", "pero", "mas", "más", "aunque", "sino", "siquiera", "o", "u", "otra", "sea", "ya", "este", "aquél", "aquel", "pues", "porque", "puesto", "que", "como", "así", "asi", "luego", "tan", "tanto", "conque", "a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "durante", "en" , "entre", "hacia", "hasta", "mediante", "para", "por", "según", "segun", "sin", "so", "sobre", "tras", "versus", "vía", "via", "yo", "tú", "tu", "él", "usted", "ustedes", "nosotros", "nosotras", "vosotros", "vosotras", "ellos", "ellas", "me", "te", "nos", "se"}

def contact_text_separator(whatsapp_chat_path: str) -> dict:
    """Generate a dictionary where the keys are the names of each contact and the values are what they said

    Parameters
    ----------
    whatsapp_chat_path : str
        Path to the .txt file that contains the whatsapp chat.

    Returns
    -------
    contact_speech_dictionary: dict(str)
        Dictionary where the keys are the names of each contact and the values are what they said.
    """
    contact_speech_dictionary = {}
    with open(whatsapp_chat_path, "r", encoding="utf8") as source_file:

        for line in source_file:
            matched_contact = re.match(r"^\d+/\d+/\d{2}, \d:\d{2} [AP]M - (.*?): (.*)\n", line)    # Match contact name in group 1 and what they said in group 2
            if matched_contact is not None:
                # Add contact to dictionary if it isn't there already
                cotact_name = matched_contact[1]
                contact_speech = matched_contact[2] + " "

                if cotact_name not in contact_speech_dictionary:
                    contact_speech_dictionary[cotact_name] = contact_speech
                else:
                    contact_speech_dictionary[cotact_name] += contact_speech
    return contact_speech_dictionary

def _punctuation_cleaner(word_list: list) -> list:
    """Delete punctuation symbols in each word of a list

    Parameters
    ----------
    word_list : list(str)
        List containing all the words that will be cleaned separately

    Returns
    -------
    cleaned_words: list(srt)
        List containing all the words without punctuation symbols.
    """

    cleaned_words = []

    for word in word_list:
        if word.isalpha():
            cleaned_words.append(word)
        else:
            cleaned_word = re.sub(r"[\W]", "", word)     # Here we delete the punctuation symbols of each word using a regex pattern and the re.sub() function
            # after cleaning the word we check if it actually got cleaned if it didn't it gets discarted
            if cleaned_word.isalpha():
                cleaned_words.append(cleaned_word)

    return cleaned_words

def text_cleaner(text: str, uninteresting_words: list=uninteresting_words_en) -> list: 
    """Delete punctuation symbols, uninteresting words (articles, conjunctions, prepositions, pronouns, etc.)

    Parameters
    ----------
    text : str
        The text we want to clean
    uninteresting_words : list(str)
        List of the words we want to delete from the text. Ex. "the", "a", "in".

    Returns
    -------
    clean_text: list(str)
        List of every individual word present in the text input without any punctuation symbol and excluding the uninteresting words.
    """

    lower_cased_text = text.lower()
    splitted_text = lower_cased_text.split()    # Here we crerate a list with the words that are separated by a space

    unpunctuated_text = _punctuation_cleaner(splitted_text)
    
    clean_text = [element for element in unpunctuated_text if element not in uninteresting_words]    # Here we delete the uninteresting words from the cleaned using list comprehensions

    return clean_text

def color_generator(contacts: dict) -> list:
    """Generate a list of HEX color codes extracted from coolors.co pallettes.
       It generates at least as many colors as the amount of contacts.

    Parameters
    ----------
    contacts : dict(str)
        Dictionary where the keys are the names of the contacts.

    Returns
    -------
    color_pallette : list(str)
        List of HEX color codes.
    """
    amount_contacts = len(contacts)

    # Open a downloaded version of the website coolors.co 
    with open("font\\coolors.html") as coolors_web_source:
        web_scrapper = BeautifulSoup(coolors_web_source, 'html.parser')

    pallette_container = web_scrapper.find_all('div', class_="explore-palette_colors")

    color_pallette = []
    pallette_seed = random.sample(range(46), 45)    # List of random numbers to select a pallete
    cyc = 0     # cycle counter
    # In this cycle we add random pallettes until there are more colors than contacts
    while len(color_pallette) < amount_contacts:
        color_pallette += ["#"+color.text for color in pallette_container[pallette_seed[cyc]].find_all('span')]     # Add hex colors to the list from a pallette randomly selected from the pallette container
        cyc += 1

    return color_pallette



"""

contact_names = []

    for contact in chat_members:
        contact_names.append(contact[0])
    
    def name_to_color(name, contact_names, chat_members):
        cycle_counter = 0
        for contact in contact_names:
            if contact == name:
                return chat_members[cycle_counter][1]
            cycle_counter += 1

    processed_words = set([])
    color_groups = {}

    for contact in chat_members:
        color_groups[contact[1]] = []

    for word in final_text:
        if word in contact_names:
            current_key = name_to_color(word, contact_names, chat_members)
        else:
            if word in processed_words:
                pass
            else:
                if current_key is not None:
                    color_groups[current_key].append(word)
                    #print("key is none")

        processed_words.add(word)

    final_text = [element for element in final_text if element not in contact_names]


def word_counter(words_to_count):
    counter = collections.Counter(words_to_count)
    return dict(counter)

# Reading the text file

with open("demo.txt", "r", encoding="utf8") as source_file:
    raw_text = source_file.read()

default_color = 'grey'

# Here we generate both the list of words cleaned and the dictionary of words assigned to each color

clean_text, color_groups = text_cleaner(raw_text, [["shushis", "#F9C74F"], ["cabrera", "#577590"], ["casta", "#43AA8B"], ["mosquera", "#90BE6D"], ["angelo", "#000000"], ["carlos", "#000000"]], uninteresting_words_es)

# Here we use the color function to transform the dictionary of words assigned to each color into a color function accepted by the wordcloud library

grouped_color_func = GroupedColorFunc(color_groups, default_color)

# Here we create a dictionary where the keys are the words and the value is the amount of times the key is in the text

counted_words = word_counter(clean_text)

# This is a black and white mask, the words fill the black areas

mask_image = np.array(Image.open("F:/Coding/IT Automation Specialization - Coursera/Python Crash Course/Final project - wordcloud feeder/Wordcloud-feeder -master/image masks/fer.jpg"))

# And finally here we generate the wordcloud using the wordcloud class

cloud = wordcloud.WordCloud(background_color="white", mask=mask_image, max_words = 300, max_font_size=60, min_font_size=10, width=1920, height=1920, font_path="F:/Coding/IT Automation Specialization - Coursera/Python Crash Course/Final project - wordcloud feeder/Wordcloud-feeder -master/fonts/minimal.otf")
cloud.generate_from_frequencies(counted_words)

#image_colors = wordcloud.ImageColorGenerator(maya_coloring)

# Here we print the final image

myimage = cloud.to_array()
plt.figure(figsize=(27, 15), dpi=72)
plt.imshow(myimage, interpolation = 'bilinear')
plt.imshow(cloud.recolor(color_func=grouped_color_func), interpolation="bilinear")
plt.axis('off')
plt.show()

"""