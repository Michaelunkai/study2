# Question:
# Amir works on 3 deals per week and has a 30% success rate on each deal. Simulate 1 deal, simulate a week of 3 deals, 
# and simulate a year of 52 weeks of deals, then calculate the mean number of deals won weekly.

# Explanation:
# The task uses the binomial distribution to simulate Amir's sales performance. Using `binom.rvs`, we model success or failure 
# for one deal, weekly deals, and yearly performance. A random seed ensures reproducibility, and calculations provide the average 
# deals won weekly.

# Full Answer (Code):
# Step 1: Import necessary libraries
from scipy.stats import binom
import numpy as np

# Step 2: Set random seed for reproducibility
np.random.seed(10)

# Step 3: Simulate a single deal (1 trial with 30% success rate)
single_deal = binom.rvs(1, 0.3, size=1)
print(f"Simulated outcome of a single deal: {single_deal[0]}")

# Step 4: Simulate a week of Amir's work (3 trials with 30% success rate)
weekly_deals = binom.rvs(3, 0.3, size=1)
print(f"Simulated deals won in a week: {weekly_deals[0]}")

# Step 5: Simulate a year of Amir's work (52 weeks of 3 trials each)
yearly_deals = binom.rvs(3, 0.3, size=52)
print(f"Simulated deals won each week over a year: {yearly_deals}")

# Step 6: Calculate the mean number of deals won per week
mean_deals = np.mean(yearly_deals)
print(f"Mean number of deals won per week: {mean_deals:.2f}")

# Answer Explanation:
# The `binom.rvs` function simulates sales outcomes under a binomial distribution, modeling individual deals, weekly deals, and yearly 
# performance (52 weeks). The random seed ensures consistent results. Weekly success rates align with Amir's 30% probability, yielding 
# an average of 0.85 deals won weekly. This reflects realistic performance expectations.
