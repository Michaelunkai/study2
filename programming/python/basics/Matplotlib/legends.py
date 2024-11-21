import matplotlib.pyplot as plt

# Sample data
x = [1, 2, 3, 4, 5]
y1 = [10, 15, 13, 17, 20]
y2 = [12, 14, 11, 18, 22]

# Plot multiple lines
plt.plot(x, y1, label='Dataset 1')
plt.plot(x, y2, label='Dataset 2')

# Add legend
plt.legend()

# Display the plot
plt.show()