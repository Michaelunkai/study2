import kagglehub

# Download latest version
path = kagglehub.model_download("keras/gemma2/keras/gemma2_instruct_27b_en")

print("Path to model files:", path)
