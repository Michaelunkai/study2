import praw
from datetime import datetime, timedelta, timezone
from colorama import Fore, Style, init

# Initialize colorama
init()

# Reddit API credentials
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
user_agent = 'YOUR_USER_AGENT'

# Initialize Reddit API client
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

# Define the search parameters
search_query = 'Israel'
time_filter = 'day'
time_threshold = datetime.now(timezone.utc) - timedelta(days=2)

# Function to get subreddit posts
def get_reddit_posts(subreddit_name, search_query, time_threshold):
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.search(search_query, time_filter=time_filter)
    
    post_list = []
    for post in posts:
        post_time = datetime.fromtimestamp(post.created_utc, timezone.utc)
        if post_time > time_threshold:
            post_data = {
                'title': post.title,
                'subreddit': subreddit_name,
                'url': post.url,
                'score': post.score,
                'num_comments': post.num_comments,
                'created_utc': post_time.strftime('%Y-%m-%d %H:%M:%S')
            }
            post_list.append(post_data)
    
    return post_list

# List of popular subreddits for news
subreddits = ['worldnews', 'news', 'Israel', 'MiddleEastNews']

# Aggregate posts from all subreddits
all_posts = []
for subreddit in subreddits:
    posts = get_reddit_posts(subreddit, search_query, time_threshold)
    all_posts.extend(posts)

# Sort posts by score in descending order (most popular to least popular)
all_posts.sort(key=lambda x: x['score'], reverse=True)

# Display the data in a readable way
for post in all_posts:
    print(Fore.RED + f"Title: {post['title']}")
    print(Style.RESET_ALL + f"Subreddit: {post['subreddit']}")
    print(Style.RESET_ALL + f"URL: {post['url']}")
    print(Fore.GREEN + f"Score: {post['score']} | Comments: {post['num_comments']} | Date: {post['created_utc']}")
    print(Style.RESET_ALL + '-'*80)

print(f'\nScraped {len(all_posts)} posts about Israel from the last 48 hours.')
