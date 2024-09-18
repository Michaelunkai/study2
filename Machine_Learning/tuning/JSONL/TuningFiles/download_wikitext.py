from datasets import load_dataset
ds = load_dataset("wikitext", "wikitext-103-v1", split="train")
ds.to_json("wikitext.jsonl")