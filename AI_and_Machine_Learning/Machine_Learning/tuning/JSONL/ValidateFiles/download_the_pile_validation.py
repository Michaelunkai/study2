from datasets import load_dataset
ds = load_dataset("the_pile", split="validation")
ds.to_json("the_pile_validation.jsonl")