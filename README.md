# Whatsapp-Wordcloud-Generator
Python script that extracts the most common words used by each contact in a a whatsapp chat and plots them in a wordcloud where each person's words have a different color.

## Usage
if you want to generate your wordcloud you have to follow this steps:

1. Download your whatsapp conversations and store them in the folder "whatsapp chats" to download your whatsapp conversation:
- open the conversation in your phone
- click the three dots on the top right of the chat
- go to "more"
- click on "export chat"
- click on "without media" (it will generate the .txt file)

2. If you want to use a personalized font, store it in the "font" folder, it can be an .otf or .ttf file (the script will use the first font it founds in the folder ordered alphabetically)

3. If you want to fit the words to an image, store the images in the "image masks" folder (the words will fit into the colored regions therefore the background has to be white), the script will use the first image to mask the first conversation, the second with the second one and so on, if there aren't enough masks it will generate standard square wordclouds.

4. Execute the file whatsapp_wordcloud.py
('python whatsapp_wordcloud.py' or 'python3 whatsapp_wordcloud.py' or './whatsapp_wordcloud.py')

## License
Whatsapp Wordcloud Generator is released under the MIT license. See LICENSE for details.

## Contact
Let's talk! Twitter/instagram: @anggelomos, email: anggelomos@outlook.com
