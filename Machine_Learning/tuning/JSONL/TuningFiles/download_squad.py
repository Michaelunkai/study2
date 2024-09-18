from datasets import load_dataset
ds = load_dataset("squad", split="train")
ds.to_json("squad_data.jsonl")