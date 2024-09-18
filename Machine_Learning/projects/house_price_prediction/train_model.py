from sklearn.ensemble import RandomForestRegressor
import joblib

# Load preprocessed data
X_train = joblib.load('X_train.pkl')
y_train = joblib.load('y_train.pkl')

# Choose a model
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, 'model.pkl')
