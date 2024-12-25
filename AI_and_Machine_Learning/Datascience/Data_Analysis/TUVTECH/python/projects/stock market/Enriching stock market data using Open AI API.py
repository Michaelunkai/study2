import os
import pandas as pd
from openai import OpenAI
client = OpenAI(api_key="api key")

def classify_sector(company_name):
    """
    Uses OpenAI API to classify a company into a sector.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a financial expert specializing in company classifications."},
            {"role": "user", "content": f"Classify the company '{company_name}' into a sector. Respond with just the sector name."}
        ]
    )
    return response.choices[0].message.content.strip()

def enrich_data_with_sector(data):
    """
    Adds a 'Sector' column to the dataset using OpenAI classification.
    """
    data['Sector'] = data['name'].apply(classify_sector)
    return data

def calculate_performance_metrics(data):
    """
    Calculate performance metrics for each sector
    """
    metrics = ['ytd_change', 'price_change_1d', 'price_change_5d', 'price_change_1m', 'price_change_3m', 'price_change_6m']
    
    # Ensure numeric columns
    for metric in metrics:
        if metric in data.columns:
            data[metric] = pd.to_numeric(data[metric].str.rstrip('%'), errors='coerce')

    return data

# Load datasets
nasdaq100 = pd.read_csv("nasdaq100.csv")
nasdaq100_price_change = pd.read_csv("nasdaq100_price_change.csv")

# Enrich the dataset with sectors
nasdaq100_with_sectors = enrich_data_with_sector(nasdaq100)

# Merge datasets to include price change data
merged_data = pd.merge(nasdaq100_with_sectors, nasdaq100_price_change, on="symbol")

# Calculate performance metrics
merged_data = calculate_performance_metrics(merged_data)

# Summarize sector performance
numeric_columns = merged_data.select_dtypes(include=['float64', 'int64']).columns
sector_summary = merged_data.groupby("Sector")[numeric_columns].agg(['mean', 'std']).round(2)

# Save the output
merged_data.to_csv("enriched_nasdaq100.csv", index=False)
sector_summary.to_csv("sector_performance_summary.csv")

print("Data enrichment and analysis complete. Files saved successfully.")
