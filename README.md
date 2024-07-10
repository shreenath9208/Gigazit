# Paint Boundary Crossing Detection


# Installation:

		Ensure you have Python 3 installed along with the necessary libraries:
     		code:
        		pip install opencv-python numpy

# Functionality:

		This Python script analyzes images to detect whether blue paint has crossed a specified boundary shape (rectangle, circle, or ellipse). It utilizes OpenCV for image processing and contour detection.

# Color Representation:

		Red Boundary: Detected using the HSV color space to handle variations in lighting and shade.
		Blue Paint: Similarly detected in HSV to ensure accurate segmentation.

# Image Structure:
  The script supports multiple boundary shapes:

		Rectangle: A red rectangular boundary.
		Circle: A red circular boundary.
		Ellipse: A red elliptical boundary.
		Blue paint circles are drawn inside or crossing these boundaries for testing purposes.

# Expected Output:

		"Border Crossed": If any blue paint pixels are detected outside the specified boundary.
		"Within Boundaries": If all blue paint pixels are contained within the specified boundary.

# Usage:

		Install Python and required libraries.
		Run the script.
		Select the test image scenario (inside or crossing boundary) when prompted.

# Files:

		Boundary_Detection.py: Main script file containing the detection logic.
		README.md: This file providing an overview of the script's functionality and usage.
