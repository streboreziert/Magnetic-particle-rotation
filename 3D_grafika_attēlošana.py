import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

vectors = []
vectors_file_path = 'vectors.txt'  
with open(vectors_file_path, 'r') as vf:
    for line in vf.readlines():
        if ':' in line:
            parts = line.split(':')
            coords = eval(parts[1].strip())  
            vectors.append(coords)

angles_file_path = 'extracted_values_with_angles.txt' 
angles_data = np.loadtxt(angles_file_path, delimiter=",", skiprows=1, usecols=3)
angles_rad = np.radians(angles_data)  # Convert angles to radians

vectors = np.array(vectors[:300]) 
angles_rad = angles_rad[:300]  
magnitudes = np.linalg.norm(vectors, axis=1)
z = magnitudes * np.sin(angles_rad)  
unit_vectors = np.column_stack((vectors, z))  

magnitudes_3d = np.linalg.norm(unit_vectors, axis=1)
unit_vectors = unit_vectors / magnitudes_3d[:, np.newaxis]

x_scale_factor = 5  
unit_vectors[:, 0] *= x_scale_factor

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = np.outer(np.cos(u), np.sin(v)) * x_scale_factor 
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x, y, z, color='c', alpha=0.1, edgecolor='w')

ax.plot(unit_vectors[:, 0], unit_vectors[:, 1], unit_vectors[:, 2],
        color='r', linewidth=2, label="Vector Path (Scaled on X-axis)")

ax.set_xlabel('X (scaled)')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Path of Vector Ends with Scaled X-axis')
ax.legend()
plt.show()

