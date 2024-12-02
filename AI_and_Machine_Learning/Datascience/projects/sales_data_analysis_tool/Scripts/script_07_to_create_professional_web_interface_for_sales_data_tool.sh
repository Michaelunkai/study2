# Navigate to the project directory
cd ~/projects/sales_data_analysis_tool

# Install Flask and related packages
pip3 install flask

# Create a Python script to set up the Flask web application
echo "from flask import Flask, render_template, request
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
" > app.py

# Create the templates directory and HTML files for the web pages
mkdir -p templates static

# Create the home page template with Bootstrap styling
echo "<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'>
    <title>Sales Data Analysis Tool</title>
</head>
<body>
    <nav class='navbar navbar-expand-lg navbar-light bg-light'>
        <a class='navbar-brand' href='/'>Sales Data Analysis Tool</a>
        <button class='navbar-toggler' type='button' data-toggle='collapse' data-target='#navbarNav' aria-controls='navbarNav' aria-expanded='false' aria-label='Toggle navigation'>
            <span class='navbar-toggler-icon'></span>
        </button>
        <div class='collapse navbar-collapse' id='navbarNav'>
            <ul class='navbar-nav'>
                <li class='nav-item active'>
                    <a class='nav-link' href='/'>Home</a>
                </li>
                <li class='nav-item'>
                    <a class='nav-link' href='/analyze'>Data Analysis</a>
                </li>
                <li class='nav-item'>
                    <a class='nav-link' href='/predictions'>Sales Predictions</a>
                </li>
            </ul>
        </div>
    </nav>

    <div class='container mt-4'>
        <div class='jumbotron'>
            <h1 class='display-4'>Welcome to the Sales Data Analysis Tool</h1>
            <p class='lead'>This tool allows you to analyze sales data and make predictions based on historical trends.</p>
            <hr class='my-4'>
            <p>Use the navigation bar to explore data analysis and predictions.</p>
            <a class='btn btn-primary btn-lg' href='/analyze' role='button'>View Data Analysis</a>
            <a class='btn btn-secondary btn-lg' href='/predictions' role='button'>View Sales Predictions</a>
        </div>
    </div>

    <footer class='footer bg-light text-center'>
        <div class='container'>
            <span class='text-muted'>© 2024 Sales Data Analysis Tool. All rights reserved.</span>
        </div>
    </footer>

    <script src='https://code.jquery.com/jquery-3.5.1.slim.min.js'></script>
    <script src='https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js'></script>
    <script src='https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js'></script>
</body>
</html>
" > templates/index.html

# Create the analysis page template with Bootstrap styling
echo "<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'>
    <title>Data Analysis</title>
</head>
<body>
    <nav class='navbar navbar-expand-lg navbar-light bg-light'>
        <a class='navbar-brand' href='/'>Sales Data Analysis Tool</a>
        <button class='navbar-toggler' type='button' data-toggle='collapse' data-target='#navbarNav' aria-controls='navbarNav' aria-expanded='false' aria-label='Toggle navigation'>
            <span class='navbar-toggler-icon'></span>
        </button>
        <div class='collapse navbar-collapse' id='navbarNav'>
            <ul class='navbar-nav'>
                <li class='nav-item'>
                    <a class='nav-link' href='/'>Home</a>
                </li>
                <li class='nav-item active'>
                    <a class='nav-link' href='/analyze'>Data Analysis</a>
                </li>
                <li class='nav-item'>
                    <a class='nav-link' href='/predictions'>Sales Predictions</a>
                </li>
            </ul>
        </div>
    </nav>

    <div class='container mt-4'>
        <h1>Data Analysis</h1>
        <img src='{{ plot_url }}' class='img-fluid' alt='Total Sales by Product'>
        <hr class='my-4'>
        <a class='btn btn-primary' href='/'>Back to Home</a>
    </div>

    <footer class='footer bg-light text-center'>
        <div class='container'>
            <span class='text-muted'>© 2024 Sales Data Analysis Tool. All rights reserved.</span>
        </div>
    </footer>

    <script src='https://code.jquery.com/jquery-3.5.1.slim.min.js'></script>
    <script src='https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js'></script>
    <script src='https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js'></script>
</body>
</html>
" > templates/analyze.html

# Create the predictions page template with Bootstrap styling
echo "<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'>
    <title>Sales Predictions</title>
</head>
<body>
    <nav class='navbar navbar-expand-lg navbar-light bg-light'>
        <a class='navbar-brand' href='/'>Sales Data Analysis Tool</a>
        <button class='navbar-toggler' type='button' data-toggle='collapse' data-target='#navbarNav' aria-controls='navbarNav' aria-expanded='false' aria-label='Toggle navigation'>
            <span class='navbar-toggler-icon'></span>
        </button>
        <div class='collapse navbar-collapse' id='navbarNav'>
            <ul class='navbar-nav'>
                <li class='nav-item'>
                    <a class='nav-link' href='/'>Home</a>
                </li>
                <li class='nav-item'>
                    <a class='nav-link' href='/analyze'>Data Analysis</a>
                </li>
                <li class='nav-item active'>
                    <a class='nav-link' href='/predictions'>Sales Predictions</a>
                </li>
            </ul>
        </div>
    </nav>

    <div class='container mt-4'>
        <h1>Sales Predictions</h1>
        <img src='{{ plot_url }}' class='img-fluid' alt='Predicted Sales vs Quantity'>
        <hr class='my-4'>
        <a class='btn btn-primary' href='/'>Back to Home</a>
    </div>

    <footer class='footer bg-light text-center'>
        <div class='container'>
            <span class='text-muted'>© 2024 Sales Data Analysis Tool. All rights reserved.</span>
        </div>
    </footer>

    <script src='https://code.jquery.com/jquery-3.5.1.slim.min.js'></script>
    <script src='https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js'></script>
    <script src='https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js'></script>
</body>
</html>
" > templates/predictions.html

# Run the Flask web application
python3 app.py
