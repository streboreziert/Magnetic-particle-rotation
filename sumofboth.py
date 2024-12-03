import pandas as pd

# Define file paths
vectorsum_file = "vectorsum.txt"  # Update this path if the file is not in the same folder
spolessum_file = "spolessum.txt"  # Update this path if needed

# Read the input files
vectorsum_data = pd.read_csv(vectorsum_file, delimiter=",", header=0, names=["Angle", "Direction", "Cumulative Angle"])
spolessum_data = pd.read_csv(spolessum_file, delimiter="\t")

# Ensure cumulative angles are numeric
vectorsum_data['Cumulative Angle'] = pd.to_numeric(vectorsum_data['Cumulative Angle'], errors='coerce')
spolessum_data['Cumulative Angle'] = pd.to_numeric(spolessum_data['Cumulative Angle'], errors='coerce')

# Drop NaN values from both datasets
vectorsum_data.dropna(subset=['Cumulative Angle'], inplace=True)
spolessum_data.dropna(subset=['Cumulative Angle'], inplace=True)

# Trim the datasets to match the minimum length
min_length = min(len(vectorsum_data), len(spolessum_data))
vectorsum_cum_angles = vectorsum_data['Cumulative Angle'][:min_length].reset_index(drop=True)
spolessum_cum_angles = spolessum_data['Cumulative Angle'][:min_length].reset_index(drop=True)

# Compute the difference
difference = vectorsum_cum_angles - spolessum_cum_angles

# Prepare the output DataFrame
output = pd.DataFrame({
    "Vectorsum Cumulative Angle": vectorsum_cum_angles,
    "Spolessum Cumulative Angle": spolessum_cum_angles,
    "Difference": difference
})

# Save the output to a text file
output_file = "difference_cumulative_angles.txt"
output.to_csv(output_file, sep="\t", index=False)

print(f"Difference saved to {output_file}")

