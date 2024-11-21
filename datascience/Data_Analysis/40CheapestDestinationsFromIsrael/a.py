import matplotlib.pyplot as plt
import numpy as np

# Data for 40 destinations
destinations = [
    "Athens", "Larnaca", "Budapest", "Bucharest", "Krakow", "Sofia", "Istanbul", "Tbilisi",
    "Prague", "Rome", "Belgrade", "Warsaw", "Vilnius", "Zagreb", "Riga", "Valencia", "Naples",
    "Lisbon", "Barcelona", "Madrid", "Bratislava", "Vienna", "Malta", "Helsinki", "Tallinn",
    "Ljubljana", "Oslo", "Stockholm", "Copenhagen", "Amsterdam", "Berlin", "Munich", "Zurich",
    "Geneva", "Paris", "Nice", "Milan", "Venice", "Florence", "London"
]
flights = [
    313, 500, 558, 540, 600, 550, 700, 650, 688, 553, 450, 620, 640, 580, 600, 750, 720,
    800, 850, 900, 480, 780, 700, 880, 660, 590, 870, 950, 980, 1050, 700, 730, 760, 780,
    890, 910, 920, 940, 950, 1000
]
accommodation = [
    150, 200, 180, 160, 170, 150, 180, 160, 200, 220, 140, 210, 200, 180, 190, 230, 210,
    240, 250, 270, 180, 220, 190, 260, 210, 185, 270, 300, 320, 350, 240, 250, 280, 300,
    310, 320, 330, 340, 350, 360
]
food = [
    100, 120, 110, 100, 90, 80, 100, 90, 110, 120, 95, 130, 120, 100, 110, 140, 135,
    150, 160, 170, 110, 140, 120, 180, 125, 115, 175, 190, 200, 220, 150, 155, 160, 165,
    170, 180, 185, 190, 195, 200
]
transport = [
    20, 30, 25, 20, 15, 20, 25, 20, 30, 35, 18, 32, 28, 25, 22, 40, 35, 42, 45, 50,
    28, 38, 30, 48, 34, 26, 50, 55, 60, 65, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85
]

# Calculate total cost per destination
total_cost = np.array(flights) + np.array(accommodation) * 3 + np.array(food) * 3 + np.array(transport) * 3

# Create bar graph
x = np.arange(len(destinations))
width = 0.2

fig, ax = plt.subplots(figsize=(20, 12))
ax.bar(x - width * 1.5, flights, width, label="Flights")
ax.bar(x - width / 2, np.array(accommodation) * 3, width, label="Accommodation (3 nights)")
ax.bar(x + width / 2, np.array(food) * 3, width, label="Food (3 days)")
ax.bar(x + width * 1.5, np.array(transport) * 3, width, label="Transport (3 days)")

# Set labels and title
ax.set_xlabel("Destinations")
ax.set_ylabel("Cost (₪)")
ax.set_title("Estimated Travel Costs from Israel for 3-Day Trips to 40 Destinations")
ax.set_xticks(x)
ax.set_xticklabels(destinations, rotation=45, ha="right")
ax.legend()

# Show the graph
plt.tight_layout()
plt.show()
