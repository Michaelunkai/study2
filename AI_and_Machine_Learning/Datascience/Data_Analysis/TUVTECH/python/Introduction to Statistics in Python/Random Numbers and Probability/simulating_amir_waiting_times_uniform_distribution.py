# Task: Simulating Amir's waiting time and creating a histogram

# Step 1: Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Step 2: Set the random seed for reproducibility
np.random.seed(334)

# Step 3: Define the minimum and maximum wait times
min_time = 0
max_time = 30

# Step 4: Simulate 1000 waiting times using a uniform distribution
waiting_times = np.random.uniform(min_time, max_time, 1000)

# Step 5: Create a histogram of the simulated waiting times
plt.hist(waiting_times, bins=15, edgecolor='black', color='skyblue')
plt.title('Simulated Waiting Times for Amir')
plt.xlabel('Waiting Time (minutes)')
plt.ylabel('Frequency')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
