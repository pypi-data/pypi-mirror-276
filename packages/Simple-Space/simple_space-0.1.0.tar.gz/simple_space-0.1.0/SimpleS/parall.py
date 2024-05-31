def find_line_equation(A, B):
    """Calculate the line equation y = mx + c given two points A(x1, y1) and B(x2, y2)"""
    x1, y1 = A
    x2, y2 = B
    
    # Calculate the slope (m)
    # Prevent division by zero in case of vertical lines
    if x2 - x1 == 0:
        print("The line is vertical.")
        return None
    
    m = (y2 - y1) / (x2 - x1)
    
    # Calculate the y-intercept (c)
    c = y1 - m * x1
    
    # Print the equation of the line
    if c < 0:
        print(f"The equation of the line is: y = {m}x - {abs(c)}")
    else:
        print(f"The equation of the line is: y = {m}x + {c}")

# Example usage
A = (1, 2)
B = (3, 6)
find_line_equation(A, B)



import matplotlib.pyplot as plt
import numpy as np

def plot_line_on_figure(ax, A, B):
    """Plot a line given by two points A and B on a provided matplotlib axis."""
    x1, y1 = A
    x2, y2 = B
    
    # Generate x values from slightly before the smallest x to slightly after the largest x
    x_values = np.linspace(min(x1, x2) - 1, max(x1, x2) + 1, 400)
    
    # Handle the case of a vertical line
    if x2 - x1 == 0:
        # Plot a vertical line
        ax.axvline(x=x1, color='r', label=f'x = {x1}')
    else:
        # Calculate the slope and y-intercept
        m = (y2 - y1) / (x2 - x1)
        c = y1 - m * x1
        
        # Generate y values based on the slope and y-intercept
        y_values = m * x_values + c
        
        # Plot the line
        ax.plot(x_values, y_values, 'r', label=f'y = {m:.2f}x + {c:.2f}')
    
    # Setting plot labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Line between points A and B')
    ax.legend()

    # Scatter plot the points A and B
    ax.scatter([x1, x2], [y1, y2], color='blue')
    ax.text(x1, y1, 'A', fontsize=12, ha='right')
    ax.text(x2, y2, 'B', fontsize=12, ha='left')

# Example usage:
fig, ax = plt.subplots()
A = (1, 2)
B = (3, 6)
plot_line_on_figure(ax, A, B)
plt.show()

def calculate_line_points(A, B):
    """Calculate all integer coordinate points on the line segment between A and B using Bresenham's Line Algorithm."""
    x1, y1 = A
    x2, y2 = B

    points = []
    dx = abs(x2 - x1)
    dy = -abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx + dy  # error value e_xy

    while True:
        points.append((x1, y1))  # Add the current point to the list
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 >= dy:  # e_xy+e_x > 0
            err += dy
            x1 += sx
        if e2 <= dx:  # e_xy+e_y < 0
            err += dx
            y1 += sy

    return points

# Example usage
A = (1, 2)
B = (11, 6)
line_points = calculate_line_points(A, B)
print("Points on the line:", line_points)


import numpy as np

def find_parallel_lines(A, B, distance):
    """Find equations of two parallel lines at a given distance from the line through points A and B."""
    x1, y1 = A
    x2, y2 = B

    # Calculate the slope (m) of the line AB
    if x2 - x1 == 0:
        print("The line is vertical, parallel lines will be horizontal.")
        # Return horizontal lines at the distance
        return [(None, y1 + distance), (None, y1 - distance)]
    
    if y2 - y1 == 0:
        print("The line is horizontal, parallel lines will be vertical.")
        # Return vertical lines at the distance
        return [(x1 + distance, None), (x1 - distance, None)]

    m = (y2 - y1) / (x2 - x1)
    # Calculate the y-intercept (c) of the line AB
    c = y1 - m * x1
    
    # Using the distance formula for a point to a line |Ax + By + C| / sqrt(A^2 + B^2)
    # For line mx - y + c = 0, A = m, B = -1, C = c
    # Distance d from line to parallel lines, solve for new c in |mx - y + new_c| / sqrt(m^2 + 1) = d
    # Simplify to find new_c = c ± d * sqrt(m^2 + 1)
    delta_c = distance * np.sqrt(m**2 + 1)
    new_c1 = c + delta_c
    new_c2 = c - delta_c

    return [(m, new_c1), (m, new_c2)]

# Example usage
A = (1, 2)
B = (3, 6)
distance = 2
parallel_lines = find_parallel_lines(A, B, distance)
print("Equations of parallel lines: y = {:.2f}x + {:.2f} and y = {:.2f}x + {:.2f}".format(
    parallel_lines[0][0], parallel_lines[0][1], parallel_lines[1][0], parallel_lines[1][1]))

import matplotlib.pyplot as plt
import numpy as np

def plot_line_on_figure(ax, slope, intercept, label, color='r'):
    """Plot a line based on slope and intercept on a provided matplotlib axis."""
    x_values = np.linspace(-10, 10, 400)
    if slope is None:  # Vertical line
        ax.axvline(x=intercept, color=color, label=label)
    elif intercept is None:  # Horizontal line
        ax.axhline(y=slope, color=color, label=label)
    else:
        y_values = slope * x_values + intercept
        ax.plot(x_values, y_values, color, label=label)
    
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()

