#in the name of God ##
#
import time
import numpy as np
import matplotlib.pyplot as plt
from SimpleS.utils import save_path_generator


def find_line_equation(A, B, return_function_object = False):
    """Calculate the line equation y = mx + c given two points A(x1, y1) and B(x2, y2)
    """
    x1, y1 = A
    x2, y2 = B
    # Calculate slope (m)
    # Prevent division by zero in case of vertical lines
    if x2 - x1 == 0:
        print("The line is vertical.")
        return None
    m = (y2 - y1) / (x2 - x1)
    # Calculate intercept(c)
    c = y1 - m * x1
    if c < 0:
        print(f"The equation of the line is: y = {m}x - {abs(c)}")
    else:
        print(f"The equation of the line is: y = {m}x + {c}")
    if return_function_object:
        def y(x):
            return (m * x) + c
        return y


def plot_line_on_figure(A, B, ax = None, additional_points = None,  additional_points_color = 'green',
                        line_color = 'r', points_colors = 'blue',  title_of_plot = 'Line between points A and B', 
                        x_lim = None, y_lim = None, x_label = 'X', y_label = 'Y',
                        Apoint_tag = 'A', Bpoint_tag = 'B', point_tag_size = 12, Apoint_tag_where= 'right', Bpoint_tag_where = 'left'):
    """
    Plot a line given by two points A and B on a provided matplotlib axis.
    options for point_tag_where are -> 'center', 'right', 'left'
    """
    x1, y1 = A
    x2, y2 = B
    # Generate x values from slightly before the smallest x to slightly after the largest x
    x_values = np.linspace(min(x1, x2) - 1, max(x1, x2) + 1, 400)
    # Handle the case of vertical line
    if ax is None:
        fig, ax = plt.subplots()
    if x2 - x1 == 0:
        # vertical line
        ax.axvline(x=x1, color=line_color, label=f'x = {x1}')
    else:
        m = (y2 - y1) / (x2 - x1)
        c = y1 - m * x1
        y_values = m * x_values + c
        ax.plot(x_values, y_values, color=line_color, label=f'y = {m:.2f}x + {c:.2f}')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title_of_plot)
    ax.legend()
    ax.scatter([x1, x2], [y1, y2], color=points_colors)
    if additional_points is not None:
        try:
            ax.scatter(additional_points[:,0], additional_points[:,1], color=additional_points_color)
        except Exception as e:
            try:
                additional_points = np.asarray(additional_points)
                ax.scatter(additional_points[:,0], additional_points[:,1], color=additional_points_color)
            except:
                print("fail to draw additional_points : reason : ", e)
                time.sleep(2)
    ax.text(x1, y1, Apoint_tag, fontsize=point_tag_size, ha=Apoint_tag_where)
    ax.text(x2, y2, Bpoint_tag, fontsize=point_tag_size, ha=Bpoint_tag_where)
    if x_lim is not None:
        ax.set_xlim(x_lim)
    if y_lim is not None:
        ax.set_ylim(y_lim)
    plt.show()


def find_parallel_lines(A, B, distance, return_function_object = False,give_me_both=False):
    """
    Find equations of two parallel lines at a given distance from the line through points A and B.
    This gave you One of the two computed Functions. If you need both, use:  give_me_both = True
    You can use the returend object like :
    >>> my_obj = find_parallel_lines(A,B,distance,True)
    >>> print(my_obj(0))
    """
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
    # the y-intercept (c) of the line AB
    c = y1 - m * x1
    # |Ax + By + C| / sqrt(A^2 + B^2)
    # For line mx - y + c = 0, A = m, B = -1, C = c
    # Distance d from line to parallel lines, solve for new c in |mx - y + new_c| / sqrt(m^2 + 1) = d
    # Simplify to find new_c = c ± d * sqrt(m^2 + 1)
    delta_c = distance * np.sqrt(m**2 + 1)
    c1 = c + delta_c
    c2 = c - delta_c
    if return_function_object:
        print("""Use give_me_both = True for returning two computed Functions""")
        def y(x):
            return (m * x) + c1
        if not give_me_both:
            return y
        else:
            def yprime(x):
                return (m * x) + c2
            return y, yprime
    else:
        print("Equations of parallel lines: y = {:.2f}x + {:.2f} and y = {:.2f}x + {:.2f}".format(m, c1, m, c2))
        return [(m, c1), (m, c2)]


