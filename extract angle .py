import re
import math

# Input and output file paths
input_file_path = 'input.txt'  # Replace with your input file path
output_file_path = 'extracted_values_with_angles.txt'

# Regular expression to match Semi-Major and Semi-Minor Axis values
pattern = r'Semi-Major Axis: (\d+), Semi-Minor Axis: (\d+)'

# Read the input file
with open(input_file_path, 'r') as file:
    content = file.read()

# Find all matches
matches = re.findall(pattern, content)

# Check if matches were found
if matches:
    # Open the output file for writing results
    with open(output_file_path, 'w') as output_file:
        # Write the header for the output file
        output_file.write("Semi-Major Axis, Semi-Minor Axis, Angle (Radians), Angle (Degrees)\n")

        # Process each match
        for major, minor in matches:
            # Convert extracted values to integers
            major = int(major)
            minor = int(minor)

            # Calculate angles if the major axis is non-zero
            if major > 0:
                angle_radians = math.asin(minor / major)
                angle_degrees = math.degrees(angle_radians)
            else:
                angle_radians = angle_degrees = 0

            # Write the results to the output file
            output_file.write(f"{major}, {minor}, {round(angle_radians, 4)}, {round(angle_degrees, 2)}\n")

    print(f"Data extracted and angles calculated successfully. Results saved to {output_file_path}")
else:
    print("No matches found. Please check the input file format.")

