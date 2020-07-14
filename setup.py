from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name="whatsapp-wordlcloud-generator",
    version="1.1.0",
    description="Creates a wordcloud with the most used words in a whatsapp conversation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Angelo Mosquera",
    license="MIT",
    keywords="whatsapp wordcloud generator",
    packages=find_packages(),
    install_requires=["wordcloud", "PIL", "matplotlib", "numpy"],
    python_requires="~=3.5"
)