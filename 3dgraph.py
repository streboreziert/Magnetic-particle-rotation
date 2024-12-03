import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load vectors from the file
vectors = []

# Process the vectors file
vectors_file_path = 'vectors.txt'  # Adjust path if necessary
with open(vectors_file_path, 'r') as vf:
    for line in vf.readlines():
        if ':' in line:
            parts = line.split(':')
            coords = eval(parts[1].strip())  # Parse 2D vectors
            vectors.append(coords)

# Load angles from the file
angles_file_path = 'extracted_values_with_angles.txt'  # Adjust path if necessary
angles_data = np.loadtxt(angles_file_path, delimiter=",", skiprows=1, usecols=3)
angles_rad = np.radians(angles_data)  # Convert angles to radians

# Calculate z-coordinates based on the angle and vector magnitude
vectors = np.array(vectors[:300])  # Take vectors from frame 1 to 300
angles_rad = angles_rad[:300]  # Take corresponding angles
magnitudes = np.linalg.norm(vectors, axis=1)
z = magnitudes * np.sin(angles_rad)  # Calculate z-coordinate
unit_vectors = np.column_stack((vectors, z))  # Combine x, y, z into a single array

# Normalize vectors to the unit sphere
magnitudes_3d = np.linalg.norm(unit_vectors, axis=1)
unit_vectors = unit_vectors / magnitudes_3d[:, np.newaxis]

# Scale the x-coordinates to make the vectors appear longer along the x-axis
x_scale_factor = 5  # Adjust this factor to control the x-axis scaling
unit_vectors[:, 0] *= x_scale_factor

# Create 3D spherical plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot the unit sphere
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = np.outer(np.cos(u), np.sin(v)) * x_scale_factor  # Scale sphere x-coordinates
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x, y, z, color='c', alpha=0.1, edgecolor='w')

# Plot the path of the vector ends as a line
ax.plot(unit_vectors[:, 0], unit_vectors[:, 1], unit_vectors[:, 2],
        color='r', linewidth=2, label="Vector Path (Scaled on X-axis)")

# Set labels and title
ax.set_xlabel('X (scaled)')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Path of Vector Ends with Scaled X-axis')
ax.legend()

plt.show()

