
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from SimpleS.utils import save_path_generator
import scipy.ndimage as ndi
from skimage import img_as_ubyte
from skimage.morphology import skeletonize




def rotate_2d_points(points, theta=0, axis=None):
    """Rotate or reflect 2D points by theta degrees around the origin or inverting the specified axis."""
    points = np.asarray(points)
    if points.shape[1] != 2:
        raise ValueError("Points should be in shape (n, 2)")
    if axis == 'x':
        # invert the y-coordinates.
        rot_matrix = np.array([
            [1, 0],
            [0, -1]
        ])
    elif axis == 'y':
        # invert the x-coordinates.
        rot_matrix = np.array([
            [-1, 0],
            [0, 1]
        ])
    else:
        # rotation around the origin by theta.
        theta = np.radians(theta)
        rot_matrix = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ])
    return np.dot(points, rot_matrix.T)




def create_flat_image(size=(750, 750), color_mode='RGB', color = 'White',return_ = True, save = False, save_path = None, file_name = None):
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
        if save:
                path_to_save = save_path_generator(file_name, save_path, flag=f'{size}_{color}')
                plt.imsave(path_to_save, image)
        if return_:
                return image
        else:
                return


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
