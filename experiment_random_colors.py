import random
from bs4 import BeautifulSoup

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

print(color_generator({'contact_01': "text",
                       'contact_02': "text",
                       'contact_03': "text",
                       'contact_04': "text"}))