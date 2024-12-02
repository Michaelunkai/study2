from datasets import load_dataset
ds = load_dataset("multi_nli", split="validation_matched")
ds.to_json("multi_nli_validation.jsonl")