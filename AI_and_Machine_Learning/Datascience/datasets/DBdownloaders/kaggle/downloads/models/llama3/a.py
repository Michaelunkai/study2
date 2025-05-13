import kagglehub

# Download latest version
path = kagglehub.model_download("metaresearch/llama-3/pyTorch/70b")

print("Path to model files:", path)
