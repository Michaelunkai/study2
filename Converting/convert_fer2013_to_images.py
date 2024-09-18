import pandas as pd
import numpy as np
import os
from PIL import Image

def convert_fer2013_to_images( _path, output_dir):
    df = pd.read_ ( _path)
    emotions = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for index, row in df.iterrows():
        emotion = emotions[row['emotion']]
        pixels = np.array(row['pixels'].split(' '), dtype=int).reshape(48, 48)
        img = Image.fromarray(pixels.astype('uint8'))
        img_path = os.path.join(output_dir, f"{emotion}_{index}.jpg")
        img.save(img_path)

 _path = '/root/fer2013/fer2013. '
output_dir = '/root/fer2013/images'
convert_fer2013_to_images( _path, output_dir)
