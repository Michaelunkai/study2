# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
import joblib

# Step 1: Load Data
data = pd.read_ ('path_to_your_data. ')

# Step 2: Exploratory Data Analysis (EDA)
# Visualize distribution of credit scores
sns.histplot(data['credit_score'])
plt.title('Distribution of Credit Scores')
plt. ow()

# Analyze summary statistics and missing values
print(data.describe())
print(data.isnull().sum())

# Step 3: Feature Engineering
# Create High Risk Indicator
data['high_risk'] = data['credit_score'] < 600

# Handle missing values by filling with mean
data = data.fillna(data.mean())

# Convert categorical features to numerical
data = pd.get_dummies(data)

# Step 4: Split Data into Training and Testing Sets
X = data.drop('high_risk', axis=1)
y = data['high_risk']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Step 5: Train a RandomForest Model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
print(classification_report(y_test, y_pred))

# Optional: Tune Model Parameters
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, 20]
}
grid_search = GridSearchCV(RandomForestClassifier(), param_grid, cv=3)
grid_search.fit(X_train, y_train)

print("Best Parameters:", grid_search.best_params_)

# Step 6: Save and Load the Model
# Save the trained model
joblib.dump(model, 'credit_risk_model.pkl')

# Load the model for future use
model = joblib.load('credit_risk_model.pkl')

# Optional: Use Jupyter Notebook for interactive analysis
