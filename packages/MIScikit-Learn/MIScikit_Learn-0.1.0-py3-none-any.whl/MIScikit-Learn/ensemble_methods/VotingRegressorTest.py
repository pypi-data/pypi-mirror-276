import numpy as np
from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from VotingRegressor import VotingRegressor

# Load the diabetes dataset
X, y = load_diabetes(return_X_y=True)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

ridge = Ridge()
dt = DecisionTreeRegressor(random_state=42)
rf = RandomForestRegressor(n_estimators=100, random_state=42)

# Initialize the Voting Regressor
voting_regressor = VotingRegressor(estimators=[('ridge', ridge), ('dt', dt), ('rf', rf)])

# Fit the models
ridge.fit(X_train, y_train)
dt.fit(X_train, y_train)
rf.fit(X_train, y_train)
voting_regressor.fit(X_train, y_train)

# Make predictions
ridge_preds = ridge.predict(X_test)
dt_preds = dt.predict(X_test)
rf_preds = rf.predict(X_test)
voting_preds = voting_regressor.predict(X_test)

# Calculate MSE
voting_mse = mean_squared_error(y_test, voting_preds)

# Print the results
print(f"Custom VotingRegressor MSE: {voting_mse:.4f}")
# Compare with sklearn's VotingRegressor
from sklearn.ensemble import VotingRegressor as SklearnVotingRegressor

sklearn_voting_regressor = SklearnVotingRegressor(estimators=[('ridge', ridge), ('dt', dt), ('rf', rf)])
sklearn_voting_regressor.fit(X_train, y_train)
sklearn_voting_preds = sklearn_voting_regressor.predict(X_test)

# Calculate MSE
sklearn_voting_mse = mean_squared_error(y_test, sklearn_voting_preds)

# Print the results
print(f"Sklearn VotingRegressor MSE: {sklearn_voting_mse:.4f}")

