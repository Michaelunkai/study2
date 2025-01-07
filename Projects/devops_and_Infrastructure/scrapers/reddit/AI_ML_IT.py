import praw
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from colorama import Fore, Style, init
import time

# Initialize colorama
init(autoreset=True)

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Reddit API credentials
client_id = '<>'
client_secret = '<>'
user_agent = '<>'

# Initialize Reddit instance
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

def summarize_text(text, min_words=200):
    stop_words = set(stopwords.words("english"))
    sentences = sent_tokenize(text)
    
    word_frequencies = {}
    for sentence in sentences:
        words = word_tokenize(sentence.lower())
        for word in words:
            if word not in stop_words:
                word_frequencies[word] = word_frequencies.get(word, 0) + 1
    
    sentence_scores = {}
    for sentence in sentences:
        words = word_tokenize(sentence.lower())
        for word in words:
            if word in word_frequencies:
                sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_frequencies[word]
    
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    
    summary = []
    word_count = 0
    for sentence in summary_sentences:
        summary.append(sentence)
        word_count += len(word_tokenize(sentence))
        if word_count >= min_words:
            break
    
    return ' '.join(summary)

def is_tutorial_or_article(title, url):
    keywords = ['tutorial', 'guide', 'how to', 'article', 'learn', 'introduction', 'beginner']
    return any(keyword in title.lower() for keyword in keywords) or 'blog' in url or 'article' in url

def get_ai_ml_it_posts(subreddit, limit=100):
    posts = []
    for post in reddit.subreddit(subreddit).hot(limit=limit):
        if is_tutorial_or_article(post.title, post.url):
            posts.append(post)
    return posts

def print_separator(char='=', length=80):
    print(char * length)

def main():
    subreddits = ['artificial', 'MachineLearning', 'programming', 'compsci', 'learnprogramming', 'coding']
    all_posts = []

    print(f"{Fore.YELLOW}Searching for AI, ML, and IT Tutorials and Articles{Style.RESET_ALL}")
    print_separator()

    for subreddit in subreddits:
        print(f"Searching in r/{subreddit}...")
        all_posts.extend(get_ai_ml_it_posts(subreddit))
        time.sleep(2)  # To avoid hitting Reddit's rate limit

    all_posts.sort(key=lambda x: x.score, reverse=True)

    for i, post in enumerate(all_posts[:50], 1):  # Limit to top 50 posts
        print(f"\n{i}. {Fore.RED}{post.title}{Style.RESET_ALL}")
        print(f"   {Fore.BLUE}Subreddit: r/{post.subreddit.display_name}{Style.RESET_ALL}")
        print(f"   Score: {post.score}")
        print(f"   URL: {post.url}")
        print("   Summary:")
        try:
            response = requests.get(post.url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            article_text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
            summary = summarize_text(article_text, min_words=200)
            print(f"{Fore.GREEN}{summary}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}   Error summarizing post: {str(e)}{Style.RESET_ALL}")
        print_separator('-')
        time.sleep(1)  # To avoid hitting websites' rate limits

if __name__ == "__main__":
    main()
