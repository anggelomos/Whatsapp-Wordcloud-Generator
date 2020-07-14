from setuptools import setup, find_packages

setup(
    name="whatsapp-wordlcloud-generator",
    version="1.1.0",
    description="Creates a wordcloud with the most used words in a whatsapp conversation",
    author="Angelo Mosquera",
    license="MIT",
    keywords="whatsapp wordcloud generator",
    packages=find_packages(),
    install_requires=["wordcloud", "PIL", "matplotlib", "numpy"],
    python_requires="~=3.5"
)