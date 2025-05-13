import kagglehub

# Download latest version
path = kagglehub.model_download("qwen-lm/qwq-32b/transformers/qwq-32b")

print("Path to model files:", path)
