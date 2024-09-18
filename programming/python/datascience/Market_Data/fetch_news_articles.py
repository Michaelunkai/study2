from newspaper import Article
import pandas as pd

# List of news URLs
urls = [
    'https://www.cnbc.com/2023/08/05/tech-stocks-lead-market-rebound.html',
    'https://www.bbc.com/news/business-57934512'
]

articles = []

for url in urls:
    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        
        articles.append({
            'title': article.title,
            'authors': article.authors,
            'publish_date': article.publish_date,
            'summary': article.summary,
            'text': article.text,
            'url': url
        })
    except Exception as e:
        print(f"Failed to process {url}: {e}")

# Convert to DataFrame
df = pd.DataFrame(articles)

# Save to CSV
df.to_csv('news_articles.csv', index=False)
