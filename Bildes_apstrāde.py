import os
import cv2
import numpy as np
import math

folder_path = "tests"
output_folder = "output_images"
os.makedirs(output_folder, exist_ok=True)
output_text_file = "ellipse_output.txt"

# Variables
points = []
temp_circle = None
generated_ellipse = None
ellipse_created = False
active_point_index = -1  
p1_angle = None  
p2_angle = None  

# Mouse events for point selection
def select_points(event, x, y, flags, param):
    global points, active_point_index, ellipse_created, p1_angle, p2_angle

    if not ellipse_created and temp_circle is not None:
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(points) < 2:  
                center, radius = temp_circle
                distance_to_center = np.linalg.norm(np.array([x, y]) - np.array(center))
                
                if abs(distance_to_center - radius) <= 10:
                    points.append([x, y])
                    if len(points) == 1:
                        p1_angle = math.atan2(y - center[1], x - center[0])
                    elif len(points) == 2:
                        p2_angle = math.atan2(y - center[1], x - center[0])
                    active_point_index = len(points) - 1  # Set active point
                    update_display()
                else:
                    print("Point must be on the detected circle's circumference.")
            elif len(points) == 2:  
                points.append([x, y])
                active_point_index = 2
                ellipse_created = True  
                update_display()

# Update the display
def update_display():
    global img_display, temp_circle, generated_ellipse

    temp_display = img_display.copy()

    # Draw temporary circle or ellipse
    if temp_circle is not None:
        center, radius = temp_circle
        cv2.circle(temp_display, center, radius, (0, 255, 0), 2)  # Circle in green

    # Draw all points
    for i, point in enumerate(points):
        color = (0, 0, 255) if i != active_point_index else (0, 255, 255)  
        cv2.circle(temp_display, tuple(point), 5, color, -1)

    if len(points) >= 2:
        cv2.line(temp_display, tuple(points[0]), tuple(points[1]), (0, 255, 255), 2)  
        if generated_ellipse:
            draw_perpendicular_vector(points[0], points[1], points[2], temp_display, generated_ellipse[0])  

    if len(points) == 3:
        generated_ellipse = create_ellipse_from_points(points[0], points[1], points[2])
        if generated_ellipse:
            draw_ellipse(generated_ellipse, temp_display)

    cv2.imshow("Interactive Ellipse Display", temp_display)

# Function for HoughCircles to detect the most prominent circle
def detect_most_voted_circle(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(
        gray_img, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100,
        param1=50, param2=30, minRadius=100, maxRadius=500
    )

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        most_voted_circle = circles[0]
        print(f"Most voted circle: Center={most_voted_circle[:2]}, Radius={most_voted_circle[2]}")
        return (most_voted_circle[:2], most_voted_circle[2])
    else:
        print("No circles detected.")
        return None

# Function to create an ellipse from three points
def create_ellipse_from_points(p1, p2, p3):
    # Calculate the center as the midpoint between p1 and p2
    center = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
    
    # Calculate the semi-major axis length as half the distance between p1 and p2
    semi_major_axis = int(np.linalg.norm(np.array(p1) - np.array(p2)) / 2)
    
    # Calculate the distance from the center to p3 for the semi-minor axis
    semi_minor_axis = int(np.linalg.norm(np.array(center) - np.array(p3)))

    # Calculate the angle of rotation for the ellipse based on p1 and p2
    angle = math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))

    print(f"Ellipse Center: {center}, Semi-Major Axis: {semi_major_axis}, Semi-Minor Axis: {semi_minor_axis}, Angle: {angle}")

    return (center, semi_major_axis, semi_minor_axis, angle)

# Function to draw the ellipse
def draw_ellipse(ellipse, img, color=(0, 0, 0)):
    center, semi_major_axis, semi_minor_axis, angle = ellipse
    cv2.ellipse(img, center, (semi_major_axis, semi_minor_axis), angle, 0, 360, color, 2)
    cv2.circle(img, center, 5, color, -1)

# Function to draw a perpendicular vector from the midpoint of the line between p1 and p2, pointing away from p3
def draw_perpendicular_vector(p1, p2, p3, img, color=(0, 255, 0), vector_length=50):
    # Calculate the midpoint between p1 and p2
    midpoint = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)

    # Calculate the direction vector from p1 to p2
    direction_p1_p2 = (p2[0] - p1[0], p2[1] - p1[1])

    # Rotate the direction vector by 90 degrees to get the perpendicular direction
    perpendicular_direction = (-direction_p1_p2[1], direction_p1_p2[0])

    # Calculate the vector from midpoint to p3
    direction_midpoint_p3 = (p3[0] - midpoint[0], p3[1] - midpoint[1])

    # Determine if the perpendicular vector should point away from p3
    # by checking the dot product with direction_midpoint_p3
    dot_product = (perpendicular_direction[0] * direction_midpoint_p3[0] +
                   perpendicular_direction[1] * direction_midpoint_p3[1])

    # If dot product is positive, reverse the perpendicular direction
    if dot_product > 0:
        perpendicular_direction = (-perpendicular_direction[0], -perpendicular_direction[1])

    # Normalize the perpendicular direction vector
    norm = np.sqrt(perpendicular_direction[0] ** 2 + perpendicular_direction[1] ** 2)
    if norm == 0:
        print("Warning: Perpendicular vector has zero length.")
        return

    # Scale the perpendicular direction vector to the desired length
    vector = (int(perpendicular_direction[0] / norm * vector_length),
              int(perpendicular_direction[1] / norm * vector_length))

    # Calculate the end point of the vector
    end_x = midpoint[0] + vector[0]
    end_y = midpoint[1] + vector[1]

    # Draw the arrowed line
    cv2.arrowedLine(img, midpoint, (end_x, end_y), color, 2, tipLength=0.2)
