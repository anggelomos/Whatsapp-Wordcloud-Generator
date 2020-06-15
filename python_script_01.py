import re
from PIL import Image
import collections
import wordcloud
from matplotlib import pyplot as plt
import numpy as np

def text_cleaner(text, uninteresting_words={"a", "was", "at", "her", "of", "also", "although", "with",  "is", "as", "by", "an", "the", "for", "and", "nor", "but", "or", "yet", "and", "so","on", "in", "to", "since", "for", "ago", "before", "past", "I", "me", "he", "she", "herself", "you", "it", "that", "they", "each", "few", "many", "who", "whoever", "whose", "someone", "everybody"} # The uninteresting words are: articles, conjunctions, prepositions and pronouns. 
):
    lower_cased_text = text.lower()

    splitted_text = lower_cased_text.split()    # Here we crerate a list with the words that are separated by a space

    splitted_text = sorted(splitted_text)

    # Here we delete the punctuation symbols of each word using the re.sub() function

    punctuation_symbols = ["'", ":", ",", "--", "_", "\...", "¡", "!", "\.", "-", "(", ")", "¿", "\?", "\"", "\;"] # Some of the symbols have a backslash (\) before because they caused an error with the re.sub() function without it

    cleaned_text = []

    for word in splitted_text:
        if word.isalpha():
            cleaned_text.append(word)
        else:
            cleaned_word = re.sub("|".join(punctuation_symbols), "", word)
            
            # after cleaning the word we check if it actually got cleaned if it didn't it gets discarted
            if cleaned_word.isalpha():
                cleaned_text.append(cleaned_word)


    # Here we delete unwanted elements from a list using list comprehensions

    final_text = [element for element in cleaned_text if element not in uninteresting_words]

    return final_text

def word_counter(words_to_count):
    counter = collections.Counter(words_to_count)
    return dict(counter)

# Reading the text file
source_file = open("demo.txt", "r")
raw_text = source_file.read()

clean_text = text_cleaner(raw_text)

counted_words = word_counter(clean_text)

maya_coloring = np.array(Image.open("F:/Coding/IT Automation Specialization - Coursera/Python Crash Course/Final project - wordcloud feeder/Wordcloud-feeder/image masks/maya.jpg"))

cloud = wordcloud.WordCloud(background_color="white", mask=maya_coloring, width=1920, height=1920, font_path="F:/Coding/IT Automation Specialization - Coursera/Python Crash Course/Final project - wordcloud feeder/Wordcloud-feeder/fonts/minimal.otf")
cloud.generate_from_frequencies(counted_words)

image_colors = wordcloud.ImageColorGenerator(maya_coloring)

myimage = cloud.to_array()
plt.imshow(myimage, interpolation = 'bilinear')
plt.imshow(cloud.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis('off')
plt.show()
