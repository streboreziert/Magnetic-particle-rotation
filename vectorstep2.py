import re

# Define the file path
file_path = 'vector_angles_with_direction.txt'

# Initialize variables
data = []
cumulative_angle = 0

# Regex pattern to parse the lines
pattern = re.compile(r"Photo \d+: Angle = ([\d.]+) degrees, Direction = (-?\d+)")

# Read and process the file
with open(file_path, 'r') as file:
    for line in file:
        match = pattern.search(line)
        if match:
            angle = float(match.group(1))
            direction = int(match.group(2))
            cumulative_angle += angle * direction
            data.append({'Angle': angle, 'Direction': direction, 'Cumulative Angle': cumulative_angle})

# Write results to a TXT file
output_file = 'cumulative_angles.txt'
with open(output_file, 'w') as file:
    file.write("Angle (degrees), Direction, Cumulative Angle (degrees)\n")
    for entry in data:
        file.write(f"{entry['Angle']:.2f}, {entry['Direction']}, {entry['Cumulative Angle']:.2f}\n")

print(f"\nResults saved to '{output_file}'.")