def simple_calculate_line_points(A, B):
    """Calculate all 'integer' coordinate points on the line segment between A and B using Bresenham's Line Algorithm."""
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


def advance_calculate_line_points(A, B, scale = 1e6):
    """
    Calculate all 'float' coordinate points on the line segment between A and B 
    Using a ' modified Bresenham's Line Algorithm 'that handles very short values.
    You can Use this line for avoiding scientific numbers yourself. replace 10 with any other number you like.
                    >>> points = calculate_line_points(A, B)
                    >>> formatted_points = [(f"{x:.10f}", f"{y:.10f}") for x, y in points]
    """
    x1, y1 = A
    x2, y2 = B
    points = []
    # Scale up to handle very short values
    x1, y1, x2, y2 = int(x1 * scale), int(y1 * scale), int(x2 * scale), int(y2 * scale)
    dx = abs(x2 - x1)
    dy = -abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx + dy  # error value e_xy
    while True:
        points.append((x1 / scale, y1 / scale))  # Add the current point to the list
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


def calculate_shortest_dist_point_to_line(point, A, B):
    """Calculate the shortest distance from a point to a line defined by points A and B."""
    x3, y3 = point
    x1, y1 = A
    x2, y2 = B
    if A == B:
        raise ValueError("Point A and B cannot be the same for a line definition.")
    # Ax + By + C = 0 # y = mx + c
    # m = (y2 - y1) / (x2 - x1) # c = y1 - m * x1
    # (y2 - y1)x - (x2 - x1)y + (x2*y1 - x1*y2) = 0
    A = y2 - y1
    B = x1 - x2
    C = x2 * y1 - x1 * y2
    # Distance formula from point (x3, y3) to line Ax + By + C = 0 # |Ax3 + By3 + C| / sqrt(A^2 + B^2)
    distance = np.abs(A * x3 + B * y3 + C) / np.sqrt(A**2 + B**2)
    return distance


def calculate_perpendicular_bisector(p1, p2):
    # the midpoint
    midpoint = ((p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0)
    # the slope of the line segment
    if (p2[0] - p1[0]) != 0:
        slope_segment = (p2[1] - p1[1]) / (p2[0] - p1[0])
        if slope_segment == 0:
            bisector_slope = 'vertical'
            bisector_equation = f"x = {midpoint[0]}"
        else:
            bisector_slope = -1 / slope_segment
            b = midpoint[1] - bisector_slope * midpoint[0]
            bisector_equation = f"y = {bisector_slope}x + {b}"
    else:
        bisector_slope = 'horizontal'
        bisector_equation = f"y = {midpoint[1]}"
    return midpoint, bisector_slope, bisector_equation


def plot_bisectors(points, 
                   x_label = 'X Axis' , y_label= 'Y Axis', 
                   title = 'Perpendicular Bisectors', 
                   have_grid = True,
                   save = False, save_path = None, file_name = None):
    plt.figure()
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            p1, p2 = points[i], points[j]
            midpoint, slope, equation = calculate_perpendicular_bisector(p1, p2)
            print(f"Between points {p1} and {p2}:")
            print(f"  Midpoint: {midpoint}")
            print(f"  Slope of Perpendicular Bisector: {slope}")
            print(f"  Equation: {equation}")
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'bo-')  # Line segment
            if isinstance(slope, str) and slope == 'vertical':
                plt.axvline(x=midpoint[0], color='r', linestyle='--')
            elif isinstance(slope, str) and slope == 'horizontal':
                plt.axhline(y=midpoint[1], color='r', linestyle='--')
            else:
                x_values = np.linspace(min(p1[0], p2[0])-1, max(p1[0], p2[0])+1, 400)
                y_values = slope * x_values + (midpoint[1] - slope * midpoint[0])
                plt.plot(x_values, y_values, 'r--')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(have_grid)
    if save:
        path_to_save = save_path_generator(file_name, save_path, flag=None)
        plt.savefig(path_to_save)
    plt.show()


