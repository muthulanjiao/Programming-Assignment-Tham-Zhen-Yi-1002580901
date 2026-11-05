# DEX2013 Programming for Engineering - Python Assignment
# Smart Machine Condition Monitoring and Safety Alert System
# Note: classroom simulation only, thresholds are example values.

import pandas as pd
import matplotlib.pyplot as plt

# Show all columns when printing tables
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

FILE_NAME = "machine_condition_dataset.csv"

REQUIRED_COLUMNS = ["Reading_ID", "Time_s", "Temperature_C", "Pressure_bar",
                    "Vibration_mm_s", "Motor_Current_A", "RPM"]

PARAMETERS = ["Temperature_C", "Pressure_bar", "Vibration_mm_s",
              "Motor_Current_A", "RPM"]

UNITS = {"Temperature_C": "°C", "Pressure_bar": "bar", "Vibration_mm_s": "mm/s",
         "Motor_Current_A": "A", "RPM": "RPM"}


def classify_condition(temperature, pressure, vibration, current, rpm):
    """Return NORMAL, WARNING or CRITICAL for one reading.
    CRITICAL is checked first, then WARNING, otherwise NORMAL."""
    if (temperature > 50 or pressure > 6.0 or vibration > 6.0
            or current > 5.0 or rpm < 1350 or rpm > 1550):
        return "CRITICAL"
    elif (temperature >= 40 or pressure < 2.0 or vibration >= 3.0
          or current >= 4.0 or rpm < 1400 or rpm > 1500):
        return "WARNING"
    else:
        return "NORMAL"


def determine_action(status):
    """Return the simulated recommended action for a status."""
    if status == "CRITICAL":
        return "Stop operation in the simulation and request supervisor/technician inspection"
    elif status == "WARNING":
        return "Continue monitoring and arrange inspection"
    else:
        return "Continue normal monitoring in the simulation"


def load_data(file_name):
    """Load the CSV file and check the required columns. Returns None on failure."""
    try:
        data = pd.read_csv(file_name)
    except FileNotFoundError:
        print("ERROR: Could not find '" + file_name + "'.")
        print("Put the CSV file in the same folder as this Python file and try again.")
        return None
    except Exception as error:
        print("ERROR: The file could not be loaded:", error)
        return None

    print("CSV file loaded successfully.")
    print("Number of readings (rows):", data.shape[0])
    print("Number of columns:", data.shape[1])

    missing = []
    for column in REQUIRED_COLUMNS:
        if column not in data.columns:
            missing.append(column)
    if len(missing) > 0:
        print("ERROR: Missing required columns:", missing)
        return None
    print("All required columns are present.")
    print("\nFirst five rows:")
    print(data.head())
    return data


def add_status_columns(data):
    """Loop through every row, classify it, and add Status and Recommended_Action."""
    status_list = []
    action_list = []
    for index in range(len(data)):
        row = data.iloc[index]
        status = classify_condition(row["Temperature_C"], row["Pressure_bar"],
                                    row["Vibration_mm_s"], row["Motor_Current_A"],
                                    row["RPM"])
        status_list.append(status)
        action_list.append(determine_action(status))
    data["Status"] = status_list
    data["Recommended_Action"] = action_list
    return data


def print_summary(data):
    """Print the status table, statistics, and status counts/percentages."""
    print("\n--- Reading status ---")
    print(data[["Reading_ID", "Status"]].to_string(index=False))

    print("\n--- Summary statistics ---")
    for parameter in PARAMETERS:
        unit = UNITS[parameter]
        print(parameter + ":")
        print("  Mean =", round(data[parameter].mean(), 2), unit)
        print("  Min  =", round(data[parameter].min(), 2), unit)
        print("  Max  =", round(data[parameter].max(), 2), unit)

    total = len(data)
    print("\n--- Status counts and percentages (total readings = " + str(total) + ") ---")
    for status in ["NORMAL", "WARNING", "CRITICAL"]:
        count = (data["Status"] == status).sum()
        percent = count / total * 100
        print(status + ": " + str(count) + " readings (" + str(round(percent, 1)) + "%)")


def make_graphs(data):
    """Create and save the temperature and vibration graphs."""
    # Temperature graph with threshold lines
    plt.figure(figsize=(8, 5))
    plt.plot(data["Time_s"], data["Temperature_C"], marker="o", label="Temperature")
    plt.axhline(y=40, color="orange", linestyle="--", label="Warning threshold (40 °C)")
    plt.axhline(y=50, color="red", linestyle="--", label="Critical boundary (50 °C)")
    plt.title("Machine Temperature vs Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Temperature (°C)")
    plt.grid(True)
    plt.legend()
    plt.savefig("temperature_vs_time.png", dpi=150)
    plt.close()

    # Vibration graph
    plt.figure(figsize=(8, 5))
    plt.plot(data["Time_s"], data["Vibration_mm_s"], marker="o", color="green",
             label="Vibration")
    plt.title("Machine Vibration vs Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Vibration (mm/s)")
    plt.grid(True)
    plt.legend()
    plt.savefig("vibration_vs_time.png", dpi=150)
    plt.close()
    print("\nGraphs saved: temperature_vs_time.png and vibration_vs_time.png")


def run_tests():
    """Run the ten required test cases from the assignment."""
    tests = [
        (35, 4.0, 2.0, 3.5, 1450, "NORMAL"),
        (40, 4.0, 2.0, 3.5, 1450, "WARNING"),
        (50, 4.0, 2.0, 3.5, 1450, "WARNING"),
        (50.1, 4.0, 2.0, 3.5, 1450, "CRITICAL"),
        (35, 6.1, 2.0, 3.5, 1450, "CRITICAL"),
        (35, 4.0, 6.1, 3.5, 1450, "CRITICAL"),
        (35, 4.0, 2.0, 5.1, 1450, "CRITICAL"),
        (35, 4.0, 2.0, 3.5, 1349, "CRITICAL"),
        (35, 4.0, 2.0, 3.5, 1390, "WARNING"),
        (35, 1.9, 2.0, 3.5, 1450, "WARNING"),
    ]
    print("\n--- Classification tests ---")
    print("Test | Expected | Actual   | Result")
    number = 1
    passed = 0
    for t in tests:
        actual = classify_condition(t[0], t[1], t[2], t[3], t[4])
        result = "PASS" if actual == t[5] else "FAIL"
        if result == "PASS":
            passed = passed + 1
        print(str(number).ljust(4) + " | " + t[5].ljust(8) + " | " + actual.ljust(8) + " | " + result)
        number = number + 1
    print(str(passed) + " of " + str(len(tests)) + " tests passed.")


def main():
    print("=== Smart Machine Condition Monitoring and Safety Alert System ===")
    print("(Classroom simulation only)\n")
    data = load_data(FILE_NAME)
    if data is None:
        return
    data = add_status_columns(data)
    print_summary(data)
    data.to_csv("machine_condition_results.csv", index=False)
    make_graphs(data)
    run_tests()


main()
