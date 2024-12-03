import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import interp1d

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

# Use only the first 300 frames
vectors = np.array(vectors[:300])  # Take vectors from frame 1 to 300
angles_rad = angles_rad[:300]  # Take corresponding angles
magnitudes = np.linalg.norm(vectors, axis=1)
z = magnitudes * np.sin(angles_rad)  # Calculate z-coordinate
unit_vectors = np.column_stack((vectors, z))  # Combine x, y, z into a single array

# Normalize vectors to the unit sphere
magnitudes_3d = np.linalg.norm(unit_vectors, axis=1)
unit_vectors = unit_vectors / magnitudes_3d[:, np.newaxis]

# Interpolate to add smoothness
frames = np.arange(unit_vectors.shape[0])
interp_func = interp1d(frames, unit_vectors, axis=0, kind='cubic')  # Cubic interpolation
smooth_frames = np.linspace(0, frames[-1], 1000)  # Increase resolution
smooth_unit_vectors = interp_func(smooth_frames)  # Get smoothed vectors

# Create 3D spherical plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot the unit sphere
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x, y, z, color='c', alpha=0.1, edgecolor='w')

# Plot the path of the vector ends as a smoothed line
ax.plot(smooth_unit_vectors[:, 0], smooth_unit_vectors[:, 1], smooth_unit_vectors[:, 2],
        color='r', linewidth=2, label="Smoothed Vector Path")

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Smoothed Path of Vector Ends on a Unit Sphere')
ax.legend()

plt.show()

