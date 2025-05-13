import kagglehub

# Download latest version
path = kagglehub.model_download("google/flan-t5/pyTorch/base")

print("Path to model files:", path)
