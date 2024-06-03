import matplotlib.pyplot as plt

def calculate_triangle_area(P1, P2, P3):
    
    """
    Calculate the area of a triangle given its vertices using the shoelace formula.
    Args:
    P1, P2, P3 (tuple): Vertices of the triangle.
    Returns:
    float: Area of the triangle.
    """
    
    return 0.5 * abs(P1[0]*P2[1] + P2[0]*P3[1] + P3[0]*P1[1] - P1[1]*P2[0] - P2[1]*P3[0] - P3[1]*P1[0])


def is_point_in_triangle(P, P1, P2, P3):
    
    """
    Determine if a point P is inside the triangle formed by points P1, P2, and P3.
    Args:
    P (tuple): Coordinates of the point to check.
    P1, P2, P3 (tuple): Vertices of the triangle.
    Returns:
    bool: True if the point is inside the triangle, False otherwise.
    """
    # area of main triangle
    area_main = calculate_triangle_area(P1, P2, P3)
    # areas of the triangles formed with the point and each pair of vertices
    area1 = calculate_triangle_area(P, P1, P2)
    area2 = calculate_triangle_area(P, P2, P3)
    area3 = calculate_triangle_area(P, P3, P1)
    # the sum of the areas equals the area of the main triangle ?
    
    return abs(area_main - (area1 + area2 + area3)) < 1e-9 


def chech_points_pos_vs_triangle(P1, P2, P3, test_point, use_lim = True , x_lim=(-10, 10), y_lim=(-10, 10),
                                 triangle_label = 'Triangle', triangle_edgecolor = 'blue',
                                 points_label = 'Triangle Vertices',points_color = 'yellow',
                                 test_point_label = 'Test Point', test_point_color = 'black',
                                 inside_color = 'green', inside_label ='Inside',
                                 outside_color= 'red' , outside_label =  'Outside',
                                 plot_title = ' Test Point  VS  Triangle '):
    """
    optionally check if a test point lies within the triangle formed by these points.
    Args:
    P1 (tuple): Coordinates of the first point (i1, j1).
    P2 (tuple): Coordinates of the second point (i2, j2).
    P3 (tuple): Coordinates of the third point (i3, j3).
    test_point (tuple, optional): The point to test whether it lies within the triangle.
    xlim (tuple): Limits for the x-axis as (xmin, xmax).
    ylim (tuple): Limits for the y-axis as (ymin, ymax).
    Returns:
    bool: True if the test point is inside the triangle, False otherwise.
    """
    points = [P1, P2, P3]
    fig, ax = plt.subplots()
    x_coords, y_coords = zip(*points)
    if use_lim and x_lim is not None :
        ax.set_xlim(x_lim)
    if use_lim and y_lim is not None :
        ax.set_ylim(y_lim)
    ax.scatter(x_coords, y_coords, color=points_color, label=points_label)
    # triangle formed by the points
    triangle = plt.Polygon(points, fill=None, edgecolor=triangle_edgecolor, linestyle='--', label=triangle_label)
    ax.add_patch(triangle)
    result = None
    if test_point:
        ax.scatter(*test_point, color = test_point_color, label=test_point_label)
        result = is_point_in_triangle(test_point, P1, P2, P3)
        if result:
            plt.text(test_point[0], test_point[1], inside_label, fontsize=12, color=inside_color)
        else:
            plt.text(test_point[0], test_point[1],outside_label, fontsize=12, color=outside_color)
    ax.axhline(0, color='black',linewidth=0.5)
    ax.axvline(0, color='black',linewidth=0.5)
    ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(plot_title)
    ax.legend()
    plt.show()
    return result


def create_triangle_with_points(P1, P2, P3, xlim=(-10, 10), ylim=(-10, 10)):
    
    """
    Create and display a Euclidean plane with three given points P1, P2, and P3.
    Args:
    P1 (tuple): Coordinates of the first point (i1, j1).
    P2 (tuple): Coordinates of the second point (i2, j2).
    P3 (tuple): Coordinates of the third point (i3, j3).
    xlim (tuple): Limits for the x-axis as (xmin, xmax).
    ylim (tuple): Limits for the y-axis as (ymin, ymax).
    """
    points = [P1, P2, P3]
    fig, ax = plt.subplots()
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    x_coords, y_coords = zip(*points)
    ax.scatter(x_coords, y_coords, color='red', label='Points')
    triangle = plt.Polygon(points, fill=None, edgecolor='blue', linestyle='--', label='Triangle')
    ax.add_patch(triangle)
    ax.axhline(0, color='black',linewidth=0.5)
    ax.axvline(0, color='black',linewidth=0.5)
    ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Euclidean Plane with Points P1, P2, P3')
    ax.legend()
    plt.show()
    return triangle
#end