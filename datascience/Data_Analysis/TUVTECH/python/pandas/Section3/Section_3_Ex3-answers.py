# Install necessary dependencies
import os
os.system('pip install pandas kagglehub')

# Set up Kaggle API credentials
os.environ['KAGGLE_USERNAME'] = 'your_kaggle_username'
os.environ['KAGGLE_KEY'] = 'your_kaggle_api_key'

# Authenticate Kaggle API
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate()

# Download and unzip dataset
api.dataset_download_files('openfoodfacts/world-food-facts', path='datasets', unzip=True)

# Import libraries
import pandas as pd

# Load the dataset
file_path = './datasets/en.openfoodfacts.org.products.tsv'
food = pd.read_csv(file_path, sep='\t', low_memory=False)

# Step 2: See the first 5 entries
print(food.head())

# Step 3: What is the number of observations in the dataset?
print(len(food))

# Step 4: What is the number of columns in the dataset?
print(food.shape[1])

# Step 5: Print the name of all the columns
print(food.columns.tolist())

# Step 6: What is the name of the 105th column?
print(food.columns[104])

# Step 7: What is the type of the observations of the 105th column?
print(food.dtypes[104])

# Step 8: How is the dataset indexed?
print(food.index)

# Step 9: What is the product name of the 19th observation?
print(food.iloc[18]['product_name'])
