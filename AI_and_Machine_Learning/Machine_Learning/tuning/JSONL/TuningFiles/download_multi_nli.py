from datasets import load_dataset
ds = load_dataset("multi_nli", split="train")
ds.to_json("multi_nli.jsonl")