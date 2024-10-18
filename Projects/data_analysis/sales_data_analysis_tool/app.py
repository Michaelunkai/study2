from flask import Flask, render_template, request
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to display data analysis and visualization
@app.route('/analyze')
def analyze():
    # Connect to the SQLite database
    conn = sqlite3.connect('sales_data_analysis.db')

    # Read cleaned data from the sales_data_cleaned table into a DataFrame
    df = pd.read_sql_query('SELECT * FROM sales_data_cleaned', conn)

    # Plot total sales by product using cleaned data
    total_sales_by_product = df.groupby('product_name')['total_sales'].sum()
    total_sales_by_product.plot(kind='bar', title='Total Sales by Product (Cleaned Data)')
    plt.xlabel('Product Name')
    plt.ylabel('Total Sales')

    # Save the plot as an image file within the project folder
    plot_path = 'static/total_sales_by_product_cleaned_web.png'
    plt.savefig(plot_path)
    plt.close()

    # Close the database connection
    conn.close()

    return render_template('analyze.html', plot_url=plot_path)

# Route to display sales predictions
@app.route('/predictions')
def predictions():
    # Connect to the SQLite database
    conn = sqlite3.connect('sales_data_analysis.db')

    # Read the predictions from the sales_predictions table into a DataFrame
    df = pd.read_sql_query('SELECT * FROM sales_predictions', conn)

    # Plot the predicted sales
    plt.scatter(df['quantity'], df['predicted_sales'], color='blue', label='Predicted Sales')
    plt.xlabel('Quantity')
    plt.ylabel('Predicted Sales')
    plt.title('Predicted Sales vs Quantity')
    plt.legend()

    # Save the plot as an image file within the project folder
    plot_path = 'static/predicted_sales_vs_quantity_web.png'
    plt.savefig(plot_path)
    plt.close()

    # Close the database connection
    conn.close()

    return render_template('predictions.html', plot_url=plot_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)

