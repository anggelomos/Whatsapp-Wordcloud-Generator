import re

def contact_text_separator(whatsapp_chat_path: str) -> dict:
    """Generate a dictionary where the keys are the names of each contact and the values are what they said

    Parameters
    ----------
    whatsapp_chat_path : str
        Path to the .txt file that contains the whatsapp chat.

    Returns
    -------
    contact_speech_dictionary: dict
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

#"test files\\testfile_01.txt"
#"whatsapp chats\\demo.txt"
contact_dict = contact_text_separator("test files\\testfile_01.txt")

print(contact_dict)

#for contact_name, contact_speech in contact_dict.items():
#   print(f"{contact_name} = {len(contact_speech)}\n{contact_speech}\n\n")