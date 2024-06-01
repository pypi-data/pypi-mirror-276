# In The Name of God ##
import os
import cv2
import time
import tempfile
import numpy as np
from skimage import draw
import scipy.ndimage as ndi
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from SimpleS.utils import save_path_generator
from scipy.ndimage import binary_dilation



def invert_image_color(image, save = False, save_path = None, file_name = None):
    
    if isinstance(image, str):
        with Image.open(image) as img:
            img = img
    else:
        try:
            img = Image.fromarray(image)
        except Exception as e:
            TypeError(f" You Should pass a valid path to a valid image ! to this Function could work! \n in addition: {e}")
    try:
            img = img.convert('RGBA')
            datas = img.getdata()
            new_data = [(0, 0, 0, 255) if all(c > 200 for c in item[:3]) else (255, 255, 255, 255) for item in datas]
            img.putdata(new_data)
            width, height = img.size
            fill_point = (int(width / 2), int(height / 2))  # Consider allowing parameterization
            ImageDraw.floodfill(img, xy=fill_point, value=(255, 255, 255, 255), thresh=50)
            img = img.convert('L').convert('1')
    except Exception as e:
        print(f"An error occurred: {e}")
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        img.save(tmp.name)
        tmp.seek(0)
        inverted_image = plt.imread(tmp.name)
    os.unlink(tmp.name)
    if save:
        save_path = save_path_generator(file_name,  save_path, flag=None)  
        plt.imsave(save_path, inverted_image)
    
    return inverted_image


def show_image(image, title="Image", c_map = 'gray',interpolation = 'nearest',save = False, save_path = None, file_name = None):
    """
    Display an image from a numpy array using matplotlib.
    Parameters:
    image_array (numpy.ndarray): The image data in a numpy array format.
    title (str): The title of the image window.
    """
    if isinstance(image, str):
        image = cv2.imread(image)
    if image.dtype == bool:
        image = image.astype(np.uint8) * 255
    elif image.dtype != np.uint8:
        image = image - image.min()
        max_val = image.max()
        if max_val > 0:
            image = image / max_val
    plt.title(title)
    plt.axis('off')
    if save:
        path_to_save = save_path_generator(file_name,save_path,flag=None )
        plt.imsave(path_to_save, image, cmap=c_map)
    plt.imshow(image, cmap=c_map, interpolation=interpolation)
    
    plt.show()


def fill_inside_3d_image(image, iterations=5, structure=None, structure_like = (3,3) , save = False, save_path = None, file_name = None):
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
                path_to_save = save_path_generator(file_name, save_path, flag=None)
                plt.imsave(path_to_save, image )
        
        return filled_image


def fill_shape_in_image(image, points, color = (255, 0, 0)):
    """
    Fill an area of a shape in an image based on the points defining the edges of the shape.
    Parameters:
    image (numpy.ndarray): The image where the shape is to be filled.
    points (list of tuples): A list of (x, y) tuples defining the vertices of the shape.
    color (tuple): A tuple defining the color to fill the shape. For grayscale, use one value; for color, use (B, G, R).
    Returns:
    numpy.ndarray: The modified image with the filled shape.
    """
    points_array = np.array(points, dtype=np.int32).reshape((-1, 1, 2))
    cv2.fillPoly(image, [points_array], color)
    return image


def force_image_to_grayscale(image):
    holder = 0.2989
    keeper = 0.5870
    informer = 0.1140
    gray_image = holder * image[:, :, 0] + keeper * image[:, :, 1] + informer * image[:, :, 2]
    return gray_image


def read_image_in_grayscale(image_path, thrhold = 127, type = 'THRESH_BINARY', also_make_it_binary = False , binary_image_color = 255 ):
    # Read the image in grayscale mode
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError("The specified image could not be loaded.")
    type_options = [cv2.THRESH_BINARY, cv2.THRESH_BINARY_INV, cv2.THRESH_TRUNC, cv2.THRESH_TOZERO, cv2.THRESH_TOZERO_INV]
    
    if type == 'THRESH_BINARY':
        _, binary_img = cv2.threshold(img, thrhold, 255, type_options[0])
    elif type == 'THRESH_BINARY_INV':
        _, binary_img = cv2.threshold(img, thrhold, 255, type_options[1])
    elif type == 'THRESH_TRUNC':
        _, binary_img = cv2.threshold(img, thrhold, 255, type_options[2])
    elif type == 'THRESH_TOZERO':
        _, binary_img = cv2.threshold(img, thrhold, 255, type_options[3])
    elif type == 'THRESH_TOZERO_INV':
        _, binary_img = cv2.threshold(img, thrhold, 255, type_options[4])
    else:
        raise AssertionError(" The type arg should be THRESH_BINARY or THRESH_BINARY_INV or THRESH_TRUNC or THRESH_TOZERO or THRESH_TOZERO_INV")
    if also_make_it_binary:
        try:
            binary_img = binary_img == binary_image_color
        except Exception as e:
            print(f"Fail to create binary in color specified! {e}")
            time.sleep(3)
            print("Returning The cv2 Object")
    
    return binary_img


