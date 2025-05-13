import kagglehub

# Download latest version
path = kagglehub.model_download("keras/gemma3/keras/gemma3_12b")

print("Path to model files:", path)
