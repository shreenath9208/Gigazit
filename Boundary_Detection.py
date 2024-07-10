import cv2         # used for the images task and processing the image data
import numpy as np # used for the numerical task and processing statistical data

def detect_paint_boundary_crossing(image, boundary_type='rectangle'):
    # Convert the image to the HSV color space for easier color segmentation
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the color range for the red boundary in HSV
    # This range includes two segments to cover the red color properly
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    mask_red1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask_red2 = cv2.inRange(hsv_image, lower_red2, upper_red2)

    # Combine the two red masks to form the complete red boundary mask
    red_boundary_mask = mask_red1 + mask_red2

    # Define the color range for the blue paint in HSV
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])
    # Create a mask for the blue paint
    blue_paint_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

    # Find contours of the red boundary in the mask
    contours, _ = cv2.findContours(red_boundary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("No red boundary found")

    # Assume the largest contour is the boundary of the red shape
    if boundary_type == 'rectangle':
        boundary_contour = max(contours, key=cv2.contourArea)
    elif boundary_type == 'circle':
        # Fit a circle around the boundary
        (x, y), radius = cv2.minEnclosingCircle(contours[0])
        boundary_contour = np.array([[int(x), int(y)]])
    elif boundary_type == 'ellipse':
        # Fit an ellipse around the boundary
        ellipse = cv2.fitEllipse(contours[0])
        boundary_contour = np.array(cv2.ellipse2Poly((int(ellipse[0][0]), int(ellipse[0][1])),
                                                     (int(ellipse[1][0] / 2), int(ellipse[1][1] / 2)),
                                                     int(ellipse[2]), 0, 360, 5), dtype=np.int32)
    else:
        raise ValueError("Unsupported boundary type")

    # Check if any blue paint pixels are outside the boundary
    paint_crosses_boundary = False
    # Get the coordinates of blue paint pixels
    blue_paint_coords = np.column_stack(np.where(blue_paint_mask > 0))

    for coord in blue_paint_coords:
        # Use (coord[1], coord[0]) for (x, y) format
        if cv2.pointPolygonTest(boundary_contour, (int(coord[1]), int(coord[0])), False) < 0:
            paint_crosses_boundary = True
            break

    # Check the flag value to determine if paint crosses the boundary
    if paint_crosses_boundary:
        print("Border Crossed")
    else:
        print("Within Boundaries")

    # Visualization of the result
    visualization = image.copy()
    cv2.drawContours(visualization, [boundary_contour], -1, (0, 255, 0), 2)
    for coord in blue_paint_coords:
        if cv2.pointPolygonTest(boundary_contour, (int(coord[1]), int(coord[0])), False) < 0:
            cv2.circle(visualization, (coord[1], coord[0]), 2, (0, 0, 255), -1)

    # Display the visualization image
    cv2.imshow("Visualization", visualization)
    cv2.waitKey(0)  # Wait for a key press to close the window
    cv2.destroyAllWindows()  # Close all OpenCV windows

def create_rectangle():
    # Create a blank white image
    image = np.ones((500, 500, 3), dtype=np.uint8) * 255

    # Draw a red rectangular boundary
    cv2.rectangle(image, (100, 100), (400, 400), (0, 0, 255), 5)

    return image

def create_circle_inside(image):
    # Draw a blue circle inside the boundary
    cv2.circle(image, (250, 250), 100, (255, 0, 0), -1)
    return image

def create_circle_crossing(image):
    # Draw another blue circle crossing the boundary
    cv2.circle(image, (450, 250), 100, (255, 0, 0), -1)
    return image

def create_ellipse(image):
    # Create a blank white image
    image = np.ones((500, 500, 3), dtype=np.uint8) * 255

    # Draw a red ellipse boundary
    cv2.ellipse(image, (250, 250), (150, 100), 0, 0, 360, (0, 0, 255), 5)

    return image

if __name__ == '__main__':
    # Example usage:
    image_rectangle = create_rectangle()
    image_circle_inside = create_circle_inside(image_rectangle.copy())
    image_circle_crossing = create_circle_crossing(image_rectangle.copy())
    image_ellipse = create_ellipse(np.ones((500, 500, 3), dtype=np.uint8) * 255)

    try:
        # Test different shapes
        detect_paint_boundary_crossing(image_circle_inside, boundary_type='circle')
        detect_paint_boundary_crossing(image_circle_crossing, boundary_type='circle')
        detect_paint_boundary_crossing(image_rectangle, boundary_type='rectangle')
        detect_paint_boundary_crossing(image_ellipse, boundary_type='ellipse')
    except ValueError as e:
        print(e)
