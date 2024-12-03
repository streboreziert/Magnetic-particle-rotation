import re
import numpy as np
import pandas as pd

# Define input and output file paths
input_file = 'spoles.txt'
output_file = 'angles_and_cumulative.txt'

# Function to calculate the angle between two vectors
def calculate_angle(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    dot_product = np.dot(v1, v2)
    magnitude_product = np.linalg.norm(v1) * np.linalg.norm(v2)
    if magnitude_product == 0:
        return 0
    angle = np.degrees(np.arccos(np.clip(dot_product / magnitude_product, -1.0, 1.0)))
    return angle

# Parse the file and extract vectors
vector_data = []
with open(input_file, 'r') as file:
    for line in file:
        if "Vector" in line:
            try:
                timestamp = line.split(",")[0].split(":")[1].strip()
                vector_values = line.split("Vector: ")[1].strip("[]\n").split(", ")
                vector = [float(v) for v in vector_values]
                vector_data.append({'Time': timestamp, 'Vector': vector})
            except Exception as e:
                print(f"Error parsing line: {line}, Error: {e}")

# Calculate angles and cumulative angles
angles = []
cumulative_angle = 0
cumulative_angles = []

for i in range(1, len(vector_data)):
    angle = calculate_angle(vector_data[i - 1]['Vector'], vector_data[i]['Vector'])
    angles.append(angle)
    cumulative_angle += angle
    cumulative_angles.append(cumulative_angle)

# Save results to a file
results = []
for i in range(1, len(vector_data)):
    results.append({
        'Time': vector_data[i]['Time'],
        'Angle': angles[i - 1],
        'Cumulative Angle': cumulative_angles[i - 1]
    })

# Convert results to DataFrame and save to a text file
df_results = pd.DataFrame(results)
df_results.to_csv(output_file, index=False, sep='\t')

print(f"Results saved to {output_file}.")

