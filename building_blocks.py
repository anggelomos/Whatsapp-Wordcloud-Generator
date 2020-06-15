import re
import collections
import timeit

# Reading the text file
source_file = open("demo.txt", "r")
raw_text = source_file.read()

lower_cased_text = raw_text.lower()

splitted_text = raw_text.split()    # Here we crerate a list with the words that are separated by a space

sorted_text = sorted(splitted_text)

# Here we delete the punctuation symbols of each word using the re.sub() function

punctuation_symbols = ["'", ":", ",", "--", "_", "\...", "¡", "!", "\.", "-", "(", ")", "¿", "\?", "\"", "\;"] # Some of the symbols have a backslash (\) before because they caused an error with the re.sub() function without it

for word in splitted_text:
    if word.isalpha():
        pass
    else:
        cleaned_word = re.sub("|".join(punctuation_symbols), "", word)
    
    
# Here we delete unwanted elements from a list using list comprehensions

uninteresting_words = {"a", "is","as", "by", "an", "the", "for", "and", "nor", "but", "or", "yet", "and", "so","on", "in", "to", "since", "for", "ago", "before", "past", "I", "me", "he", "she", "herself", "you", "it", "that", "they", "each", "few", "many", "who", "whoever", "whose", "someone", "everybody"} # The uninteresting words are: articles, conjunctions, prepositions and pronouns. 

cleaned_text = [element for element in splitted_text if element not in uninteresting_words]


counter = collections.Counter(sorted_text)

print(dict(counter))


################################# Test 01: re.sub() vs list comprehensions ######################################################

# In this test we want to know which tecnique performs better to delete unninteresting words

setup_code= '''

import re
uninteresting_words = {"a", "an", "the", "for", "and", "nor", "but", "or", "yet", "and", "so","on", "in", "to", "since", "for", "ago", "before", "past", "I", "me", "he", "she", "herself", "you", "it", "that", "they", "each", "few", "many", "who", "whoever", "whose", "someone", "everybody"} # The uninteresting words are: articles, conjunctions, prepositions and pronouns. 

# Reading the text file
source_file = open("demo.txt", "r")
raw_text = source_file.read()

splitted_text = raw_text.split()    # Here we crerate a list with the words that are separated by a space

'''

test_re_sub = '''

tested_text = []
for word in splitted_text:
    tested_text.append(re.sub("|".join(uninteresting_words), "", word))

'''

test_list_compr = '''

tested_text = [word for word in splitted_text if word not in uninteresting_words]

'''

# time_re_sub = timeit.timeit(test_re_sub, setup_code, number=1000)
# time_list_compr = timeit.timeit(test_list_compr, setup_code, number=1000)

# print("sub.re() time: {}\tlist comprehension time: {}".format(time_re_sub, time_list_compr))

# These are the results:
#
# sub.re() time: 3.6447984        list comprehension time: 0.04235330000000026
#
# We declase list comprehensions THE ABSOLUTE WINEER!!!!

###################################################################################################################################