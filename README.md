# Whatsapp-Wordcloud-Generator
Python script that extracts the most common words used by each contact in a whatsapp chat and plots them in a wordcloud where each person's words have a different color.

## Usage
if you want to generate your wordcloud you have to follow these steps:

1. **Download your whatsapp chats.** To download your whatsapp chats:
	1. open the chat in your phone
	2. click the three dots on the top right of the chat
	3. go to "more"
	4. click on "export chat"
	5. click on "without media" (it will generate the .txt file)

2. **Save your whatsapp chats in the folder "whatsapp chats".**

3. **[Optional]** If you want to use a personalized font (type of letter), **save the font file (.otf or .ttf) in the "font" folder** (the script will use the first font it founds in the folder ordered alphabetically)

4. **[Optional]** If you want the words to form a shape (see the examples in the "examples" folder) **save the images in .jpg format in the "image masks" folder** (the words will fit into the colored regions therefore the background has to be white). The script will use the first image to mask the first conversation, the second with the second one and so on, if there aren't enough masks it will generate standard square wordclouds.

5. **Execute the file "whatsapp_wordcloud.py"** using python 3.5+ in your favorite IDE or with any of this commands in the terminal:
	- python whatsapp_wordcloud.py
	- python3 whatsapp_wordcloud.py
	- ./whatsapp_wordcloud.py

## License
Whatsapp Wordcloud Generator is released under the MIT license. See LICENSE for details.

## Contact
Let's talk! Twitter/instagram: @anggelomos, email: anggelomos@outlook.com
