from datasets import load_dataset
ds = load_dataset("squad", split="validation")
ds.to_json("squad_validation.jsonl")