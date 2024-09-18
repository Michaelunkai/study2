from datasets import load_dataset
ds = load_dataset("xnli", split="train")
ds.to_json("xnli.jsonl")