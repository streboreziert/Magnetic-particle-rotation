import re
import numpy as np
import matplotlib.pyplot as plt

def parse_data(filename):
    data = []
    with open(filename, 'r') as file:
        content = file.read()
        
        pattern = r"p1: \[(\d+), (\d+)\], p2: \[(\d+), (\d+)\]"
        matches = re.findall(pattern, content)
        for match in matches:
            p1 = np.array([int(match[0]), int(match[1])])
            p2 = np.array([int(match[2]), int(match[3])])
            data.append((p1, p2))
    return data

def calculate_perpendicular_vector(p1, p2):
    direction = p2 - p1
    perpendicular_direction = np.array([-direction[1], direction[0]])
    perpendicular_direction_normalized = perpendicular_direction / np.linalg.norm(perpendicular_direction)
    return perpendicular_direction_normalized

def plot_all_vectors_from_origin(data, origin, vector_length=100, output_filename="perpendicular_vectors.png"):
    plt.figure(figsize=(10, 8))
    
    for p1, p2 in data:
        
        unit_vector = calculate_perpendicular_vector(p1, p2)
        endpoint = origin + vector_length * unit_vector
        
        
        plt.arrow(origin[0], origin[1], endpoint[0] - origin[0], endpoint[1] - origin[1], 
                  head_width=10, head_length=10, color='green', alpha=0.6)

    
    plt.scatter(origin[0], origin[1], color='black', label="Origin Point")
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title("Perpendicular Vectors with Fixed Length from a Single Origin")
    plt.legend()
    plt.grid(True)

    
    plt.savefig(output_filename, format='png')
    plt.show()
    print(f"Image saved as {output_filename}")


filename = 'circles_output.txt'  
origin = np.array([0, 0])  
data = parse_data(filename)
plot_all_vectors_from_origin(data, origin)

