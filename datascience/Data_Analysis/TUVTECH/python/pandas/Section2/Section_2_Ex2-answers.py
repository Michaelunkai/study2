# Install necessary dependencies
import os
os.system('pip install pandas kagglehub')

# Import libraries
import kagglehub
import pandas as pd

# Download datasets
organizations_openfoodfacts_world_food_facts_path = kagglehub.dataset_download('organizations/openfoodfacts/world-food-facts')
organizations_tovtech_pandas_exercises_path = kagglehub.dataset_download('organizations/TovTech/pandas-exercis')

# Load the dataset
file_path = '/kaggle/input/world-food-facts/en.openfoodfacts.org.products.tsv'
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
