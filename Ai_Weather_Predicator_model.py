"""
Simple Weather Predictor
------------------------
Predicts the chance of rain tomorrow using a simple decision-tree style model.
This version is designed to match the assignment topic of decision trees and
random forests.

Run:  Select this file's Python interpreter in VS Code, then choose "Run Python File".
"""


import numpy as np
from sklearn.ensemble import RandomForestRegressor

FEATURES = ["temp", "humidity", "pressure", "cloud", "wind"]

# 1. Make fake training data (replace with real weather records if you have them)
rng = np.random.default_rng(42)
X = np.column_stack([
    rng.uniform(-5, 40, 3000),     # temp
    rng.uniform(10, 100, 3000),    # humidity
    rng.uniform(980, 1030, 3000),  # pressure
    rng.uniform(0, 100, 3000),     # cloud
    rng.uniform(0, 60, 3000),      # wind
])
# "True" rain chance: humid + cloudy + low pressure + windy = more rain
y = 0.4 * X[:, 1] + 0.4 * X[:, 3] + (1013 - X[:, 2]) + 0.2 * X[:, 4]
y = np.clip(y + rng.normal(0, 5, 3000), 0, 100)

# 2. Train the random forest
model = RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42)
model.fit(X, y)


# 3. Ask for today's weather
def ask(prompt, default):
    while True:
        value = input(f"{prompt} [{default}]: ").strip()
        if not value:
            return float(default)

        try:
            return float(value)
        except ValueError:
            print("Please enter a number, or press Enter to use the default value.")


today = [
    ask("Temperature (°C)", 18),
    ask("Humidity (%)", 85),
    ask("Air pressure (hPa)", 1000),
    ask("Cloud cover (%)", 80),
    ask("Wind speed (km/h)", 20),
]

# 4. Every tree votes, the forest averages the votes
votes = [tree.predict([today])[0] for tree in model.estimators_]
rain = round(float(np.clip(np.mean(votes), 0, 100)))

print("\n--- Voting ---")
for i in range(3):
    print(f"Tree {i + 1}: {votes[i]:.0f}%")
print(f"... {len(votes)} trees in total")
print(f"Forest average = {rain}%")

# 5. Turn the number into a forecast
cloud, wind = today[3], today[4]
if rain >= 80 and wind > 35:
    condition = "Stormy"
elif rain >= 60:
    condition = "Rainy"
elif cloud >= 70:
    condition = "Cloudy"
elif cloud >= 30:
    condition = "Partly Cloudy"
else:
    condition = "Sunny"

print(f"\nCondition   : {condition}")
print(f"Rain chance : {rain}%")