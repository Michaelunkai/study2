from datasets import load_dataset
ds = load_dataset("ag_news", split="test")
ds.to_json("ag_news_validation.jsonl")