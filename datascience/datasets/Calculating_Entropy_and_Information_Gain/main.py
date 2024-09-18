import pandas as pd
import numpy as np
from math import log2

# Load dataset
data = pd.read_csv('play_tennis.csv')

def entropy(target_col):
    elements, counts = np.unique(target_col, return_counts=True)
    entropy = np.sum([(-counts[i]/np.sum(counts)) * log2(counts[i]/np.sum(counts)) for i in range(len(elements))])
    return entropy

def info_gain(data, split_attribute_name, target_name="PlayTennis"):
    total_entropy = entropy(data[target_name])
    vals, counts = np.unique(data[split_attribute_name], return_counts=True)
    
    weighted_entropy = np.sum([(counts[i]/np.sum(counts)) * entropy(data.where(data[split_attribute_name] == vals[i]).dropna()[target_name]) for i in range(len(vals))])
    Information_Gain = total_entropy - weighted_entropy
    return Information_Gain

print("Entropy of PlayTennis:", entropy(data['PlayTennis']))

for col in data.columns[:-1]:
    print(f'Information Gain for {col}: {info_gain(data, col)}')
