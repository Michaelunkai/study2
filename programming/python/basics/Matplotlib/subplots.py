import matplotlib.pyplot as plt

# Sample data
x = [1, 2, 3, 4, 5]
y1 = [10, 15, 13, 17, 20]
y2 = [12, 14, 11, 18, 22]

# Create subplots
fig, axs = plt.subplots(2)

# First subplot
axs[0].plot(x, y1)
axs[0].set_title('First Plot')

# Second subplot
axs[1].plot(x, y2)
axs[1].set_title('Second Plot')

# Adjust layout
plt.tight_layout()

# Display the plots
plt.show()