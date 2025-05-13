import kagglehub

# Download latest version
path = kagglehub.model_download("jiazhuang/sac-logos-ava1-l14-linearmse/transformers/default")

print("Path to model files:", path)
