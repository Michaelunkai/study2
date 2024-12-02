from datasets import load_dataset
ds = load_dataset("trec", split="train")
ds.to_json("trec_data.jsonl")