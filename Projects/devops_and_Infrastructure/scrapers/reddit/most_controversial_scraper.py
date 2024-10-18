import praw
from datetime import datetime, timedelta
import pandas as pd

# Initialize the Reddit instance
reddit = praw.Reddit(
    client_id='<YOUR_CLIENT_ID>',
    client_secret='<YOUR_CLIENT_SECRET>',
    user_agent='<YOUR_USER_AGENT>'
)

# Define the time range for the last month
end_date = datetime.utcnow()
start_date = end_date - timedelta(days=30)

# Container for posts
posts_data = []

# Fetching most controversial posts
for submission in reddit.subreddit('all').controversial('month'):
    post_date = datetime.utcfromtimestamp(submission.created_utc)
    if start_date <= post_date <= end_date:
        posts_data.append({
            'title': submission.title,
            'subreddit': submission.subreddit.display_name,
            'score': submission.score,
            'num_comments': submission.num_comments,
            'url': submission.url,
            'created_utc': submission.created_utc,
            'summary': submission.selftext[:500]  # Summarize the post content (first 500 characters)
        })

# Sort posts by score (most controversial)
posts_data.sort(key=lambda x: x['score'])

# Function to print post details
def print_post(post):
    print("\033[91m" + post['title'] + "\033[0m")  # Red colored title
    print("Subreddit:", post['subreddit'])
    print("Score:", post['score'])
    print("Comments:", post['num_comments'])
    print("URL:", post['url'])
    print("Summary:", post['summary'])
    print("\033[90m" + "-" * 80 + "\033[0m")  # Fake line separator

# Print each post's details
for post in posts_data:
    print_post(post)

# Container for comments
comments_data = []

# Fetching most controversial comments from the most controversial posts
for post in posts_data:
    submission = reddit.submission(url=post['url'])
    submission.comment_sort = 'controversial'
    submission.comments.replace_more(limit=0)
    for comment in submission.comments:
        comments_data.append({
            'body': comment.body[:500],  # Summarize the comment content (first 500 characters)
            'score': comment.score,
            'created_utc': comment.created_utc,
            'post_title': post['title']
        })

# Sort comments by score (most controversial)
comments_data.sort(key=lambda x: x['score'])

# Function to print comment details
def print_comment(comment):
    print("\033[92m" + comment['body'] + "\033[0m")  # Green colored comment
    print("Score:", comment['score'])
    print("Post Title:", comment['post_title'])
    print("\033[90m" + "-" * 80 + "\033[0m")  # Fake line separator

# Print each comment's details
for comment in comments_data:
    print_comment(comment)
