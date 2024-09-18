from transformers import pipeline

# Load a sentiment-analysis pipeline
classifier = pipeline('sentiment-analysis')

# Test the classifier
result = classifier("I love using Hugging Face Transformers!")
print(result)
