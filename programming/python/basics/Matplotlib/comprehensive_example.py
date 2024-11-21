import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Load Data
data = pd.read_csv('students_scores.csv')

# Preview data
print(data.head())

# Step 2: Plot Data
plt.scatter(data['Hours_Studied'], data['Test_Score'])

# Add title and labels
plt.title('Test Score vs. Hours Studied')
plt.xlabel('Hours Studied')
plt.ylabel('Test Score')

# Display the plot
plt.show()

# Step 3: Add a Trend Line
# Calculate the trend line
z = np.polyfit(data['Hours_Studied'], data['Test_Score'], 1)
p = np.poly1d(z)

# Plot the scatter plot
plt.scatter(data['Hours_Studied'], data['Test_Score'])

# Plot the trend line
plt.plot(data['Hours_Studied'], p(data['Hours_Studied']), 'r--')

# Add title and labels
plt.title('Test Score vs. Hours Studied with Trend Line')
plt.xlabel('Hours Studied')
plt.ylabel('Test Score')

# Display the plot
plt.show()