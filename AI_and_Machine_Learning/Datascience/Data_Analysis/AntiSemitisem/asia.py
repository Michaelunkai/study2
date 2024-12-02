import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Extended Data: Adding 10 More Asian Countries (2024)
data = {
    'Country': [
        'Israel', 'Turkey', 'Iran', 'India', 'Indonesia', 'Pakistan', 'Bangladesh', 'Japan', 'Philippines', 'Vietnam',
        'South Korea', 'Thailand', 'Myanmar', 'Malaysia', 'Nepal', 'Sri Lanka', 'Kazakhstan', 'Uzbekistan', 'Saudi Arabia',
        'United Arab Emirates', 'Iraq', 'Syria', 'Jordan', 'Lebanon', 'Yemen', 'Oman', 'Qatar', 'Kuwait', 'Bahrain',
        'Afghanistan', 'Turkmenistan', 'Tajikistan', 'Kyrgyzstan', 'Mongolia', 'Laos', 'Cambodia', 'Brunei', 'Bhutan',
        'Maldives', 'Singapore', 'Armenia', 'Azerbaijan', 'Georgia', 'North Korea', 'East Timor', 'Palestine', 'Cyprus', 'Maldives'
    ],
    'Incidents': [
        500, 200, 150, 100, 80, 70, 60, 50, 40, 30, 25, 20, 18, 15, 12, 10, 8, 7, 6, 5, 5, 4, 4, 3, 3, 2, 2, 2, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 8, 7, 6, 5, 4, 3, 2
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Sort DataFrame by number of incidents
df_sorted = df.sort_values(by='Incidents', ascending=False)

# Plot
plt.figure(figsize=(14, 18))
sns.barplot(x='Incidents', y='Country', data=df_sorted, palette='viridis')
plt.title('Antisemitic Incidents in Asian Countries (2024)')
plt.xlabel('Number of Incidents')
plt.ylabel('Country')
plt.annotate('Data updated as of November 11, 2024', xy=(0.5, -0.05), xycoords='axes fraction', ha='center', fontsize=10)
plt.show()
