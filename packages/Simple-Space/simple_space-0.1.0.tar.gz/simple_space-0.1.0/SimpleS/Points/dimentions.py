import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.ndimage import binary_dilation
from SimpleS.utils import save_path_generator
import cv2
import scipy.ndimage as ndi
from skimage import img_as_ubyte
from skimage.morphology import skeletonize


class Dim3:
    
    def __init__(self):
        pass
    
    
    @staticmethod
    def read_off_file(file_path):
        """ It will return 2Object  Vertices  and  Faces. """
        with open(file_path, 'r') as file:
                if file.readline().strip() != "OFF":
                        raise ValueError("Not a valid OFF file")
                n_vertices, n_faces, _ = map(int, file.readline().strip().split())
                vertices = [tuple(map(float, file.readline().strip().split())) for _ in range(n_vertices)]
                faces = [tuple(map(int, file.readline().strip().split()[1:])) for _ in range(n_faces)]
                vertices = np.asarray(vertices)
                print("Secssesful . Vertices")
                faces = np.asarray(faces)
                print("Secssesful . Faces")
        
        return vertices, faces
    
    
    @staticmethod
    def rotate_points(points, theta, axis='z'):
        """Rotate 3D points around the specified axis by theta degrees."""
        theta = np.radians(theta)
        if axis == 'x':
                rot_matrix = np.array([
                        [1, 0, 0],
                        [0, np.cos(theta), -np.sin(theta)],
                        [0, np.sin(theta), np.cos(theta)]
                ])
        elif axis == 'y':
                rot_matrix = np.array([
                        [np.cos(theta), 0, np.sin(theta)],
                        [0, 1, 0],
                        [-np.sin(theta), 0, np.cos(theta)]
                ])
        else:  # Default
                rot_matrix = np.array([
                        [np.cos(theta), -np.sin(theta), 0],
                        [np.sin(theta), np.cos(theta), 0],
                        [0, 0, 1]
                ])
        
        return np.dot(points, rot_matrix.T)
    
    
    @staticmethod
    def plot_points(v, f=None, axis = 'on', title = '3D Data Visualization', faces_colors = 'blue', alpha=0.75, linewidths=1, edgecolors='r', point_color='blue',show =True, save=False, save_path = None, file_name = None ):
        """
        Plot 3D points or a mesh from vertices and optionally faces.
        
        Parameters:
        - v: List of vertices where each vertex is a list or tuple [x, y, z].
        - f: Optional. List of faces, where each face is a list of indices of vertices forming that face.
        - axis: if 'on' shows the title for each axis -> 'X-axis' and 'Y-axis' and 'Z-axis'.
        - title: if set to  None  or an empty string  ''  it will remove the title in result.
        - faces_colors: Can be whether a single color or a list of colors. It's the color for face's points.
        - alpha: Transparency of the faces when plotting a mesh.
        - linewidths: Width of the edges when plotting a mesh.
        - edgecolors: Color of the edges when plotting a mesh.
        - point_color: Color of the points when plotting only points.
        Example usage:
        vertices = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0.5, 0.5, 1]]
        faces = [[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4], [0, 1, 2, 3]]
        plot_3d_data(vertices, faces)  # Plotting a mesh
        plot_3d_data(vertices)  # Plotting points
        """
        vertices = np.array(v)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        if f is not None:
                faces = np.array(f, dtype=int)
                for face in faces:
                        verts = vertices[face]
                        poly = Poly3DCollection([verts], alpha=alpha, linewidths=linewidths, edgecolors=edgecolors)
                        poly.set_facecolor(faces_colors)
                        ax.add_collection3d(poly)
        else:
                ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], color=point_color, alpha=alpha)
        
        ax.set_xlim([vertices[:, 0].min(), vertices[:, 0].max()])
        ax.set_ylim([vertices[:, 1].min(), vertices[:, 1].max()])
        ax.set_zlim([vertices[:, 2].min(), vertices[:, 2].max()])
        if axis == 'on':
                ax.set_xlabel('X-axis')
                ax.set_ylabel('Y-axis')
                ax.set_zlabel('Z-axis')
        if title is not None and title != '':
                if save == True and file_name is None:
                        if title != '3D Data Visualization':
                                file_name = title
                plt.title(title)
        if save:
                path_to_save_file = save_path_generator(file_name,save_path, flag=None)
                plt.savefig(path_to_save_file)
        if show:
                plt.show()
        else:
                plt.clf()
                plt.close()
                return
    
    
    @staticmethod
    def create_bool_image_from_points(points, image_size=(500, 500),save = False, save_path = None, file_name = None):
        """
        Create a grayscale image from 3D points by projecting them onto a 2D plane using the z-coordinate
        as intensity.
        Args:
        points (numpy.ndarray): An array of points with shape (N, 3), where each row represents a 3D point (x, y, z).
        image_size (tuple): The dimensions of the output image (width, height).
        
        Returns:
        numpy.ndarray: A grayscale image where pixels' intensity is based on the z-value of points.
        """
        # use z for intensity
        projected_points = points[:, :2]
        z_values = points[:, 2]
        
        min_vals = np.min(projected_points, axis=0)
        max_vals = np.max(projected_points, axis=0)
        scaled_points = (projected_points - min_vals) / (max_vals - min_vals) * (np.array(image_size) - 1)
        
        z_min = np.min(z_values)
        z_max = np.max(z_values)
        z_scaled = (z_values - z_min) / (z_max - z_min) * 255 if z_max > z_min else np.zeros_like(z_values)
        
        image = np.zeros(image_size, dtype=np.uint8)
        
        for (point, intensity) in zip(scaled_points.astype(int), z_scaled.astype(np.uint8)):
                current_intensity = image[point[1], point[0]]
                image[point[1], point[0]] = max(current_intensity, intensity)  # Use the maximum intensity if overlapping
        if save:
                path_to_save = save_path_generator(file_name,save_path, flag=None)
                plt.imsave(path_to_save, image )
        return image
    
    
    @staticmethod
    def fill_points(image, iterations=5, structure=None, structure_like = (3,3) , save = False, save_path = None, file_name = None):
        """Fill in the gaps in a binary image using morphological dilation."""
        if structure is None:
                structure = np.ones(structure_like)
        try:
                filled_image = binary_dilation(image, structure=structure, iterations=iterations)
        except Exception as e:
                try:
                        filled_image = binary_dilation(image, structure=(3,3,3), iterations=iterations)
                except:
                        raise ValueError(f"{e}")
        if save:
                save_path_generator(file_name, save_path, flag=None)
        return filled_image
    
    
    @staticmethod
    def plot_3d_points(points, title = '3D Points Plot', labels = 'on', elev=None, azim=None,save = False,save_path=None, file_name = None):
        """
        Plot and optionally save a 3D plot of points with specified view angles.
        Args:
        - points (array-like): A list or array of points where each point is a list or tuple of three floats (x, y, z).
        - save_path (str, optional): Path to save the plot image. If None, the plot will not be saved.
        - elev (float, optional): Elevation angle in the z plane for viewing. If None, the angle is not adjusted.
        - azim (float, optional): Azimuth angle in the x,y plane for viewing. If None, the angle is not adjusted.
        """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # x, y, z coordinates from points
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        z = [p[2] for p in points]
        ax.scatter(x, y, z, )
        if elev is not None or azim is not None:
                ax.view_init(elev=elev, azim=azim)
        if labels.lower() == 'on':
                ax.set_xlabel('X Coordinate')
                ax.set_ylabel('Y Coordinate')
                ax.set_zlabel('Z Coordinate')
        else:
                plt.axis('off')
        ax.set_title(title)
        plt.show()
        if save:
                path_to_save = save_path_generator(file_name, save_path, flag=None)
                print(f"Plot saved to {path_to_save}")



