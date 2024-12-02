import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv('play_tennis.csv')

# Prepare data
X = data.iloc[:, :-1]  # Features
y = data.iloc[:, -1]   # Target

# Convert categorical data to numeric
X = pd.get_dummies(X)

# Create and train the decision tree
clf = DecisionTreeClassifier(criterion='entropy')
clf = clf.fit(X, y)

# Plot the tree
plt.figure(figsize=(12, 8))
tree.plot_tree(clf, feature_names=X.columns, class_names=['No', 'Yes'], filled=True)
plt.show()
