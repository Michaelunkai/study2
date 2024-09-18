from datasets import load_dataset
ds = load_dataset("ag_news", split="train")
ds.to_json("ag_news.jsonl")