import os
import cv2
import numpy as np
import math

folder_path = "tests"
output_folder = "output_images"
os.makedirs(output_folder, exist_ok=True)
output_text_file = "circles_output.txt"

# variables
points = []
temp_circle = None
generated_circle = None
circle_created = False
active_point_index = -1  
p1_angle = None  
p2_angle = None  

# mouse events for point selection
def select_points(event, x, y, flags, param):
    global points, active_point_index, circle_created, p1_angle, p2_angle

    if not circle_created and temp_circle is not None:
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(points) < 2:  
                center, radius = temp_circle
                distance_to_center = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
                
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
                circle_created = True  
                update_display()

# update the display
def update_display():
    global img_display, temp_circle, generated_circle

    
    temp_display = img_display.copy()

    
    if temp_circle is not None:
        center, radius = temp_circle
        cv2.circle(temp_display, center, radius, (0, 255, 0), 2)  # Circle in green

    # Draw all points
    for i, point in enumerate(points):
        color = (0, 0, 255) if i != active_point_index else (0, 255, 255)  
        cv2.circle(temp_display, tuple(point), 5, color, -1)

    if len(points) >= 2:
        cv2.line(temp_display, tuple(points[0]), tuple(points[1]), (0, 255, 255), 2)  
        if generated_circle:
            draw_inward_vector(points[0], points[1], temp_display, generated_circle[0])  

    if len(points) == 3:
        generated_circle = create_circle_from_points(points[0], points[1], points[2])
        if generated_circle:
            draw_circle(generated_circle, temp_display)

    cv2.imshow("Interactive Circle Display", temp_display)

# Function for HoughCircles
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

# Function to create a circle
def create_circle_from_points(p1, p2, p3):
    ax, ay = p1
    bx, by = p2
    cx, cy = p3

    area = ax * (by - cy) + bx * (cy - ay) + cx * (ay - by)
    if abs(area) < 1e-6:  
        return None

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

# Function to draw the circle 
def draw_circle(circle, img, color=(0, 0, 0)):
    center, radius = circle
    cv2.circle(img, center, radius, color, 2)  
    cv2.circle(img, center, 5, color, -1)  
# Function to calculate angle using the formula 
def calculate_cosine_angle(radius):
    if radius >= 166:
        cos_alpha = 166 / radius
        angle = math.degrees(math.acos(cos_alpha))
        return angle
    else:
        print("Warning: Radius is too small to calculate angle with cos(alpha) = 166 / radius")
        return None

# Function to draw a vector from the midpoint of the line between p1 and p2 toward the generated circle center
def draw_inward_vector(p1, p2, img, center, color=(0, 255, 0)):
    midpoint = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)

    direction_to_center = (center[0] - midpoint[0], center[1] - midpoint[1])

    vector_length = 50
    norm = np.sqrt(direction_to_center[0] ** 2 + direction_to_center[1] ** 2)
    vector = (int(direction_to_center[0] / norm * vector_length), int(direction_to_center[1] / norm * vector_length))

    end_x = midpoint[0] + vector[0]
    end_y = midpoint[1] + vector[1]

    cv2.arrowedLine(img, midpoint, (end_x, end_y), color, 2, tipLength=0.1)

def update_p1_p2_positions():
    center, radius = temp_circle
    p1_x = int(center[0] + radius * np.cos(p1_angle))
    p1_y = int(center[1] + radius * np.sin(p1_angle))
    p2_x = int(center[0] + radius * np.cos(p2_angle))
    p2_y = int(center[1] + radius * np.sin(p2_angle))

    points[0] = [p1_x, p1_y]
    points[1] = [p2_x, p2_y]

def save_results(image_name, img, angle, custom_circle):
    output_image_path = os.path.join(output_folder, f"output_{image_name}")
    
    if custom_circle:
        draw_circle(custom_circle, img, color=(0, 255, 0))
    if len(points) >= 2:
        cv2.line(img, tuple(points[0]), tuple(points[1]), (0, 0, 0), 2) 
        if custom_circle:
            draw_inward_vector(points[0], points[1], img, custom_circle[0], color=(0, 0, 0))  

    # Annotate points and angle on the image in black
    for i, point in enumerate(points):
        cv2.putText(img, f"p{i+1}: {point}", (point[0] + 5, point[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    if angle is not None:
        cv2.putText(img, f"Angle: {angle:.2f} degrees", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    if custom_circle:
        center, radius = custom_circle
        cv2.putText(img, f"Circle Center: {center}, Radius: {radius}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    cv2.imwrite(output_image_path, img)
    print(f"Saved processed image to: {output_image_path}")

    # Save data to text file
    with open(output_text_file, "a") as f:
        f.write(f"{image_name}:\n")
        f.write(f"  p1: {points[0]}, p2: {points[1]}, p3: {points[2]}\n")
        if angle is not None:
            f.write(f"  Angle: {angle:.2f} degrees\n")
        if custom_circle:
            f.write(f"  Circle Center: {center}, Radius: {radius}\n\n")
    print(f"Saved data to text file: {output_text_file}")

# Main loop to process each image
for filename in os.listdir(folder_path):
    if filename.endswith(('.png', '.jpg', '.jpeg', '.tiff')):
        img_path = os.path.join(folder_path, filename)
        img = cv2.imread(img_path)

        temp_circle = detect_most_voted_circle(img)

        points.clear()
        circle_created = False
        active_point_index = -1
        p1_angle, p2_angle = None, None  
        img_display = img.copy()
        update_display()

        cv2.setMouseCallback("Interactive Circle Display", select_points)

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
                if key == ord('w'):  # Move up
                    points[2][1] -= 1
                elif key == ord('a'):  # Move left
                    points[2][0] -= 1
                elif key == ord('s'):  # Move down
                    points[2][1] += 1
                elif key == ord('d'):  # Move right
                    points[2][0] += 1

            elif key == 13:  # Enter key
                if len(points) == 3 and temp_circle:  
                    generated_circle = create_circle_from_points(points[0], points[1], points[2])
                    angle = calculate_cosine_angle(generated_circle[1]) if generated_circle else None
                    save_results(filename, img_display, angle, generated_circle)
                    break

            update_display()

            if key == 27:  
                print("Resetting circle selection...")
                points.clear()
                circle_created = False
                active_point_index = -1
                img_display = img.copy()
                update_display()
                break

cv2.destroyAllWindows()
print("Process completed.")

