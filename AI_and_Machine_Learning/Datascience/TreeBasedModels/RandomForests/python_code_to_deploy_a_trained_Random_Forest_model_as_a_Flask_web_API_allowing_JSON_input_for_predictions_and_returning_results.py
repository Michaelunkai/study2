#pip install pandas scikit-learn joblib

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import joblib

# Load the data from the CSV file
data = pd.read_csv('data.csv')

# Split the data into features (X) and labels (y)
X = data[['Feature1', 'Feature2', 'Feature3']]
y = data['Label']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a RandomForestClassifier object
clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Hyperparameter tuning
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_features': ['sqrt', 'log2'],
    'max_depth': [4, 6, 8, None],
    'criterion': ['gini', 'entropy']
}

grid_search = GridSearchCV(estimator=clf, param_grid=param_grid, cv=2, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

# Save the best model to a file
best_clf = grid_search.best_estimator_
joblib.dump(best_clf, 'best_random_forest_model.pkl')

