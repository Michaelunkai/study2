from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    return scores

if __name__ == "__main__":
    text = input("Enter text to analyze: ")
    scores = analyze_sentiment(text)
    print(f"Sentiment Scores: {scores}")
