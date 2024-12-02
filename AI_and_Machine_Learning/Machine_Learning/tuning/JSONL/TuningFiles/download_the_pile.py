from datasets import load_dataset
ds = load_dataset("the_pile", split="train")
ds.to_json("the_pile.jsonl")