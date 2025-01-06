# %% [markdown]
# # Comprehensive Academic-Style Tutorial on Iris Dataset Analysis using Python, Pandas, Seaborn, and Matplotlib
#
# This notebook covers:
# - Data Import and Preparation with Pandas
# - Data Manipulation and Transformation Techniques
# - Data Visualization with Seaborn and Matplotlib
# - Data Aggregation and Descriptive Statistics
#
# Tools and Libraries:
# - Python
# - Pandas
# - Seaborn
# - Matplotlib

# %% [code]
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the Iris dataset
iris = sns.load_dataset('iris')

# 1. Data Preparation (25 points)
# a. Examine the first and last 5 rows of the dataset.
first_five = iris.head(5)
last_five = iris.tail(5)

# b. Check the data types of each column.
dtypes = iris.dtypes

# c. Rename the columns to more descriptive names.
iris = iris.rename(columns={
    'sepal_length': 'Sepal_Length_cm',
    'sepal_width': 'Sepal_Width_cm',
    'petal_length': 'Petal_Length_cm',
    'petal_width': 'Petal_Width_cm',
    'species': 'Species'
})

# d. Create a new column "sepal_area" which is product of sepal length and width.
iris['Sepal_Area_cm2'] = iris['Sepal_Length_cm'] * iris['Sepal_Width_cm']

# e. Create a new column "petal_area" which is product of petal length and width.
iris['Petal_Area_cm2'] = iris['Petal_Length_cm'] * iris['Petal_Width_cm']

# 2. Data Manipulation (25 points)
# a. Sort dataset by sepal length in descending order.
iris_sorted = iris.sort_values(by='Sepal_Length_cm', ascending=False)

# b. Filter dataset to include rows where sepal width > 3.0
iris_filtered = iris[iris['Sepal_Width_cm'] > 3.0]

# c. Group by species and calculate mean of each numeric column.
iris_grouped_mean = iris.groupby('Species').mean(numeric_only=True)

# d. Pivot dataset with species as columns and sepal length/width as rows.
iris_pivot = iris.pivot_table(index=['Sepal_Length_cm', 'Sepal_Width_cm'], columns='Species', values='Petal_Length_cm', aggfunc='mean')

# e. Melt pivoted DataFrame to create long format DataFrame.
iris_melted = iris_pivot.reset_index().melt(id_vars=['Sepal_Length_cm', 'Sepal_Width_cm'], var_name='Species', value_name='Mean_Petal_Length')

# 3. Data Visualization (25 points)
# a. Histogram of sepal length.
plt.figure(figsize=(6,4))
plt.hist(iris['Sepal_Length_cm'], bins=10, color='skyblue', edgecolor='black')
plt.title('Histogram of Sepal Length')
plt.xlabel('Sepal Length (cm)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig("histogram_sepal_length.png")
plt.close()

# b. Scatterplot of sepal length vs sepal width, colored by species.
plt.figure(figsize=(6,4))
sns.scatterplot(data=iris, x='Sepal_Length_cm', y='Sepal_Width_cm', hue='Species', palette='viridis')
plt.title('Sepal Length vs Sepal Width by Species')
plt.xlabel('Sepal Length (cm)')
plt.ylabel('Sepal Width (cm)')
plt.tight_layout()
plt.savefig("scatter_sepal_length_width_by_species.png")
plt.close()

# c. Boxplot of petal length by species.
plt.figure(figsize=(6,4))
sns.boxplot(data=iris, x='Species', y='Petal_Length_cm', palette='pastel')
plt.title('Petal Length Distribution by Species')
plt.xlabel('Species')
plt.ylabel('Petal Length (cm)')
plt.tight_layout()
plt.savefig("boxplot_petal_length_by_species.png")
plt.close()

# d. Pairplot of the dataset, colored by species.
pairplot_fig = sns.pairplot(iris, hue='Species', diag_kind='hist', palette='Set2')
pairplot_fig.savefig("pairplot_iris.png")
plt.close()

# e. Heatmap of the correlation matrix.
corr = iris[['Sepal_Length_cm','Sepal_Width_cm','Petal_Length_cm','Petal_Width_cm','Sepal_Area_cm2','Petal_Area_cm2']].corr()
plt.figure(figsize=(6,4))
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix of Iris Measurements')
plt.tight_layout()
plt.savefig("heatmap_correlation_matrix.png")
plt.close()

# 4. Data Aggregation (25 points)
# a. Total sepal area and petal area for each species.
species_area_sum = iris.groupby('Species')[['Sepal_Area_cm2','Petal_Area_cm2']].sum()

# b. Max and min values for each numeric column by species.
species_max = iris.groupby('Species').max(numeric_only=True)
species_min = iris.groupby('Species').min(numeric_only=True)

# c. Mean and median values for each numeric column by species.
species_mean = iris.groupby('Species').mean(numeric_only=True)
species_median = iris.groupby('Species').median(numeric_only=True)

# d. Count number of observations for each species.
species_count = iris['Species'].value_counts()

# e. Calculate 25th, 50th, and 75th percentiles for each numeric column by species.
percentiles = iris.groupby('Species').quantile([0.25,0.50,0.75], numeric_only=True)

# End of Notebook

