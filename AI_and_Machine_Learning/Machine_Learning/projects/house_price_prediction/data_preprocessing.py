import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib

# Load your dataset
data = pd.read_ ('dataset. ')
print(data.head())

# Handling missing values
data = data.dropna()
# or
# data = data.fillna(method='ffill')

# Encoding categorical variables
data = pd.get_dummies(data, columns=['categorical_column'])

# Feature scaling
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data.drop('target_column', axis=1))
data_scaled = pd.DataFrame(data_scaled, columns=data.columns[:-1])
data_scaled['target_column'] = data['target_column']

# Split the data into training and testing sets
X = data_scaled.drop('target_column', axis=1)
y = data_scaled['target_column']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Save the preprocessed data
joblib.dump(X_train, 'X_train.pkl')
joblib.dump(X_test, 'X_test.pkl')
joblib.dump(y_train, 'y_train.pkl')
joblib.dump(y_test, 'y_test.pkl')
