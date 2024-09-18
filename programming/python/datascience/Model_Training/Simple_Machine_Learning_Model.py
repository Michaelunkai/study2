import pandas as pd  # Importing pandas for data manipulation
from sklearn.datasets import load_iris  # Loading Iris dataset from sklearn
from sklearn.model_selection import train_test_split  # Importing train_test_split for data splitting
from sklearn.ensemble import RandomForestClassifier  # Importing RandomForestClassifier
from sklearn.metrics import accuracy_score  # Importing accuracy_score for evaluation

# Load the Iris dataset
iris = load_iris()  # Loading the Iris dataset
data = pd.DataFrame(data=iris.data, columns=iris.feature_names)  # Creating DataFrame
data['target'] = iris.target  # Adding target column

# Split the data into training and testing sets
X = data.iloc[:, :-1]  # Features
y = data['target']  # Target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # Splitting data

# Train a Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)  # Initializing classifier
clf.fit(X_train, y_train)  # Training classifier

# Make predictions
y_pred = clf.predict(X_test)  # Making predictions

# Calculate the accuracy
accuracy = accuracy_score(y_test, y_pred)  # Calculating accuracy
print(f'Accuracy: {accuracy * 100:.2f}%')  # Printing accuracy
