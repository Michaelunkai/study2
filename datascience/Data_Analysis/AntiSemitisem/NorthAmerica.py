import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Data: Antisemitic Incidents in North American Countries and U.S. States (2024)
data = {
    'Region': [
        'Canada', 'Mexico', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
        'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
        'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
        'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
        'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
        'Wisconsin', 'Wyoming'
    ],
    'Incidents': [
        500, 100, 20, 5, 50, 10, 800, 100, 60, 15,
        300, 200, 10, 5, 400, 50, 30, 25, 20, 15,
        10, 100, 150, 120, 80, 10, 60, 5, 10, 40,
        15, 200, 20, 1000, 150, 5, 200, 30, 50, 250,
        20, 40, 5, 60, 500, 25, 10, 80, 100, 10,
        70, 5
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Sort DataFrame by number of incidents
df_sorted = df.sort_values(by='Incidents', ascending=False)

# Plot
plt.figure(figsize=(14, 20))
sns.barplot(x='Incidents', y='Region', data=df_sorted, palette='viridis')
plt.title('Antisemitic Incidents in North American Countries and U.S. States (2024)')
plt.xlabel('Number of Incidents')
plt.ylabel('Region')
plt.annotate('Data updated as of November 11, 2024', xy=(0.5, -0.05), xycoords='axes fraction', ha='center', fontsize=10)
plt.show()
