import math

# Load data from file
input_file = "vectors.txt"
output_file = "vector_angles_with_direction.txt"

# Function to calculate the angle between two vectors
def angle_between_vectors(v1, v2):
    x1, y1 = v1
    x2, y2 = v2
    dot_product = x1 * x2 + y1 * y2
    magnitude_v1 = math.sqrt(x1**2 + y1**2)
    magnitude_v2 = math.sqrt(x2**2 + y2**2)
    angle = math.acos(dot_product / (magnitude_v1 * magnitude_v2))  # Angle in radians
    return math.degrees(angle)  # Convert to degrees

# Function to calculate the cross product direction
def cross_product_direction(v1, v2):
    x1, y1 = v1
    x2, y2 = v2
    cross_product = x1 * y2 - y1 * x2
    return 1 if cross_product > 0 else -1

# Read vectors from the input file
vectors = []
with open(input_file, "r") as file:
    for line in file:
        if "Photo" in line:
            parts = line.split(":")
            vector = eval(parts[1].strip())  # Convert string to tuple
            vectors.append(vector)

# Calculate angles and directions
results = []
for i in range(1, len(vectors)):
    angle = angle_between_vectors(vectors[i-1], vectors[i])
    direction = cross_product_direction(vectors[i-1], vectors[i])
    results.append((i+1, angle, direction))

# Write results to the output file
with open(output_file, "w") as file:
    for i, angle, direction in results:
        file.write(f"Photo {i:04}: Angle = {angle:.2f} degrees, Direction = {direction}\n")

print(f"Vector angles with direction written to {output_file}")

