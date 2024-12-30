# Question:
# Amir usually works on 3 deals per week and has a 30% success rate on each deal. Using a binomial distribution:
# 1. Simulate 1 deal worked on by Amir.
# 2. Simulate 1 week of Amir's work (3 deals).
# 3. Simulate Amir's work for a year (52 weeks) and calculate the mean number of deals won per week.

# Explanation:
# The task models Amir's sales performance using a binomial distribution. With a 30% success rate, simulate outcomes for 1 deal, 
# 1 week's worth of deals, and a year. This helps estimate Amir's performance and average deals won weekly.

# Full Answer (Code):
# Step 1: Import necessary libraries
from scipy.stats import binom
import numpy as np

# Step 2: Set random seed for reproducibility
np.random.seed(10)

# Step 3: Define parameters
n_deals_per_week = 3  # Deals per week
p_success = 0.3       # Success probability

# Step 4: Simulate 1 deal worked on by Amir
deal_outcome = binom.rvs(1, p_success)
print(f"Simulated outcome of 1 deal: {deal_outcome}")

# Step 5: Simulate a typical week of Amir's work (3 deals)
week_outcome = binom.rvs(n_deals_per_week, p_success)
print(f"Simulated deals won in 1 week: {week_outcome}")

# Step 6: Simulate Amir's work for a year (52 weeks)
year_outcome = binom.rvs(n_deals_per_week, p_success, size=52)
print(f"Simulated deals won each week over a year: {year_outcome}")

# Step 7: Calculate the mean number of deals won per week
mean_deals_per_week = np.mean(year_outcome)
print(f"Mean number of deals won per week: {mean_deals_per_week:.2f}")

# Answer Explanation:
# The binomial distribution models Amir's sales outcomes, simulating successes for a deal, weekly performance, and yearly performance. 
# Each trial reflects a success rate of 30%. Calculating the mean deals per week (0.96) over 52 weeks demonstrates Amir's expected 
# weekly performance based on the given probabilities.
