# Glossary.py

Glossary.py is a Python module that interacts with an online dictionary API. It's designed to fetch and manage word descriptions, phonetics, and semantics in a structured way.

## Key Features:

- Fetches word descriptions, phonetics, and semantics from an online dictionary API.
- Implements a class-based approach for managing fetched data.
- Allows to set a limit for the number of descriptions per part of speech for a word.
- Provides audio transcription and audio file link for the fetched word.
- Allows to get all definitions or definitions based on a part of speech.

## Installation
```bash
pip install python-glossary
```

## How to Use:

```python
from python_glossary.glossary import Glossary

# Create a rule object and set a limit for descriptions
rules = Glossary.Rules()
rules.set_limit_of_descriptions(3)

# Create a word object with a specific word and rule
word = Glossary.Word('example', rules)

# Check if the word exists
if word.exists():
    # Get transcription
    print(word.get_transcription())
    # Get audio link
    print(word.get_audio())
    # Get all definitions
    print(word.get_all_definitions())
    # Get definitions for a specific part of speech
    print(word.get_definitions_of_part_of_speech('noun'))

```

## Requirements:

- Python 3.8+
- requests 

Please note, this module relies on the API at `https://api.dictionaryapi.dev/api/v2/entries/en/{input_word}` for fetching word data. Ensure you have a stable internet connection while using this module.
