import matplotlib.pyplot as plt
import numpy as np

# Sample data
data = np.random.rand(10, 10)

# Create a heatmap
plt.imshow(data, cmap='hot', interpolation='nearest')

# Add a colorbar
plt.colorbar()

# Display the plot
plt.show()