def simple_binary_image_creator(points, 
                                    image_size = None, 
                                    size_of_edge_points = (2, 2),
                                    iterations = 2,
                                    enlarge_points=True, 
                                    smoothing = False):
        """
        Create a binary image from a list of points.
        :param points: List of tuples (x, y) representing the coordinates of points.
        :param image_size: Tuple (width, height) for the output image size.
        :param smoothing: Boolean, if True apply Gaussian blur to smooth the image.
        :param enlarge_points: Boolean, if True apply dilation to make points larger.
        :return: NumPy array representing the binary image.
        """
        img_size = (  int( points.max() )  , int( points.max() ) ) if image_size is None else image_size
        img = np.zeros((img_size[1], img_size[0]), dtype=np.uint8)
        points = np.array(points)
        min_vals = points.min(axis=0)
        max_vals = points.max(axis=0)
        scaled_points = (points - min_vals) / (max_vals - min_vals)
        scaled_points[:, 0] *= (img_size[0] - 1)
        scaled_points[:, 1] *= (img_size[1] - 1)
        scaled_points = scaled_points.astype(int)
        for x, y in scaled_points:
                img[y, x] = 255
        if enlarge_points:
                kernel = np.ones(size_of_edge_points, np.uint8)
                img = cv2.dilate(img, kernel, iterations=iterations)
        if smoothing:
                img = cv2.GaussianBlur(img, (5, 5), 0)
        
        return img


def advance_binary_image_creator(points, shape_size = None):
        
        shape_size =  (  int( points.max() )  , int( points.max() ) ) if shape_size is None else shape_size
        img = np.zeros(shape_size, dtype=bool)
        rr, cc = draw.polygon(points[:, 1], points[:, 0], shape=img.shape)
        img[rr, cc] = True
        img = ndi.binary_fill_holes(img)
        img = ndi.gaussian_filter(img.astype(float), sigma=1)
        img = img > 0.5
        
        return img


def detect_edges(image, 
                 n1=100, 
                 n2=100,  
                 show_edges = True, 
                 show_contours=True, 
                 title_for_detected_edges = 'Detected Edges',
                 title_for_detected_contours = 'Detected Edges with Contours',
                 return_edges = False, 
                 return_contours = False, 
                 range_color_start=100, 
                 range_color_end=255, 
                 save = False,
                 save_path = None,
                 file_name = None):
    
    if isinstance(image, str):
        image = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError(f"Image file '{image}' not found or could not be read.")
    elif isinstance(image, np.ndarray):
        if len(image.shape) != 2:
            raise ValueError("Image must be a grayscale image.")
    else:
        raise TypeError("Input must be a file path (str) or a grayscale image (numpy.ndarray).")
    
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
    
    _, binary_image = cv2.threshold(blurred_image, 127, 255, cv2.THRESH_BINARY)
    
    kernel = np.ones((5, 5), np.uint8)
    closed_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)
    
    edges = cv2.Canny(closed_image, n1, n2, apertureSize=3)
    if show_edges:
        plt.imshow(edges, cmap='gray')
        plt.title(title_for_detected_edges)
        plt.axis('off')
        plt.show()
    if save:
        path_to_save = save_path_generator(file_name, save_path, flag = 'DetectedEdges')
        plt.imsave(path_to_save, edges)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    canvas = np.zeros_like(image)
    for contour in contours:
        color = np.random.randint(range_color_start, range_color_end, size=3, dtype=np.uint8)
        color = tuple(map(int, color))
        cv2.drawContours(canvas, [contour], -1, color, 2)
    
    canvas_rgb = cv2.cvtColor(canvas, cv2.COLOR_GRAY2BGR)
    canvas_rgb = cv2.cvtColor(canvas_rgb, cv2.COLOR_BGR2RGB)
    if show_contours:
        plt.imshow(canvas_rgb)
        plt.title(title_for_detected_contours)
        plt.axis('off')
        plt.show()
    if save:
        path_to_save = save_path_generator(file_name, save_path, flag = 'DetectedContours')
        plt.imsave(path_to_save, canvas_rgb)
    
    if return_edges and return_contours:
        return edges, canvas
    elif return_edges:
        return edges
    elif return_contours:
        return canvas
    else:
        return
#end#
