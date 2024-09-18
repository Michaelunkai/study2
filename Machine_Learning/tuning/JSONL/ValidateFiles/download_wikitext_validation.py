from datasets import load_dataset
ds = load_dataset("wikitext", "wikitext-103-v1", split="validation")
ds.to_json("wikitext_validation.jsonl")