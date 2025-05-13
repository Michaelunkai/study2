import kagglehub

# Download latest version
path = kagglehub.model_download("metaresearch/segment-anything/pyTorch/vit-b")

print("Path to model files:", path)
