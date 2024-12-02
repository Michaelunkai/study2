from datasets import load_dataset
ds = load_dataset("tweet_eval", "sentiment", split="test")
ds.to_json("twitter_sentiment_validation.jsonl")