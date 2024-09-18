import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier

# Load the Iris dataset
iris = load_iris()
data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
data['target'] = iris.target

# Features and target
X = data.iloc[:, :-1]
y = data['target']

# Initialize the classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Perform cross-validation
scores = cross_val_score(clf, X, y, cv=5)

# Print the cross-validation scores
print(f'Cross-validation scores: {scores}')
print(f'Mean accuracy: {scores.mean() * 100:.2f}%')
