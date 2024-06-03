# Simple-Space
### *A Try at Better Understanding Space*

### Table of Contents

- [Installation](#installation)
- [Structure](#structure)
- [Submodules](#submodules)
    - Points
        - [Dim3 Module](#Dim3-module)
        - Dim2 Module
        - [Circle Module](#Circle-module)
        - [Line Module](#Line-module)
        - [Triangle Module](#Triangle-module)
    - ImageRelated
        - [enhancements.py](#imagerelated-scripts--enhancementspy)
        - [basics.py](#imagerelated-scripts--basicspy)
- [License](#license)
- [Contact](#contact)

## Installation

To use all these utilities, just following Python package should be installed:

```sh
pip install simple-space
```

## Structure

```markdown
simple-space/
│
├── SimpleS/
│   ├── __init__.py
│   ├── utils.py
│   ├── detection.py
│   └── Points/
│       ├── __init__.py
│       ├── Dim3.py
│       ├── Dim2.py
│       ├── Circle.py
│       ├── Line.py
│       ├── Triangle.py
│   └── ImageRelated/
│       ├── __init__.py
│       ├── enhancements.py
│       └── basics.py
├── README.md
├── LICENSE
└── pyproject.toml
```
## Submodules
1. Points

    - Dim3.py:
     Contains basic functions for 3D point data processing and visualization.
    - Dim2.py:
     Contains basic functions for 2D point data processing and visualization.
2. ImageRelated

    - enhancements.py: Provides functions for image enhancement, including erosion and dilation.
    - basics.py: Contains basic image processing utilities like edge detection and color inversion.

## Dim3 Module

The Dim3 module offers tools for visualizing and processing 3D point data in Python, using libraries such as numpy, matplotlib, and scipy.

### Features

- **Rotate 3D Points:** Rotate points around a specified axis by a given angle in degrees.
- **Plot 3D Points/Mesh:** Visualize 3D points or a mesh, with customizable visual attributes.
- **Create Grayscale Image from 3D Points:** Project 3D points onto a 2D plane using the z-coordinate for intensity.
- **Fill Points in Binary Image:** Use morphological dilation to fill gaps in binary images.

### Usage

#### Importing

```python

from SimpleS.Points import Dim3
```
```python
# But I recommend You Simply Use this one:

from SimpleS.Points.Dim3 import *

# This one Lets you use all the functions inside Dim3 module without any initialize word;
# FOR EXAMPLE:

Dim3.rotate_3d_points()

# WOULD BE JUST:

rotate_3d_points()
```
**If you encounter any trouble determining the specifics of an import, such as which functions it includes, simply use the dir() function:**
```python
from SimpleS.Points import Dim3

dir(Dim3)
```
This will show you the names of all functions inside the Dim3 module.

After that, we will return to our simpler method:

```python
from SimpleS.Points.Dim3 import *
```

#### Rotating 3D Points

```python
rotated_points = rotate_3d_points(points, 45, 'z')
```

#### Plotting 3D Points or Mesh

```python
plot_3d_points_using_vertices(vertices, faces)
```


#### Creating a Grayscale Image from 3D Points

```python
image = create_bool_image_from_3d_points(points)
```


#### Filling Points in a Binary Image

```python
filled_image = fill_3d_points(binary_image)
```
For more detailed information on each method, please refer to the inline documentation within the module methods.


## Circle Module

The Circle module provides functions for handling and visualizing circles and arcs.

### Features

-    **Plot Circles Along Arc:** Plot circles along a defined arc.
-    **Calculate Arc Angle:** Calculate the angle between two points on a circle.
-    **Calculate Circle Center:** Determine the center of a circle passing through three points.
-    **Position Along Curve:** Calculate the position of a point along a Bezier curve.
-    **Fit and Plot Polynomial Curve:** Fit and plot a polynomial curve through given points.
-    **Tangent Circles:** Plot tangent circles along a line or between lines.
-    **Smallest Enclosing Circle:** Find the smallest circle that encloses a set of points.

### Usage

```python

from SimpleS.Points.Circle import *

# Plot Circles Along Arc
center = (0, 0)
radius = 5
plot_circles_along_arc(center, radius, 0, 180, 1)

# Calculate Arc Angle
start_point = (1, 0)
end_point = (0, 1)
angle = calculate_arc_angle(center, start_point, end_point)
print('Arc Angle is : ', angle)

# Calculate Circle Center
p1 = (0, 0)
p2 = (1, 1)
p3 = (1, 0)
circle_center = calculate_circle_center(p1, p2, p3)
print('Circle Center is : ', circle_center)

# Fit and Plot Polynomial Curve
x_points = [0, 1, 2, 3]
y_points = [1, 3, 2, 5]
poly = create_and_fit_curve_with_points(x_points, y_points, 2)
plot_a_curve(x_points, y_points, degree= 2)

# Plot Tangent Circles Along Line
start_point = np.array([0, 0])
end_point = np.array([10, 0])
plot_tangent_circles_along_line(1, start_point, end_point, 5)

# Smallest Enclosing Circle
points = np.array([[0, 0], [1, 1], [1, 0]])
smallest_circle = find_smallest_circle(points)
print('Smallest Enclosing Circle is : ', smallest_circle)
```
## Line Module

The Line module includes functions for handling and plotting lines.


### Features

-    **Find Line Equation:** Calculate the line equation given two points.
-    **Plot Line on Figure:** Plot a line between two points on a matplotlib figure.
-    **Find Parallel Lines:** Calculate parallel lines at a given distance from an original line.
-    **Calculate Line Points:** Calculate points along a line segment.
-    **Shortest Distance to Line:** Find the shortest distance from a point to a line.
-    **Plot Bisectors:** Plot perpendicular bisectors of lines connecting given points.

### Usage

```python

from SimpleS.Points.Line import *

# Find Line Equation
A = (0, 0)
B = (1, 1)
line_eq = find_line_equation(A, B)

# Plot Line on Figure
plot_line_on_figure(A, B)

# Find Parallel Lines
distance = 1
parallel_lines = find_parallel_lines(A, B, distance)
plot_parallelـlines(A, B, distance)
# Calculate Line Points
line_points = simple_calculate_line_points(A, B)

# Shortest Distance to Line
point = (1, 0)
shortest_distance = calculate_shortest_dist_point_to_line(point, A, B)
print('Shortest Distance from Point -> (1, 0) to Line -> ( (0, 0), (1, 1) ) is :',shortest_distance)

# Plot Bisectors
points = [(0, 0), (1, 1), (2, 0)]
plot_bisectors(points)

```
## Triangle Module

The Triangle module provides functions for handling and plotting triangles.

### Features

-    **Calculate Triangle Area:** Compute the area of a triangle given its vertices.
-    **Check Point in Triangle:** Determine if a point is inside a triangle.
-    **Create and Plot Triangle:** Plot a triangle with given vertices.
-    **Check Point Position vs Triangle:**Check and plot the position of a point relative to a triangle.

### Usage

```python

from SimpleS.Points.Triangle import *

# Calculate Triangle Area
P1 = (1, -4)
P2 = (3, 5)
P3 = (2, 7)
area = calculate_triangle_area(P1, P2, P3)

# Create and Plot Triangle
create_triangle_with_points(P1, P2, P3)

# Check Point Position vs Triangle
test_point = (1.5,-1)
chech_points_pos_vs_triangle(P1, P2, P3, test_point)
```
## ImageRelated Scripts : enhancements.py

### Introduction
This Python script, titled "enhancements", is an enhanced version of the original image processing examples provided by OpenCV. It includes functionalities for applying erosion and dilatation transformations to images. This script can be used for educational purposes or integrated into larger image processing projects.

### Features
- **Erosion and Dilatation**: Apply morphological transformations to enhance or reduce features in images.
- **Flexible File Handling**: Load images from file paths or directly from images in memory.
- **Visualization**: Compare original and transformed images side by side.
- **Save Results**: Optionally save the resulting images with a timestamp and transformation details.

### Prerequisites
Before running the script, ensure you have Python installed on your system. This script is compatible with Python 3.6 or higher.

### Usage

To use this script, you need to create an instance of the ErosAndDilat class with either a path to an image file or an image object. Here's a quick example on how to use the class:

```python

from SimpleS.ImageRelated.enhancements import ErosAndDilat

# Initialize with an image path
image_processor = ErosAndDilat('path/to/your/image.jpg')

# Perform erosion and dilatation, display results, and save them
image_processor.main(eros=True, dilate=True, show=True, save=True)
```
### Parameters

- eros: Enable erosion (default: True)
- dilate: Enable dilatation (default: True)
- show: Display the images using matplotlib (default: True)
- save: Save the images to disk (default: False)
- save_path: Directory to save the images (default: 'results')
- file_name: Base file name for saved images (default: None)

### Acknowledgements

Special thanks to the OpenCV community for providing the base examples which were enhanced in this project. Also, check out the original script and documentation at OpenCV GitHub.

## ImageRelated Scripts : basics.py

This script, titled "basics", provides a collection of image processing utilities written in Python. These functions can be used for tasks such as edge detection, image inversion, and binary image creation. 


### ***Functions***

#### invert_image_color

  - Inverts the colors of an image. Can optionally save the result to a file.
  - Parameters:

    - image: Path to the image file or a numpy array.
    - save (optional): Whether to save the result.
    - save_path (optional): Directory to save the result.
    - file_name (optional): Name of the saved file.

- Example:

```python

from SimpleS.ImageRelated import basics

# Or :

from SimpleS.ImageRelated.basics import invert_image_color

#Or:

from SimpleS.ImageRelated.basics import * # Access to all

```

#### show_image

- Displays an image using matplotlib.
- Parameters:

    - image: Path to the image file or a numpy array.
    - title (optional): Title of the image window.
    - c_map (optional): Color map for displaying the image.
    - interpolation (optional): Interpolation method for - - - displaying the image.
    - save (optional): Whether to save the result.
    - save_path (optional): Directory to save the result.
    - file_name (optional): Name of the saved file.

- Example:

```python
from SimpleS.ImageRelated.basics import *

show_image('path_to_image.png', title="Example Image", save=True, save_path='./', file_name='example_image.png')
```

#### fill_shape

- Fills an area of a shape in an image based on the points defining the edges of the shape.
- Parameters:

    - image: The image where the shape is to be filled.
    - points: A list of (x, y) tuples defining the vertices of the shape.
    - color: A tuple defining the color to fill the shape.

- Example:

```python
from SimpleS.ImageRelated.basics import *

filled_image = fill_shape(image, points, color=(255, 0, 0))
```

#### force_image_to_GRAYSCALE

+ Converts a color image to grayscale.
+ Parameters:

    - image: The color image.

+ Example:

```python
from SimpleS.ImageRelated.basics import *

grayscale_image = force_image_to_GRAYSCALE(color_image)
```

#### read_image_in_grayscale

+ Reads an image in grayscale mode and optionally converts it to binary.
+ Parameters:

    + image_path: Path to the image file.
    + thrhold (optional): Threshold value for binarization.
    + type (optional): Thresholding type.
    + also_make_it_binary (optional): Whether to convert to binary.
    + binary_image_color (optional): Color for binary conversion.

+ Example:

```python
from SimpleS.ImageRelated.basics import *

binary_image = read_image_in_grayscale('path_to_image.png', thrhold=127, type='THRESH_BINARY', also_make_it_binary=True)
```
#### simple_binary_image_creator

+ Creates a binary image from a list of points.
+ Parameters:

    +points: List of tuples (x, y) representing the coordinates of points.
    + image_size (optional): Tuple (width, height) for the output image size.
    + size_of_edge_points (optional): Size of the points to enlarge.
    + iterations (optional): Number of iterations for dilation.
    + enlarge_points (optional): Whether to enlarge points.
    + smoothing (optional): Whether to apply Gaussian blur.

+ Example:

```python

from SimpleS.ImageRelated.basics import *

binary_image = simple_binary_image_creator(points, image_size=(100, 100))
```
#### advance_binary_image_creator

+ Creates an advanced binary image from a list of points.
+ Parameters:

    + points: List of tuples (x, y) representing the coordinates of points.
    + shape_size (optional): Size of the shape.

#### detect_edges

+ Detects edges in an image and optionally displays or saves the result.
+ Parameters:

    + image: Path to the image file or a numpy array.
    + n1 (optional): Lower threshold for the Canny edge detector.
    + n2 (optional): Upper threshold for the Canny edge detector.
    + show_edges (optional): Whether to display the detected edges.
    + show_contours (optional): Whether to display the detected contours.
    + title_for_detected_edges (optional): Title for the detected edges plot.
    + title_for_detected_contours (optional): Title for the detected contours plot.
    + return_edges (optional): Whether to return the detected edges.
    + return_contours (optional): Whether to return the detected contours.
    + range_color_start (optional): Start of the range for random colors.
    + range_color_end (optional): End of the range for random colors.
    + save (optional): Whether to save the result.
    + save_path (optional): Directory to save the result.
    + file_name (optional): Name of the saved file.


## License
This project is open-sourced under the `MIT License`. See the LICENSE file for more details.

## Mistakes and Corrections
To err is human, and nobody likes a perfect person! If you come across any mistakes or if you have questions, feel free to raise an issue or submit a pull request. Your contributions to improving the content are highly appreciated.

## Contact

Any Time: cloner174.org@gmail.com
