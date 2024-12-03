import pandas as pd
import numpy as np

def normalize_vector(vector):
    """Normalize a vector to have a length of 1."""
    magnitude = np.sqrt(sum(x**2 for x in vector))
    if magnitude == 0:
        return [0, 0, 0]  # Handle zero-length vectors gracefully
    return [x / magnitude for x in vector]

def process_vectors(input_file, output_file):
    # Read the data
    data = pd.read_csv(input_file, delim_whitespace=True)

    # Filter the first 300 entries
    first_300 = data.iloc[:300]

    # Extract relevant columns: time and vectors (Ux, Uy, Uz)
    output_data = first_300[["time", "Ux", "Uy", "Uz"]]

    # Normalize vectors and write to output
    with open(output_file, "w") as file:
        for _, row in output_data.iterrows():
            time = row["time"]
            vector = [row["Ux"], row["Uy"], row["Uz"]]
            normalized_vector = normalize_vector(vector)
            file.write(f"Time: {time}, Vector: {normalized_vector}\n")

if __name__ == "__main__":
    # Specify input and output file paths
    input_file = "power.txt"  # Replace with your input file name
    output_file = "processed_vectors_normalized.txt"  # Replace with your desired output file name
    
    # Process the data and generate output
    process_vectors(input_file, output_file)