def find_parallel_lines(A, B, distance):
    """Find equations of two parallel lines at a given distance from the line through points A and B."""
    x1, y1 = A
    x2, y2 = B
    if x2 - x1 == 0:
        return [(None, x1 + distance), (None, x1 - distance)]
    elif y2 - y1 == 0:
        return [(y1 + distance, None), (y1 - distance, None)]
    
    m = (y2 - y1) / (x2 - x1)
    c = y1 - m * x1
    delta_c = distance * np.sqrt(m**2 + 1)
    return [(m, c + delta_c), (m, c - delta_c)]

# Example usage
A = (1, 2)
B = (3, 6)
distance = 2

# Calculate parallel lines
parallel_lines = find_parallel_lines(A, B, distance)

# Create a plot
fig, ax = plt.subplots()

# Plot the original line
m_orig = (B[1] - A[1]) / (B[0] - A[0]) if (B[0] - A[0]) != 0 else None
c_orig = A[1] - m_orig * A[0] if m_orig is not None else None
plot_line_on_figure(ax, m_orig, c_orig, 'Original Line')

# Plot parallel lines
for i, line in enumerate(parallel_lines):
    plot_line_on_figure(ax, line[0], line[1], f'Parallel Line {i+1}')

plt.show()


import matplotlib.pyplot as plt
import numpy as np

def comprehensive_line_plot(A, B, distance, ax=None):
    """Plot a line through points A and B and two parallel lines at a given distance."""
    if ax is None:
        fig, ax = plt.subplots()  # Create a new figure and axis if not provided

    # Define the original line equation
    x1, y1 = A
    x2, y2 = B
    if x1 == x2:  # Vertical line
        ax.axvline(x=x1, color='blue', label='Original Line: x = {}'.format(x1))
        ax.axvline(x=x1 + distance, color='green', label='Parallel Line 1: x = {}'.format(x1 + distance))
        ax.axvline(x=x1 - distance, color='red', label='Parallel Line 2: x = {}'.format(x1 - distance))
    elif y1 == y2:  # Horizontal line
        ax.axhline(y=y1, color='blue', label='Original Line: y = {}'.format(y1))
        ax.axhline(y=y1 + distance, color='green', label='Parallel Line 1: y = {}'.format(y1 + distance))
        ax.axhline(y=y1 - distance, color='red', label='Parallel Line 2: y = {}'.format(y1 - distance))
    else:
        m = (y2 - y1) / (x2 - x1)
        c = y1 - m * x1
        delta_c = distance * np.sqrt(m**2 + 1)

        x_values = np.linspace(min(x1, x2) - 10, max(x1, x2) + 10, 400)
        y_values = m * x_values + c
        ax.plot(x_values, y_values, 'blue', label='Original Line: y = {:.2f}x + {:.2f}'.format(m, c))

        # Plot parallel lines
        y_values_1 = m * x_values + (c + delta_c)
        y_values_2 = m * x_values + (c - delta_c)
        ax.plot(x_values, y_values_1, 'green', label='Parallel Line 1: y = {:.2f}x + {:.2f}'.format(m, c + delta_c))
        ax.plot(x_values, y_values_2, 'red', label='Parallel Line 2: y = {:.2f}x + {:.2f}'.format(m, c - delta_c))

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()
    ax.grid(True)
    ax.set_title('Line through ({}, {}) and ({}, {}) with parallels at distance {}'.format(x1, y1, x2, y2, distance))

    if ax is None:
        plt.show()  # Show the plot if we created the figure internally

# Example usage
A = (1, 2)
B = (3, 6)
distance = 1
comprehensive_line_plot(A, B, distance)


import numpy as np

def calculate_distance_point_to_line(point, A, B):
    """Calculate the shortest distance from a point to a line defined by points A and B."""
    x3, y3 = point
    x1, y1 = A
    x2, y2 = B

    # Ensure the line is not just a point
    if A == B:
        raise ValueError("Point A and B cannot be the same for a line definition.")

    # Line coefficients A, B, and C in the form Ax + By + C = 0
    # Derived from the general line equation y = mx + c
    # Where m = (y2 - y1) / (x2 - x1) and c = y1 - m * x1
    # Line equation becomes (y2 - y1)x - (x2 - x1)y + (x2*y1 - x1*y2) = 0
    A = y2 - y1
    B = x1 - x2
    C = x2 * y1 - x1 * y2

    # Distance formula from point (x3, y3) to line Ax + By + C = 0
    # |Ax3 + By3 + C| / sqrt(A^2 + B^2)
    distance = np.abs(A * x3 + B * y3 + C) / np.sqrt(A**2 + B**2)

    return distance

# Example usage
point = (4, 4)
A = (1, 2)
B = (3, 6)
distance = calculate_distance_point_to_line(point, A, B)
print(f"The perpendicular distance from the point {point} to the line through {A} and {B} is: {distance:.2f}")


def calculate_midpoint(A, B):
    """Calculate the midpoint of a line segment between two points A and B."""
    x1, y1 = A
    x2, y2 = B
    # Midpoint formulas
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    # Return the midpoint as a tuple
    return (mid_x, mid_y)

# Example usage
A = (1, 2)
B = (3, 6)
midpoint = calculate_midpoint(A, B)
print(f"The midpoint between {A} and {B} is: {midpoint}")
