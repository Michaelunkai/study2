from datasets import load_dataset
ds = load_dataset("mozilla-foundation/common_voice_11_0", "en", split="test")
ds.to_json("common_voice_validation.jsonl")