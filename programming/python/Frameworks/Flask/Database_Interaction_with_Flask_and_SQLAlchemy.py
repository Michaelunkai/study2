#  Database Interaction with Flask and SQLAlchemy
# pip install Flask Flask-SQLAlchemy


from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Create a simple model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

# Define a route
@app.route('/')
def home():
    # Query all users from the database
    users = User.query.all()
    return render_template('index.html', title='Home', content='Welcome to the home page!', users=users)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
