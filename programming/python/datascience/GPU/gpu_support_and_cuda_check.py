import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

import torch
print("Is CUDA available: ", torch.cuda.is_available())
