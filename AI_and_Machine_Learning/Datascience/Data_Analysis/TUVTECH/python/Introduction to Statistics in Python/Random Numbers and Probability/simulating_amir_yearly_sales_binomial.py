# Question:
# Amir works on 3 deals per week, with a 30% success rate for each deal. Simulate a year (52 weeks) of Amir's work, 
# calculate the mean number of deals won per week, and print the results.

# Explanation:
# Using the binomial distribution, simulate 52 weeks of Amir's sales performance with 3 deals per week and a 30% success rate. 
# The task calculates the average deals won weekly based on the simulated yearly data to estimate his performance.

# Full Answer (Code):
# Import binom from scipy.stats
from scipy.stats import binom
import numpy as np

# Set random seed to 10
np.random.seed(10)

# Simulate 52 weeks of 3 deals
deals = binom.rvs(3, 0.3, size=52)

# Print mean deals won per week
print(f"Simulated deals won each week over a year: {deals}")
print(f"Mean number of deals won per week: {np.mean(deals):.2f}")
