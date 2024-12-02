import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load Data
try:
    df = pd.read_csv('news_articles.csv')

    # Combine all summaries
    text = ' '.join(df['summary'].dropna())

    # Generate Word Cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # Plot Word Cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
except FileNotFoundError:
    print("The file 'news_articles.csv' was not found. Please make sure to run 'fetch_news_articles.py' first.")