def distance_point_to_line(px, py, ax, ay, bx, by, tolerance=1e-10):
    """Calculate the precise distance from point P(px, py) to the line segment AB(ax, ay to bx, by)."""
    AB = [bx - ax, by - ay]
    AP = [px - ax, py - ay]
    AB_mag = np.sqrt(AB[0]**2 + AB[1]**2)
    AB_dot_AP = AB[0] * AP[0] + AB[1] * AP[1]
    distance = AB_dot_AP / AB_mag
    if AB_mag < tolerance:
        return np.sqrt((px - ax)**2 + (py - ay)**2)
    if distance < 0:
        return np.sqrt((px - ax)**2 + (py - ay)**2)
    elif distance > AB_mag:
        return np.sqrt((px - bx)**2 + (py - by)**2)
    else:
        x = ax + (distance * AB[0] / AB_mag)
        y = ay + (distance * AB[1] / AB_mag)
        return np.sqrt((px - x)**2 + (py - y)**2)


def distance_from_point_to_polygon_sides(px, py, polygon, return_closest=False, tolerance=1e-10):
    distances = []
    closest_distance = float('inf')
    closest_edge = None
    closest_point = None
    for i in range(len(polygon)):
        ax, ay = polygon[i]
        bx, by = polygon[(i + 1) % len(polygon)]
        dist = distance_point_to_line(px, py, ax, ay, bx, by, tolerance)
        distances.append(dist)
        if dist < closest_distance:
            closest_distance = dist
            closest_edge = (ax, ay, bx, by)
            closest_point = (ax + (dist * (bx - ax) / np.sqrt((bx - ax)**2 + (by - ay)**2)),
                             ay + (dist * (by - ay) / np.sqrt((bx - ax)**2 + (by - ay)**2)))
    if return_closest:
        return distances, closest_distance, closest_edge, closest_point
    return distances


def draw_line_on_fig_using_slope(ax, slope, intercept, label, color='r'):
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


def plot_any(*args, color_for_points = None, color_for_lines = None, random_color = True,
              title = 'Plot of Points and Lines', x_label = 'X-axis', y_label = 'Y-axis', has_grid = True):
    points = []
    lines = []
    for arg in args:
        if isinstance(arg, tuple) and len(arg) == 2:
            points.append(arg)
        elif isinstance(arg, tuple) and len(arg) == 4:
            lines.append(((arg[0], arg[1]), (arg[2], arg[3])))
        elif isinstance(arg, list):
            for item in arg:
                if isinstance(item, tuple) and len(item) == 2:
                    points.append(item)
                elif isinstance(item, tuple) and len(item) == 4:
                    lines.append(((item[0], item[1]), (item[2], item[3])))
    plt.figure()
    # Plot points
    color_fix_lines = None
    color_fix_points = None
    color = ['blue', 'red', 'yellow', 'pink', 'brown', 'purple', 'black']
    if color_for_lines is None and not random_color:
            color_fix_lines = 'blue'
    else:
        if isinstance(color_for_lines, list) and len(color_for_lines) == len(lines):
            color_fix_lines = color_for_lines
        else:
            if not random_color:
                color_fix_lines = 'red'
    if color_for_points is None and not random_color:
            color_fix_points = 'red'
    else:
        if isinstance(color_for_points, list) and len(color_for_points) == len(points):
            color_fix_points = color_for_points
        else:
            if not random_color:
                color_fix_points = 'blue'
    for point in points:
        if color_fix_points is not None:
            plt.scatter(*point, color=color_fix_points)
        else:
            plt.scatter(*point, color=np.random.choice(color))
    # Plot lines
    for line in lines:
        (x1, y1), (x2, y2) = line
        if color_fix_lines is not None:
            plt.scatter(*point, color=color_fix_lines)
        else:
            plt.plot([x1, x2], [y1, y2], color=np.random.choice(color))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(has_grid)
    plt.show()


def plot_parallelـlines(A, B, distance, ax=None):
    """Plot a line through points A and B and two parallel lines at a given distance."""
    if ax is None:
        fig, ax = plt.subplots()  # Create a new figure and axis if not provide
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
    plt.show()
#end#