from datasets import load_dataset
ds = load_dataset("imdb", split="test")
ds.to_json("imdb_reviews_validation.jsonl")