import pandas as pd
import matplotlib.pyplot as plt

# Define the file path
file_path = "difference_cumulative_angles.txt"  # Ensure this file is in the same directory as the script

# Load the data
data = pd.read_csv(file_path, delimiter="\t")

# Extract data for plotting
vectorsum_angles = data["Vectorsum Cumulative Angle"]
spolessum_angles = data["Spolessum Cumulative Angle"]
differences = data["Difference"]

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(vectorsum_angles, label="Vectorsum Cumulative Angle", linewidth=2)
plt.plot(spolessum_angles, label="Spolessum Cumulative Angle", linewidth=2)
plt.plot(differences, label="Difference", linestyle='--', linewidth=2, color="red")
plt.title("Comparison of Cumulative Angles and Their Differences", fontsize=14)
plt.xlabel("Data Points", fontsize=12)
plt.ylabel("Angles (degrees)", fontsize=12)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()

