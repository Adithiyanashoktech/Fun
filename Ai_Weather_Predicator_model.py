"""
Simple Weather Predictor
------------------------
Predicts the chance of rain tomorrow using a simple decision-tree style model.
This version is designed to match the assignment topic of decision trees and
random forests.

Run:  python weather_predictor.py
"""


def decision_tree_1(today):
    """Tree 1: heavy humidity + low pressure + lots of cloud = rain."""
    if today["humidity"] >= 75 and today["pressure"] <= 1010 and today["cloud"] >= 70:
        return 92
    if today["humidity"] >= 65 and today["pressure"] <= 1012:
        return 78
    if today["cloud"] >= 60:
        return 60
    if today["humidity"] >= 50:
        return 42
    return 18


def decision_tree_2(today):
    """Tree 2: strong wind and high clouds often mean storms."""
    if today["wind"] >= 30 and today["cloud"] >= 70:
        return 88
    if today["pressure"] <= 1008 and today["humidity"] >= 70:
        return 82
    if today["cloud"] >= 50:
        return 54
    if today["temp"] >= 28 and today["humidity"] <= 45:
        return 12
    return 28


def decision_tree_3(today):
    """Tree 3: combine humidity, cloud, and pressure rules."""
    if today["humidity"] >= 80 and today["cloud"] >= 75:
        return 90
    if today["pressure"] <= 1005 and today["wind"] >= 20:
        return 80
    if today["cloud"] >= 65:
        return 68
    if today["humidity"] >= 60:
        return 46
    return 22


def predict_weather(today):
    trees = [decision_tree_1(today), decision_tree_2(today), decision_tree_3(today)]
    rain_chance = round(sum(trees) / len(trees))

    print("\n--- Decision tree voting ---")
    print(f"Tree 1: {trees[0]}%")
    print(f"Tree 2: {trees[1]}%")
    print(f"Tree 3: {trees[2]}%")
    print(f"Random forest style average = {rain_chance}%")

    if rain_chance >= 80 and today["wind"] > 35:
        condition = "Stormy"
    elif rain_chance >= 60:
        condition = "Rainy"
    elif today["cloud"] >= 70:
        condition = "Cloudy"
    elif today["cloud"] >= 30:
        condition = "Partly Cloudy"
    else:
        condition = "Sunny"

    tomorrow_temp = today["temp"] + (today["pressure"] - 1013) * 0.1 - (rain_chance / 100) * 3

    return rain_chance, condition, round(tomorrow_temp, 1)


def ask(prompt, default):
    while True:
        value = input(f"{prompt} [{default}]: ").strip()
        if not value:
            return float(default)

        try:
            return float(value)
        except ValueError:
            print("Please enter a number, or press Enter to use the default value.")


if __name__ == "__main__":
    print("=== Simple Weather Predictor ===  (press Enter for default)")
    today = {
        "temp":     ask("Temperature (°C)", 18),
        "humidity": ask("Humidity (%)", 85),
        "pressure": ask("Air pressure (hPa)", 1000),
        "cloud":    ask("Cloud cover (%)", 80),
        "wind":     ask("Wind speed (km/h)", 20),
    }

    rain, condition, temp = predict_weather(today)

    print("\n=== Tomorrow's Forecast ===")
    print(f"Condition   : {condition}")
    print(f"Rain chance : {rain}%")
    print(f"Temperature : {temp} °C")
    