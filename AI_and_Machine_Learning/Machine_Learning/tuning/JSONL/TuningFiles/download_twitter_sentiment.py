from datasets import load_dataset
ds = load_dataset("tweet_eval", "sentiment", split="train")
ds.to_json("twitter_sentiment.jsonl")