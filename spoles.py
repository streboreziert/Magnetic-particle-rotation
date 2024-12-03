import os
import numpy as np

# Simplified function to calculate the vector length
def calculate_vector(x, y):
    return np.sqrt(x**2 + y**2)

# Path setup (replace 'E614-08F2' with your actual USB identifier)
usb_path = '/media/roberts/E614-08F2/Roberts ZPD 2024'  # Input folder
output_path = '/media/roberts/E614-08F2/results'  # Output folder

# Create results folder if it doesn't exist
os.makedirs(output_path, exist_ok=True)

# Process each .txt file in the input folder
for file_name in os.listdir(usb_path):
    if file_name.endswith('.txt'):
        input_file = os.path.join(usb_path, file_name)
        output_file = os.path.join(output_path, file_name)

        # Read the input file
        with open(input_file, 'r') as infile:
            lines = infile.readlines()

        # Process the lines, extract coordinates and calculate vectors
        with open(output_file, 'w') as outfile:
            for line in lines:
                columns = line.split()
                if len(columns) > 5:  # Ensure there are enough columns
                    try:
                        x = float(columns[3])  # 4th column (X coordinate)
                        y = float(columns[4])  # 5th column (Y coordinate)
                        vector_length = calculate_vector(x, y)
                        outfile.write(f"{line.strip()} {vector_length:.6f}\n")
                    except ValueError:
                        outfile.write(line)  # Write line as is if there's an error (header, etc.)

