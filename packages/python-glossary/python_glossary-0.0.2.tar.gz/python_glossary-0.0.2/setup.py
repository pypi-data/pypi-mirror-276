import setuptools

VERSION = "0.0.2"

NAME = "python-glossary"

INSTALL_REQUIRES = [
    "requests"
]


setuptools.setup(
    name=NAME,
    version=VERSION,
    description="Python module that uses free dictionary API to retrieve definitions, examples, synonyms, antonyms, "
                "and audio of english words ",
    url="https://github.com/ilya-smut/python-glossary",
    project_urls={
        "Source Code": "https://github.com/ilya-smut/python-glossary",
    },
    author="Ilya Smut",
    author_email="ilya.smut.off.g@gmail.com",
    license="GPL-3.0 license",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",

    # Requirements
    install_requires=INSTALL_REQUIRES,
    packages=["python_glossary"],
    long_description=open("README.md", 'r', encoding='utf8').read(),
    long_description_content_type="text/markdown",
)
