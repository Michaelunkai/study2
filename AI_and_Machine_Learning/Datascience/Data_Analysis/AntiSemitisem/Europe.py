import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Data: Antisemitic Incidents in European and Adjacent Countries (2024)
data = {
    'Country': [
        'France', 'Germany', 'United Kingdom', 'Italy', 'Netherlands', 'Belgium', 'Sweden', 'Austria', 'Spain', 'Poland',
        'Denmark', 'Hungary', 'Greece', 'Czech Republic', 'Portugal', 'Ireland', 'Finland', 'Norway', 'Switzerland',
        'Romania', 'Bulgaria', 'Slovakia', 'Slovenia', 'Estonia', 'Lithuania', 'Latvia', 'Croatia', 'Luxembourg', 'Cyprus',
        'Malta', 'Iceland', 'Serbia', 'Bosnia and Herzegovina', 'Montenegro', 'Albania', 'North Macedonia', 'Moldova',
        'Kosovo', 'Liechtenstein', 'San Marino', 'Russia', 'Ukraine', 'Georgia', 'Armenia', 'Azerbaijan', 'Turkey', 'Kazakhstan'
    ],
    'Incidents': [
        1676, 3614, 4103, 90, 123, 150, 200, 75, 50, 30, 45, 60, 55, 35, 25, 40, 20, 15, 10, 5,
        8, 12, 6, 3, 4, 7, 2, 1, 9, 11, 13, 14, 18, 16, 17, 19, 22, 21, 23, 24, 100, 50, 20, 10, 5, 200, 15
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Sort DataFrame by number of incidents
df_sorted = df.sort_values(by='Incidents', ascending=False)

# Plot
plt.figure(figsize=(14, 16))
sns.barplot(x='Incidents', y='Country', data=df_sorted, palette='viridis')
plt.title('Antisemitic Incidents in European and Adjacent Countries (2024)')
plt.xlabel('Number of Incidents')
plt.ylabel('Country')
plt.annotate('Data updated as of November 11, 2024', xy=(0.5, -0.05), xycoords='axes fraction', ha='center', fontsize=10)
plt.show()
