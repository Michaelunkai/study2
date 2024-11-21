import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Data: Antisemitic Incidents in South American Countries (2024)
data = {
    'Country': [
        'Argentina', 'Brazil', 'Chile', 'Colombia', 'Peru', 'Venezuela', 'Ecuador', 'Bolivia', 'Paraguay', 'Uruguay', 'Guyana', 'Suriname'
    ],
    'Incidents': [
        598, 1774, 150, 100, 80, 60, 50, 40, 30, 20, 10, 5
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Sort DataFrame by number of incidents
df_sorted = df.sort_values(by='Incidents', ascending=False)

# Plot
plt.figure(figsize=(12, 8))
sns.barplot(x='Incidents', y='Country', data=df_sorted, palette='viridis')
plt.title('Antisemitic Incidents in South American Countries (2024)')
plt.xlabel('Number of Incidents')
plt.ylabel('Country')
plt.annotate('Data updated as of November 11, 2024', xy=(0.5, -0.05), xycoords='axes fraction', ha='center', fontsize=10)
plt.show()
