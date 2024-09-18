from datasets import load_dataset
ds = load_dataset("xnli", split="validation")
ds.to_json("xnli_validation.jsonl")