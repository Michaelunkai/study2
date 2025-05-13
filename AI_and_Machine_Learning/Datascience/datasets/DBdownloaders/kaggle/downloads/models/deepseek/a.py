import kagglehub

# Download latest version
path = kagglehub.model_download("deepseek-ai/deepseek-r1/transformers/deepseek-r1")

print("Path to model files:", path)
