#in the name of God ##
#
import numpy as np
import matplotlib.pyplot as plt
from SimpleS.utils import save_path_generator


def calculate_perpendicular_bisector(p1, p2):
    # Calculate the midpoint
    midpoint = ((p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0)
    # Calculate the slope of the line segment
    if (p2[0] - p1[0]) != 0:
        slope_segment = (p2[1] - p1[1]) / (p2[0] - p1[0])
        # Check for vertical line slope
        if slope_segment == 0:
            bisector_slope = 'vertical'
            bisector_equation = f"x = {midpoint[0]}"
        else:
            # Slope of the perpendicular bisector
            bisector_slope = -1 / slope_segment
            # Equation of the perpendicular bisector
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


def distance_point_line(px, py, ax, ay, bx, by, tolerance=1e-10):
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
        dist = distance_point_line(px, py, ax, ay, bx, by, tolerance)
        distances.append(dist)
        if dist < closest_distance:
            closest_distance = dist
            closest_edge = (ax, ay, bx, by)
            closest_point = (ax + (dist * (bx - ax) / np.sqrt((bx - ax)**2 + (by - ay)**2)),
                             ay + (dist * (by - ay) / np.sqrt((bx - ax)**2 + (by - ay)**2)))
    if return_closest:
        
        return distances, closest_distance, closest_edge, closest_point
    
    return distances
#end#