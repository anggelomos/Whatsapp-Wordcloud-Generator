#!/usr/bin/env python3

import subprocess

# Install automatically external modules in case it isn't possible print an error message
try:
    import wordcloud
    from PIL import Image
    from matplotlib import pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
    from bs4 import BeautifulSoup
except (ModuleNotFoundError, ImportError):
    try:
        print("\nInstalling missing modules (wordcloud, PIL, matplotlib, numpy, beautifulsoup4)...\n")
        subprocess.run(["pip3", "install", "-e", "."]) # Installs all the required modules in the setup.py (wordcloud, pillow, matplotlib, numpy and beautifulsoup4)
    except:
        print("\nSome python modules were not installed automatically, please install them and run the script again.\nRequired Modules: wordcloud, PIL (or pillow), matplotlib, numpy and beautifulsoup4\n\n")

import sys
import re
import os
import random
import collections
from typing import Union


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

uninteresting_words_en = {"media", "omitted", "a", "pm", "was", "at", "her", "of", "also", "although", "with",  "is", "as", "by", "an", "the", "for", "and", "nor", "but", "or", "yet", "and", "so","on", "in", "to", "since", "for", "ago", "before", "past", "I", "me", "he", "she", "herself", "you", "it", "that", "they", "each", "few", "many", "who", "whoever", "whose", "someone", "everybody"}
uninteresting_words_es = {"multimedia", "omitido", "omitida", "message", "deleted", "mensaje", "eliminado", "dan", "tener", "cual", "ser", "esas", "debe", "hacer", "además", "ademas", "también", "v", "estaba", "podría", "puede", "voy", "anda", "tengo", "hago", "iba", "aquí", "tiene", "tienes", "misma", "cada", "solo", "pasó", "esa", "q", "vez", "ud", "esto", "tal", "ella", "allá", "dió", "soy", "queda", "va", "van", "media", "omitted", "muy", "acá", "mismo", "hiciste", "has", "estuvo", "tuyo", "ah", "da", "ti", "mis", "mi", "tus", "ay", "sus", "su", "aún", "cómo", "donde", "dónde", "vas", "cuál", "estuve", "otras", "ahí", "tuya", "estas", "hubiera", "mi", "hay", "fue","están", "he", "ha", "del", "al", "eso", "era", "ese", "esta", "son", "uno", "qué", "está", "nequi", "sí", "si", "no", "les", "es", "pm", "am", "un", "una", "unos", "unas", "el", "los", "la", "las", "lo", "le", "y", "e", "ni", "que", "pero", "mas", "más", "aunque", "sino", "siquiera", "o", "u", "otra", "sea", "ya", "este", "aquél", "aquel", "pues", "porque", "puesto", "que", "como", "así", "asi", "luego", "tan", "tanto", "conque", "a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "durante", "en" , "entre", "hacia", "hasta", "mediante", "para", "por", "según", "segun", "sin", "so", "sobre", "tras", "versus", "vía", "via", "yo", "tú", "tu", "él", "usted", "ustedes", "nosotros", "nosotras", "vosotros", "vosotras", "ellos", "ellas", "me", "te", "nos", "se"}

uninteresting_words_list = uninteresting_words_es + uninteresting_words_en

def contact_text_separator(whatsapp_chat_path: str) -> dict:
    """Generate a dictionary where the keys are the names of each contact and the values are what they said

    Parameters
    ----------
    whatsapp_chat_path : str
        Path to the .txt file that contains the whatsapp chat.

    Returns
    -------
    contact_speech_dictionary: dict(list(str))
        Dictionary where the keys are the names of each contact and the values are what they said.
    """
    contact_speech_dictionary = {}
    with open(whatsapp_chat_path, "r", encoding="utf8") as source_file:

        for line in source_file:
            matched_contact = re.match(r"^\d+\/\d+\/\d+,? \d+:\d+.*?- (.*?): (.*)\n?", line)    # Match contact name in group 1 and what they said in group 2
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
    with open(os.path.join("font", "coolors.co")) as coolors_web_source:
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

def file_finder(directory: str, file_extension: Union[str, tuple] = "") -> list:
    """Generate a list containing both the name and path of each file with the specified extension in the directory.

    Parameters
    ----------
    directory : str
        Directory where you want to get the files.
    file_extension : str or tuple(str)
        The file extension or extensions you want to include in your list, by default "" (includes all files)

    Returns
    -------
    file_names: list(str,str)
        List containing both the name and the path of each file in the specified directory.
    """

    file_names = []
    for file_name in os.listdir(directory):
        if file_name.endswith(file_extension):
            file_path = os.path.join(directory, file_name)
            file_names.append([file_name, file_path])

    return file_names

def word_counter(contact_speech: dict) -> dict:
    """Return a dictionary where each key is a contact name and each value is what they said.

    Parameters
    ----------
    contact_speech : dict(str)
        Dictionary where each key is a contact name and each value is what they said.

    Returns
    -------
    counted_words : dict(int)
        Dictionary where each key is a word and each value is the number of occurrances of the word.
    """

    words_to_count = []
    for words in contact_speech.values():
        words_to_count += words

    counted_words = collections.Counter(words_to_count)     # Returns a Counter object that contains a dictionary where each word is a key and the number of occurrences are the values

    return dict(counted_words)

def colorgroup_generator(contact_speech: dict) -> dict:
    """Return a dictionary where the keys are hex color codes and the values are a the list of the words said by each contact cleaned

    Parameters
    ----------
    contact_speech : dict(str)
        Dictionary where each key is a contact name and each value is what they said.

    Returns
    -------
    colorgroup : dict(list(str))
        Dictionary where the keys are hex color codes and the values are a the list of the words said by each contact cleaned
    """
    color_list = color_generator(contact_speech)

    colorgroup = {}
    for color_index, text in enumerate(contact_speech.values()):
        color = color_list[color_index]
        colorgroup[color] = text_cleaner(text, uninteresting_words_list)

    return colorgroup

def main():
    """ Extract the most common words used by each contact in the whatsapp chats stored in the "whatsapp chats" folder 
        and plots them in a wordcloud with an optional image mask where each person's words have a different color."""
    
    # Captures the needed file paths
    whatsapp_text_files = file_finder("whatsapp chats", ".txt")
    font_path = file_finder("font", (".otf", ".ttf"))
    image_mask_files = file_finder("image masks", (".jpg", ".jpeg"))
    
    for file_index, [_, whatsapp_text_path] in enumerate(whatsapp_text_files):
        print(f"\nProccesing chat #{file_index+1}\n")
        contact_speech_separated = contact_text_separator(whatsapp_text_path)
        colorgroup = colorgroup_generator(contact_speech_separated)
        counted_words = word_counter(colorgroup)
        

        grouped_color_func = GroupedColorFunc(colorgroup, default_color="gray")
        try:
            image_mask = np.array(Image.open(image_mask_files[file_index][1]))
        except IndexError:
            image_mask = None

        # Generates the wordcloud
        cloud = wordcloud.WordCloud(background_color="white", 
                                    mask=image_mask,
                                    max_words=200,
                                    max_font_size=None, 
                                    min_font_size=10, 
                                    width=1920, 
                                    height=1920, 
                                    font_path = font_path[0][1])

        cloud.generate_from_frequencies(counted_words)

        # Prints the image
        wordcloud_image = cloud.to_array()
        plt.figure(figsize=(10, 5))
        plt.imshow(cloud.recolor(color_func=grouped_color_func), interpolation="bilinear")
        plt.axis('off')

        # Saving images as a .jpg file
        wordcloud_file_name = ""
        contact_patches = []
        for contact_name, contact_color in zip(contact_speech_separated, colorgroup):
            if len(wordcloud_file_name) <= 20:
                wordcloud_file_name += "-"+contact_name
            contact_patches.append(mpatches.Patch(color=contact_color, label=contact_name))
        
        plt.legend(handles=contact_patches)
        plt.show(block=False)
        cloud.to_file(f"wordcloud-chat{wordcloud_file_name}-generated.jpg")
    plt.show()
    
if __name__ == "__main__":
    main()
