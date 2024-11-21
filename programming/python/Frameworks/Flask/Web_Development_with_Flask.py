#  Web Development with Flask

from flask import Flask, render_template

app = Flask(__name__)

# Define a route
@app.route('/')
def home():
    return render_template('index.html', title='Home', content='Welcome to the home page!')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)