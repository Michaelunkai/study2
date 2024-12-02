from datasets import load_dataset
ds = load_dataset("imdb", split="train")
ds.to_json("imdb_reviews.jsonl")