class Dim2:
    
    def __init__(self):
        pass
        
    @staticmethod
    def create_flat_image(size=(750, 750), color_mode='RGB', color = 'White'):
        """
        Create a white image of the specified size and color mode.
        Parameters:
        size (tuple): The dimensions of the image (width, height).
        color_mode (str): The color mode of the image, either 'RGB' or 'Gray'.
        Returns:
        numpy.ndarray: The created white image.
        """
        col = 255 if color.lower() == 'white' else 0
        if color_mode.lower() == 'rgb':
                image = np.ones((size[1], size[0], 3), dtype=np.uint8) * col
        elif color_mode.lower() == 'gray':
                image = np.ones((size[1], size[0]), dtype=np.uint8) * col
        else:
                raise ValueError("Invalid color mode. Choose 'RGB' or 'Gray'.")
        return image
    
    
    @staticmethod
    def detect_centerline(image,
                                thrhold1 = 7,
                                thrhold2 = 255,
                                c_map ='gray',
                                fig_size =(6, 6),
                                plt_title ='Medial Axis',
                                plt_axis=True,
                                show = True,
                                save=False,
                                save_path = None,
                                silently = False, 
                                just_return_medial = False):
        if isinstance(image, str):
                img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
                if img is None:
                        print("Error loading image")
                        return
        try:
                _, binary = cv2.threshold(image, thrhold1, thrhold2, cv2.THRESH_BINARY)
                binary = binary > 0
                skeleton = skeletonize(binary)
        except:
                try:
                        temp = ndi.distance_transform_edt(image)
                        _, binary = cv2.threshold(temp, thrhold1, thrhold2, cv2.THRESH_BINARY)
                        binary = binary > 0
                        skeleton = skeletonize(binary)
                except:
                        try:
                                skeleton = skeletonize(img)
                        except:
                                print("Error reading image")
                                print("Nothing worked!")
                                return
        skeleton = img_as_ubyte(skeleton)
        if just_return_medial:
                return skeleton
        else:
                pass
        plt.figure(figsize=fig_size)
        plt.imshow(skeleton, cmap=c_map) if show else None
        plt.title(plt_title) if show else None
        if plt_axis:
                plt.axis('off')
        if save:
                if save_path:
                        if not save_path.endswith(('.png' ,'.jpg')):
                                save_path = os.path.join(save_path, f'{plt_title}_{thrhold1}_{c_map}.jpg')
                        else:
                                pass
                else:
                        save_path = f'{plt_title}_{thrhold1}_{c_map}.jpg'
                plt.imsave(save_path,skeleton, cmap=c_map)
        if show:
                plt.show()
        else:
                if save and not silently:
                        print(f"Result is Saved in {save_path}")
                        return
                else:
                        return
        
#end#

