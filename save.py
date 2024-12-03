import os
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the folder path
folder_path = "tests"

# Create a folder to save output images and 3D plots
output_folder = "output_images"
os.makedirs(output_folder, exist_ok=True)

# Path for the output text file
output_text_file = "circles_output.txt"

# Initialize variables
points = []
temp_circle = None
circle_created = False
active_point_index = -1  # Index of the active point for adjustment
z_axis_index = 0  # To keep track of each frame's z position

# Fixed center point (assuming the same for all images)
fixed_center = (950, 899)  # Replace with the correct center coordinates

# Initialize the 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_title("3D Vector Visualization of Rotational Movement")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Time")

# Function to handle mouse events for point selection
def select_points(event, x, y, flags, param):
    global points, active_point_index, circle_created

    if not circle_created:  # Allow one circle per image
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(points) < 3:
                points.append([x, y])  # Store point as a mutable list [x, y]
                active_point_index = len(points) - 1  # Set the current point as active
                update_display()

# Function to update the display with current points and circle
def update_display():
    global img_display, temp_circle

    # Copy the original image for display
    temp_display = img_display.copy()

    # Draw all points
    for i, point in enumerate(points):
        color = (0, 0, 255) if i != active_point_index else (0, 255, 255)  # Highlight active point
        cv2.circle(temp_display, tuple(point), 5, color, -1)

    # Draw the circle if we have three points
    if len(points) == 3:
        temp_circle = create_circle_from_points(points[0], points[1], points[2])
        draw_circle(temp_circle, temp_display)
        draw_perpendicular_vector(points[0], points[1], temp_display)

    cv2.imshow("Interactive Circle Display", temp_display)

# Function to create a circle from three points
def create_circle_from_points(p1, p2, p3):
    ax, ay = p1
    bx, by = p2
    cx, cy = p3

    mid_ab = ((ax + bx) / 2, (ay + by) / 2)
    mid_bc = ((bx + cx) / 2, (by + cy) / 2)
    slope_ab = (by - ay) / (bx - ax) if bx != ax else None
    slope_bc = (cy - by) / (cx - bx) if cx != bx else None

    perp_slope_ab = -1 / slope_ab if slope_ab else 0
    perp_slope_bc = -1 / slope_bc if slope_bc else 0

    if perp_slope_ab is not None and perp_slope_bc is not None:
        center_x = (mid_bc[1] - mid_ab[1] + perp_slope_ab * mid_ab[0] - perp_slope_bc * mid_bc[0]) / (perp_slope_ab - perp_slope_bc)
        center_y = mid_ab[1] + perp_slope_ab * (center_x - mid_ab[0])
    else:
        center_x = mid_ab[0] if slope_ab is None else mid_bc[0]
        center_y = mid_bc[1] if slope_bc is None else mid_ab[1] + perp_slope_ab * (center_x - mid_ab[0])

    radius = int(np.sqrt((center_x - ax) ** 2 + (center_y - ay) ** 2))
    return ((int(center_x), int(center_y)), radius)

# Function to draw the circle on the image
def draw_circle(circle, img):
    center, radius = circle
    cv2.circle(img, center, radius, (255, 0, 0), 2)  # Circle in blue
    cv2.circle(img, center, 5, (0, 255, 0), -1)  # Center in green

# Add these global variables to store the vector endpoint
end_x, end_y = None, None

# Function to draw a perpendicular vector from the midpoint of the line between p1 and p2
def draw_perpendicular_vector(p1, p2, img):
    global end_x, end_y  # Declare the variables as global to access them outside this function
    midpoint = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
    circle_center = temp_circle[0]  # Get the center of the generated circle

    # Calculate direction from midpoint to circle center
    dx = circle_center[0] - midpoint[0]
    dy = circle_center[1] - midpoint[1]

    vector_length = 50
    end_x = midpoint[0] + int(dx * vector_length / np.hypot(dx, dy))
    end_y = midpoint[1] + int(dy * vector_length / np.hypot(dx, dy))

    # Draw the perpendicular vector
    cv2.arrowedLine(img, midpoint, (end_x, end_y), (0, 255, 255), 2, tipLength=0.1)

