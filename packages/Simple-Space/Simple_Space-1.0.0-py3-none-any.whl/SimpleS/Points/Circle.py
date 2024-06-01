#In the name of God # #
#
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull



def plot_circles_along_arc(center, radius, start_angle, end_angle, circle_radius):
    """
    Plots circles along a circular arc.
    Parameters:
    - center: Tuple (x, y), the center of the arc
    - radius: Radius of the arc
    - start_angle, end_angle: Angles in degrees defining the arc
    - circle_radius: Radius of the circles to plot along the arc
    """
    fig, ax = plt.subplots()
    start_angle = np.deg2rad(start_angle)
    end_angle = np.deg2rad(end_angle)
    # Calculate limit of circles for fit along the arc
    arc_length = radius * (end_angle - start_angle)
    number_of_circles = int(arc_length / (2 * circle_radius))
    angle_increment = (end_angle - start_angle) / number_of_circles
    # Plot each circle along the arc
    for i in range(number_of_circles + 1):
        angle = start_angle + i * angle_increment
        circle_center = (center[0] + (radius - circle_radius) * np.cos(angle),
                         center[1] + (radius - circle_radius) * np.sin(angle))
        circle = plt.Circle(circle_center, circle_radius, color='r', fill=False, lw=2)
        ax.add_patch(circle)
    #arc = plt.Arc(center, 2 * radius, 2 * radius, angle=0, theta1=np.rad2deg(start_angle), theta2=np.rad2deg(end_angle), color='blue', linestyle='--')
    #ax.add_patch(arc)
    ax.set_xlim(center[0] - radius - 1, center[0] + radius + 1)
    ax.set_ylim(center[1] - radius - 1, center[1] + radius + 1)
    ax.set_aspect('equal')
    plt.grid(True)
    plt.show()


def calculate_arc_angle(center, start_point, end_point):
    """
    Calculate the angle of the arc on a circle between two points given the circle's center.
    Angles are calculated in radians and converted to degrees.
    Args:
    center (tuple): (x, y) coordinates of the circle's center.
    start_point (tuple): (x, y) coordinates of the starting point on the arc.
    end_point (tuple): (x, y) coordinates of the ending point on the arc.
    Returns:
    float: angle in degrees.
    """
    center = np.array(center)
    start_point = np.array(start_point)
    end_point = np.array(end_point)
    vector1 = start_point - center
    vector2 = end_point - center
    # Calculate angles using atan2
    angle1 = np.arctan2(vector1[1], vector1[0])
    angle2 = np.arctan2(vector2[1], vector2[0])
    # ensure a positive angle
    angle = angle2 - angle1
    if angle < 0:
        angle += 2 * np.pi
    return np.degrees(angle)


def calculate_circle_center(p1, p2, p3):
    """
    Calculate the center of the circle passing through three points.
    Args:
    p1, p2, p3 (tuple): (x, y) coordinates of three points on the circle.
    Returns:
    tuple: (x, y) coordinates of the circle's center.
    """
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    mid1 = (p1 + p2) / 2
    mid2 = (p2 + p3) / 2
    # slopes of lines p1p2 and p2p3
    slope1 = (p2[1] - p1[1]) / (p2[0] - p1[0]) if p2[0] != p1[0] else float('inf')
    slope2 = (p3[1] - p2[1]) / (p3[0] - p2[0]) if p3[0] != p2[0] else float('inf')
    # handle vertical lines
    if slope1 == float('inf'):
        center_x = mid1[0]
        center_y = mid2[1] + (mid2[0] - center_x) / slope2
    elif slope2 == float('inf'):
        center_x = mid2[0]
        center_y = mid1[1] + (mid1[0] - center_x) / slope1
    else:
        # Derive center
        slope1_perp = -1 / slope1
        slope2_perp = -1 / slope2
        center_x = (slope1_perp * mid1[0] - slope2_perp * mid2[0] + mid2[1] - mid1[1]) / (slope1_perp - slope2_perp)
        center_y = slope1_perp * (center_x - mid1[0]) + mid1[1]
    return (center_x, center_y)


def position_of_point_along_curve(t, points):
    """ Calculate the position of a point along a Bezier curve at parameter t.
        hint:
        If you need a point at a specific fraction along the curve, choose t based on that fraction.
        Example: t=0.5t=0.5 gives you the midpoint of the curve.
    """
    while len(points) > 1:
        points = [p1 + t * (p2 - p1) for p1, p2 in zip(points[:-1], points[1:])]
    return points[0]


def bezier_tangent(t, points):
    
    """ Calculate the tangent to the curve at parameter t. """
    derivative_points = [n * (p2 - p1) for n, (p1, p2) in enumerate(zip(points[:-1], points[1:]), 1)]
    return position_of_point_along_curve(t, derivative_points)


def angle_between_tangents(t1, t2, control_points):
    """ Calculate the angle between the tangents at two points along a Bezier curve."""
    tan1 = bezier_tangent(t1, control_points)
    tan2 = bezier_tangent(t2, control_points)
    angle = np.arccos(np.dot(tan1, tan2) / (np.linalg.norm(tan1) * np.linalg.norm(tan2)))
    return np.degrees(angle)


