import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load data
data = pd.read_csv("pong_data.csv")
X = data.drop('action', axis=1)
y = data['action']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model with hyperparameter tuning
param_grid = {
    'n_estimators': [50, 100],
    'max_depth': [5, 10, 15]
}
model = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5, n_jobs=-1)
model.fit(X_train, y_train)

# Output results
print("Best parameters:", model.best_params_)
print("Model accuracy:", model.score(X_test, y_test))

# Save the best model
joblib.dump(model.best_estimator_, "pong_model.pkl")
print("Model saved as pong_model.pkl")