# Function to finalize and save the image and text details
# Function to finalize and save the image and text details
def finalize_and_save(radius, angle_degrees, filename):
    global end_x, end_y  # Use the global vector endpoint variables

    # Copy the final display image that contains all drawn elements
    final_display = img_display.copy()

    # Draw the circle and vector again to ensure they are saved
    if temp_circle:
        draw_circle(temp_circle, final_display)
        draw_perpendicular_vector(points[0], points[1], final_display)

    # Add text annotations with the radius, angle, and vector coordinates
    cv2.putText(final_display, f"Radius: {radius}", (800, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(final_display, f"Angle α: {angle_degrees:.2f}°", (800, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Get the midpoint used for the vector and log its coordinates
    midpoint = ((points[0][0] + points[1][0]) // 2, (points[0][1] + points[1][1]) // 2)
    cv2.putText(final_display, f"Perpendicular Start: {midpoint}", (800, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(final_display, f"Perpendicular End: ({end_x}, {end_y})", (800, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Save the current state of final_display (which already has all the drawings)
    output_image_path = os.path.join(output_folder, f"final_circle_{filename}")
    cv2.imwrite(output_image_path, final_display)

    # Log details to text file
    with open(output_text_file, "a") as f:
        f.write(f"{filename}:\n")
        f.write(f"  Center: {temp_circle[0]}\n")
        f.write(f"  Radius: {radius}\n")
        f.write(f"  Angle α (in degrees): {angle_degrees:.2f}\n\n")
    print(f"Saved: {filename}")

# Process each image in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(('.png', '.jpg', '.jpeg', '.tiff')):
        img_path = os.path.join(folder_path, filename)
        img = cv2.imread(img_path)

        # Reset variables for each new image
        points.clear()
        temp_circle = None
        circle_created = False
        active_point_index = -1
        img_display = img.copy()

        cv2.imshow("Interactive Circle Display", img_display)
        cv2.setMouseCallback("Interactive Circle Display", select_points)

        while True:
            key = cv2.waitKey(0) & 0xFF

            # Select which point to adjust (1, 2, or 3)
            if key == ord('1') and len(points) > 0:
                active_point_index = 0
            elif key == ord('2') and len(points) > 1:
                active_point_index = 1
            elif key == ord('3') and len(points) > 2:
                active_point_index = 2

            # WASD to adjust the selected point
            elif key == ord('w') and active_point_index != -1:  # Move up
                points[active_point_index][1] -= 1
            elif key == ord('a') and active_point_index != -1:  # Move left
                points[active_point_index][0] -= 1
            elif key == ord('s') and active_point_index != -1:  # Move down
                points[active_point_index][1] += 1
            elif key == ord('d') and active_point_index != -1:  # Move right
                points[active_point_index][0] += 1

            # Enter to confirm position of the current point
            elif key == 13:  # Enter key
                if len(points) == 3:  # If all three points are set, finalize
                    # Finalize and save the output using actual radius and angle values
                    if temp_circle:
                        circle_center, radius = temp_circle

                        if radius >= 156:  # Ensure the value is within a valid range for arccos
                            angle_degrees = math.degrees(math.acos(166 / radius))
                        else:
                            angle_degrees = 0

                        finalize_and_save(radius=radius, angle_degrees=angle_degrees, filename=filename)

                        # Mark that a circle has been created for this image
                        circle_created = True
                        break
                else:
                    active_point_index = len(points)  # Move to the next point

            # Update display with any changes
            update_display()

            # ESC to reset the current image processing
            if key == 27:  # ESC key to reset the circle selection
                print("Resetting circle selection...")
                points.clear()
                temp_circle = None
                circle_created = False
                active_point_index = -1
                img_display = img.copy()
                cv2.imshow("Interactive Circle Display", img_display)

                # Stop current while loop, effectively moving to the next image
                break

# Close all OpenCV windows
cv2.destroyAllWindows()
print("Process completed. Images saved with circles and perpendicular vectors.")

