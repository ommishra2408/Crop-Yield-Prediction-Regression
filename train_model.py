import matplotlib.pyplot as plt
import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# 1. Load the dataset
data = pd.read_csv("crop_yield.csv")

print("Dataset loaded successfully!")
print(data.head())


# 2. Separate input features and output
X = data.drop("Yield", axis=1)
y = data["Yield"]


# 3. Define columns
categorical_columns = ["Crop"]

numerical_columns = [
    "Area",
    "Rainfall",
    "Temperature",
    "Fertilizer",
    "Irrigation",
    "Soil_pH"
]


# 4. Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_columns
        ),
        (
            "numerical",
            "passthrough",
            numerical_columns
        )
    ]
)


# 5. Create the Linear Regression model
model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("regressor", LinearRegression())
    ]
)


# 6. Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# 7. Train the model
model.fit(X_train, y_train)

print("\nModel training completed!")


# 8. Make predictions
y_pred = model.predict(X_test)


# 9. Evaluate the model
mae = mean_absolute_error(y_test, y_pred)

mse = mean_squared_error(y_test, y_pred)

rmse = mse ** 0.5

r2 = r2_score(y_test, y_pred)


print("\nModel Evaluation")
print("-------------------------")

print("Mean Absolute Error (MAE):", round(mae, 2))

print("Mean Squared Error (MSE):", round(mse, 2))

print("Root Mean Squared Error (RMSE):", round(rmse, 2))

print("R2 Score:", round(r2, 2))


# 10. Save the trained model
import os

model_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "model.pkl"
)

with open(model_path, "wb") as file:
    pickle.dump(model, file)

print("\nModel saved successfully!")
print("Model location:", model_path)

# 11. Plot Actual vs Predicted Yield

plt.figure(figsize=(8, 6))

plt.scatter(y_test, y_pred)

plt.plot(
    [y_test.min(), y_test.max()],
    [y_test.min(), y_test.max()],
    linestyle="--"
)

plt.xlabel("Actual Yield")
plt.ylabel("Predicted Yield")

plt.title("Actual vs Predicted Crop Yield")

plt.tight_layout()

plt.savefig("actual_vs_predicted.png")

plt.show()