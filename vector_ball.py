import re

def compute_perpendicular_vector(p1, p2, p3):
    # Calculate the midpoint between p1 and p2
    midpoint = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]
    
    # Direction vector from p1 to p2
    direction_vector = [p2[0] - p1[0], p2[1] - p1[1]]
    
    # Perpendicular vector to the direction vector
    perpendicular_vector = [-direction_vector[1], direction_vector[0]]
    
    # Vector from midpoint to p3
    to_p3_vector = [p3[0] - midpoint[0], p3[1] - midpoint[1]]
    
    # Determine the correct orientation of the perpendicular vector
    dot_product = (to_p3_vector[0] * perpendicular_vector[0] +
                   to_p3_vector[1] * perpendicular_vector[1])
    
    if dot_product < 0:
        perpendicular_vector = [-perpendicular_vector[0], -perpendicular_vector[1]]
    
    return perpendicular_vector

def parse_coordinates(line):
    # Extract p1, p2, p3 using regex
    coords = re.findall(r"\[([0-9,\s]+)\]", line)
    return [list(map(int, coord.split(','))) for coord in coords]

def process_data(input_file, output_file):
    # Load the input data
    data = []
    with open(input_file, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 2):  # Each entry spans two lines
            line1 = lines[i].strip()
            line2 = lines[i + 1].strip()
            
            # Extract the photo ID from the first line
            photo_id = line1.split('_')[-1].split('.')[0]
            
            # Extract p1, p2, p3 from the second line
            try:
                p1, p2, p3 = parse_coordinates(line2)
                data.append({"Photo": int(photo_id), "p1": p1, "p2": p2, "p3": p3})
            except ValueError:
                print(f"Skipping invalid line: {line2}")
                continue

    # Calculate perpendicular vectors
    results = []
    for entry in data:
        p1, p2, p3 = entry["p1"], entry["p2"], entry["p3"]
        vector = compute_perpendicular_vector(p1, p2, p3)
        results.append({"Photo": entry["Photo"], "Vector": vector})

    # Sort by photo identifier
    results = sorted(results, key=lambda x: x["Photo"])

    # Write results to output file
    with open(output_file, 'w') as file:
        for result in results:
            file.write(f"Photo {result['Photo']:04d}: {result['Vector']}\n")

if __name__ == "__main__":
    # Specify input and output file paths
    input_file = "input.txt"  # Input file name
    output_file = "vectors.txt"  # Output file name
    
    # Process data and generate output
    process_data(input_file, output_file)