def plot_tangent_circles_along_line(radius, start_point, end_point, num_circles):
    """
    Plots a series of tangent circles between two points with specified radius.
    Assumes a straight line path between start and end points.
    """
    fig, ax = plt.subplots()
    # Calculate the distance between the start and end points
    distance = np.linalg.norm(end_point - start_point)
    direction = (end_point - start_point) / distance
    
    # Calculate positions of circle centers
    centers = [start_point + direction * radius * (1 + 2 * i) for i in range(num_circles)]
    
    # Plotting each circle
    for center in centers:
        circle = plt.Circle(center, radius, color='r', fill=False, lw=2)
        ax.add_patch(circle)
    # Drawing the line for reference
    line = np.vstack([start_point, end_point])
    plt.plot(line[:,0], line[:,1], 'b--')
    # Set limits and aspect
    ax.set_xlim(min(start_point[0], end_point[0]) - radius, max(start_point[0], end_point[0]) + radius)
    ax.set_ylim(min(start_point[1], end_point[1]) - radius, max(start_point[1], end_point[1]) + radius)
    ax.set_aspect('equal')
    plt.grid(True)
    plt.show()


def plot_tangent_circles_between_lines(start_x, end_x, lower_y, upper_y):
    """
    Plots circles tangent to two horizontal lines from start_x to end_x.
    The circles' diameters are determined by the distance between lower_y and upper_y.
    """
    radius = (upper_y - lower_y) / 2
    center_y = (upper_y + lower_y) / 2
    number_of_circles = int((end_x - start_x) / (2 * radius))
    fig, ax = plt.subplots()
    
    ax.hlines(y=[lower_y, upper_y], xmin=start_x, xmax=end_x, color='blue', linestyle='--')
    
    for i in range(number_of_circles):
        center_x = start_x + radius + i * 2 * radius
        circle = plt.Circle((center_x, center_y), radius, color='r', fill=False, lw=2)
        ax.add_patch(circle)
    ax.set_xlim(start_x - 1, end_x + 1)
    ax.set_ylim(lower_y - 1, upper_y + 1)
    ax.set_aspect('equal')
    plt.grid(True)
    plt.show()


def midpoint(p1, p2):
    return (p1 + p2) / 2


def perpendicular_bisector(p1, p2):
    # Returns the slope and intercept of the perpendicular bisector
    if p2[0] - p1[0] == 0:  # vertical line
        return None, p1[0]
    elif p2[1] - p1[1] == 0:  # horizontal line
        return 0, p1[1]
    else:
        midpoint = (p1 + p2) / 2
        slope = -(p2[0] - p1[0]) / (p2[1] - p1[1])
        intercept = midpoint[1] - slope * midpoint[0]
        return slope, intercept


def find_smallest_circle(points):
    # Helper function to calculate the circle from three points
    def calculate_circle(p1, p2, p3):
        # Calculate the circumscribed circle of the triangle formed by points p1, p2, p3
        # Using determinant method
        A = np.linalg.det([[p1[0], p1[1], 1],
                           [p2[0], p2[1], 1],
                           [p3[0], p3[1], 1]])
        B = np.linalg.det([[p1[0]**2 + p1[1]**2, p1[1], 1],
                           [p2[0]**2 + p2[1]**2, p2[1], 1],
                           [p3[0]**2 + p3[1]**2, p3[1], 1]])
        C = np.linalg.det([[p1[0]**2 + p1[1]**2, p1[0], 1],
                           [p2[0]**2 + p2[1]**2, p2[0], 1],
                           [p3[0]**2 + p3[1]**2, p3[0], 1]])
        D = np.linalg.det([[p1[0]**2 + p1[1]**2, p1[0], p1[1]],
                           [p2[0]**2 + p2[1]**2, p2[0], p2[1]],
                           [p3[0]**2 + p3[1]**2, p3[0], p3[1]]])
        x = 0.5 * B / A
        y = -0.5 * C / A
        radius = np.sqrt((B**2 + C**2 - 4 * A * D) / (4 * A**2))
        return (x, y), radius
    # Start with an arbitrary point, and find the smallest circle with 2 or 3 points
    if len(points) == 1:
        return points[0], 0
    elif len(points) == 2:
        mid_point = (points[0] + points[1]) / 2
        radius = np.linalg.norm(points[0] - mid_point)
        return mid_point, radius
    # More than two points: we check every combination of three points
    smallest_radius = float('inf')
    smallest_circle = None
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            for k in range(j + 1, len(points)):
                center, radius = calculate_circle(points[i], points[j], points[k])
                if radius < smallest_radius:
                    valid = all(np.linalg.norm(center - p) <= radius + 1e-12 for p in points)
                    if valid:
                        smallest_radius = radius
                        smallest_circle = (center, radius)
    # In case no valid circle was found with three points, fallback to any two points
    if smallest_circle is None:
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                mid_point = (points[i] + points[j]) / 2
                radius = np.linalg.norm(points[i] - mid_point)
                if radius < smallest_radius:
                    smallest_radius = radius
                    smallest_circle = (mid_point, radius)
    return smallest_circle


def plot_polygon_with_circle(points, 
                             circle, fill_circle = None, lw_circle = 1, circle_color = 'r',
                             edgecolor='black', fill_edge=None,  lw_edge=1):
    
    polygon = plt.Polygon(points, edgecolor=edgecolor, fill=fill_edge, lw=lw_edge)
    fig, ax = plt.subplots()
    ax.add_patch(polygon)
    if circle:
        center, radius = circle
        circle_patch = plt.Circle(center, radius, color=circle_color, fill=fill_circle, lw=lw_circle)
        ax.add_patch(circle_patch)
    ax.set_xlim(np.min(points[:,0]) - 1, np.max(points[:,0]) + 1)
    ax.set_ylim(np.min(points[:,1]) - 1, np.max(points[:,1]) + 1)
    ax.set_aspect('equal', adjustable='datalim')
    plt.grid(True)
    plt.show()
#end#