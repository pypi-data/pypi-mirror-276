import pathlib
from setuptools import setup, find_packages

# Directory containing the README file
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="emotion_analysis",
    version="0.1.6",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "beautifulsoup4",
        "emoji",
        "nltk",
        "wordcloud",
        "matplotlib",
        "seaborn",
        "transformers",
        "torch",
    ],
    author="Ahsan Tariq",
    author_email="ahsantariq0724@email.com",
    description="A package for emotion detection using transformers-based models.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ahsantariq7/emotion_analysis",
    license="MIT",
    keywords="emotion analysis transformers machine learning,engr_ahsan_tariq_0724,bert_vector,roberta_vector,nlp,text emotion analysis,emotion analysis",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
)