def update_p1_p2_positions():
    if temp_circle is None:
        return
    
    center, radius = temp_circle
    p1_x = int(center[0] + radius * np.cos(p1_angle))
    p1_y = int(center[1] + radius * np.sin(p1_angle))
    p2_x = int(center[0] + radius * np.cos(p2_angle))
    p2_y = int(center[1] + radius * np.sin(p2_angle))

    # Update points with the new positions
    points[0] = [p1_x, p1_y]
    points[1] = [p2_x, p2_y]

def save_results(image_name, img, angle, custom_ellipse):
    output_image_path = os.path.join(output_folder, f"output_{image_name}")
    
    if custom_ellipse:
        draw_ellipse(custom_ellipse, img, color=(0, 255, 0))
    if len(points) >= 2:
        cv2.line(img, tuple(points[0]), tuple(points[1]), (0, 0, 0), 2) 
        if custom_ellipse:
            draw_perpendicular_vector(points[0], points[1], points[2], img, color=(0, 0, 0))  

    # Annotate points and angle on the image in black
    for i, point in enumerate(points):
        cv2.putText(img, f"p{i+1}: {point}", (point[0] + 5, point[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    if angle is not None:
        cv2.putText(img, f"Angle: {angle:.2f} degrees", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    if custom_ellipse:
        center, semi_major_axis, semi_minor_axis, ellipse_angle = custom_ellipse
        cv2.putText(img, f"Ellipse Center: {center}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.putText(img, f"Semi-Major Axis: {semi_major_axis}", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        cv2.putText(img, f"Semi-Minor Axis: {semi_minor_axis}", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    cv2.imwrite(output_image_path, img)
    print(f"Saved processed image to: {output_image_path}")

    # Save data to text file
    with open(output_text_file, "a") as f:
        f.write(f"{image_name}:\n")
        f.write(f"  p1: {points[0]}, p2: {points[1]}, p3: {points[2]}\n")
        if angle is not None:
            f.write(f"  Angle: {angle:.2f} degrees\n")
        if custom_ellipse:
            f.write(f"  Ellipse Center: {center}, Semi-Major Axis: {semi_major_axis}, Semi-Minor Axis: {semi_minor_axis}, Rotation Angle: {ellipse_angle}\n\n")
    print(f"Saved data to text file: {output_text_file}")

# Main loop to process each image
for filename in os.listdir(folder_path):
    if filename.endswith(('.png', '.jpg', '.jpeg', '.tiff')):
        img_path = os.path.join(folder_path, filename)
        img = cv2.imread(img_path)

        temp_circle = detect_most_voted_circle(img)

        points.clear()
        ellipse_created = False
        active_point_index = -1
        p1_angle, p2_angle = None, None  
        img_display = img.copy()
        update_display()

        cv2.setMouseCallback("Interactive Ellipse Display", select_points)

        while True:
            key = cv2.waitKey(0) & 0xFF

            if key == ord('1') and len(points) > 0:
                active_point_index = 0
            elif key == ord('2') and len(points) > 1:
                active_point_index = 1
            elif key == ord('3') and len(points) > 2:
                active_point_index = 2

            elif key in [ord('w'), ord('s')] and active_point_index in [0, 1] and len(points) > 1:
                step = 0.01 if key == ord('w') else -0.01  
                if active_point_index == 0:
                    p1_angle += step
                elif active_point_index == 1:
                    p2_angle += step
                update_p1_p2_positions()
                update_display()
            
            elif key in [ord('w'), ord('a'), ord('s'), ord('d')] and active_point_index == 2:
                if key == ord('w'):  
                    points[2][1] -= 1
                elif key == ord('a'):  
                    points[2][0] -= 1
                elif key == ord('s'):  
                    points[2][1] += 1
                elif key == ord('d'):  
                    points[2][0] += 1

            elif key == 13:  
                if len(points) == 3 and temp_circle:  
                    generated_ellipse = create_ellipse_from_points(points[0], points[1], points[2])
                    save_results(filename, img_display, None, generated_ellipse)
                    break

            update_display()

            if key == 27:  
                print("Resetting ellipse selection...")
                points.clear()
                ellipse_created = False
                active_point_index = -1
                img_display = img.copy()
                update_display()
                break

cv2.destroyAllWindows()
print("Process completed.")

