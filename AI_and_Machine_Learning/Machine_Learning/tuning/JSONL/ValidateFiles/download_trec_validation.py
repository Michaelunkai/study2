from datasets import load_dataset
ds = load_dataset("trec", split="test")
ds.to_json("trec_validation.jsonl")