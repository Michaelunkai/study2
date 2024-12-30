# Question:
# The backup tool automatically backs up every 30 minutes. Using a continuous uniform distribution,
# calculate:
# 1. Probability Amir has to wait less than 5 minutes.
# 2. Probability Amir has to wait more than 5 minutes.
# 3. Probability Amir has to wait between 10 and 20 minutes.

# Explanation:
# This problem involves a continuous uniform distribution since backups occur every 30 minutes, 
# and the exact backup time is uniformly distributed between 0 and 30 minutes. We calculate probabilities 
# using the uniform distribution's cumulative distribution function (CDF).

# Full Answer:
# Min and max wait times for backup that happens every 30 minutes
min_time = 0
max_time = 30

# Import uniform from scipy.stats
from scipy.stats import uniform

# Calculate the probability Amir has to wait less than 5 minutes
prob_less_than_5 = uniform.cdf(5, loc=min_time, scale=max_time - min_time)
print(f"Probability Amir has to wait less than 5 minutes: {prob_less_than_5}")

# Calculate the probability Amir has to wait more than 5 minutes
prob_greater_than_5 = 1 - prob_less_than_5
print(f"Probability Amir has to wait more than 5 minutes: {prob_greater_than_5}")

# Calculate the probability Amir has to wait between 10 and 20 minutes
prob_between_10_and_20 = uniform.cdf(20, loc=min_time, scale=max_time - min_time) - uniform.cdf(10, loc=min_time, scale=max_time - min_time)
print(f"Probability Amir has to wait between 10 and 20 minutes: {prob_between_10_and_20}")

# Answer Explanation:
# The uniform distribution has equal probability over an interval [0, 30].
# The CDF calculates probabilities for specific ranges:
# - Wait < 5 mins: 0.1667
# - Wait > 5 mins: 0.8333 (1 - CDF at 5 mins)
# - Wait 10–20 mins: 0.3333 (CDF difference from 10 to 20 mins)
