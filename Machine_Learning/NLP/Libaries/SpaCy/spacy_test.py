import spacy

# Load the language model
nlp = spacy.load("en_core_web_sm")

# Process a text
doc = nlp("SpaCy is an amazing library for NLP tasks.")

# Print the tokens and their parts of speech
for token in doc:
    print(f"{token.text} - {token.pos_}")
