import kagglehub

# Download latest version
path = kagglehub.model_download("google/mobilenet-v2/tensorFlow2/035-128-classification")

print("Path to model files:", path)
