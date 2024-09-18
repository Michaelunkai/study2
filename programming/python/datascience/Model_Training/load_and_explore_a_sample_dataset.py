import pandas as pd  # Importing pandas for data manipulation
from sklearn.datasets import load_iris  # Loading Iris dataset from sklearn
import matplotlib.pyplot as plt  # Importing matplotlib for plotting

# Load the Iris dataset
iris = load_iris()  # Loading the Iris dataset
data = pd.DataFrame(data=iris.data, columns=iris.feature_names)  # Creating DataFrame
data['target'] = iris.target  # Adding target column

# Display basic information about the dataset
print(data.head())  # Display first 5 rows
print(data.describe())  # Display statistical summary
print(data['target'].value_counts())  # Display target value counts

# Plotting the data
pd.plotting.scatter_matrix(data.iloc[:, :-1], c=data['target'], figsize=(15, 15), marker='o', 
                           hist_kwds={'bins': 20}, s=60, alpha=.8, cmap='viridis')  # Scatter matrix plot
plt.show()  # Show plot
