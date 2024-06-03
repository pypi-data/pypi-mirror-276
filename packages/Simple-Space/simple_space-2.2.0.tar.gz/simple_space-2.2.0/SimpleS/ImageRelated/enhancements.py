# #                                                     In The Name of God # #
import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from SimpleS.utils import save_path_generator
print(" This is an Enhanced Version of the Original Script Provided by OpenCV site. ")
#https://www.github.com/cloner174
class ErosAndDilat:
    
    def __init__(self, image):
        
        if isinstance(image, str):
            self.image_path = image
            self.src = None
        else:
            self.src = image
        self.dilatation_result = None
        self.erosion_result = None
        self.path_to_erosion_result = None
        self.path_to_dilatation_result = None
    
    def erosion(self):
        erosion_shape = self.erosion_shape
        erosion_size = self.erosion_size
        element = cv.getStructuringElement(self.morph_shape(erosion_shape), (2 * erosion_size + 1, 2 * erosion_size + 1),(erosion_size, erosion_size))
        erosion_dst = cv.erode(self.src, element)
        return erosion_dst
    
    def dilatation(self):
        
        dilation_shape = self.dilation_shape
        dilatation_size = self.dilatation_size 
        element = cv.getStructuringElement(self.morph_shape(dilation_shape), (2 * dilatation_size + 1, 2 * dilatation_size + 1), (dilatation_size, dilatation_size))
        dilatation_dst = cv.dilate(self.src, element)
        
        return dilatation_dst
    
    def show_result(self, thing_to_show, title):
        
        plt.figure(figsize=(10, 5))
        plt.subplot(121)
        plt.title('Original Image')
        plt.imshow(self.src)
        plt.subplot(122)
        plt.title(title)
        plt.imshow(thing_to_show)

        plt.show()
    
    def save_result(self) :
        
        if self.erosion_result is not None:
            erofile_path = save_path_generator(self.file_name, self.save_path, flag = f'Erosion_SIZE{self.erosion_size}_SHAPE{self.erosion_shape}')
            plt.imsave(erofile_path, self.erosion_result)
            self.path_to_erosion_result = erofile_path
        if self.dilatation_result is not None:
            dilafile_path = save_path_generator(self.file_name, self.save_path, flag = f'Dilatation_SIZE{self.dilatation_size}SHAPE{self.dilation_shape}')
            plt.imsave(dilafile_path, self.dilatation_result)
            self.path_to_dilatation_result = dilafile_path
        return
    

    def main(self,
                eros = True, erosion_size=1, erosion_shape=0,#erosion_shape -> can be 0 or 1 or 2
                dilate = True, dilatation_size=1, dilation_shape=0,#erosion_shape -> can be 0 or 1 or 2
                show = True,
                return_ = False,
                save = False,
                save_path = 'results',
                file_name = None):
        
        self.eros = eros
        self.dilate = dilate
        self.erosion_size = erosion_size
        self.erosion_shape = erosion_shape
        self.dilatation_size = dilatation_size
        self.dilation_shape = dilation_shape
        self.save_path = save_path
        self.file_name = file_name
        if self.src is None:
            try:
                src = cv.imread(cv.samples.findFile(self.image_path))
                src = cv.cvtColor(src, cv.COLOR_BGR2RGB)
                if src is None:
                    print('Could not open or find the image: ', self.image_path)
                    exit(0)
                else:
                    self.src = src
            except:
                raise FileNotFoundError("Please check again the input file that was pased into this class")
                
        else:
            pass
        if eros:
            result = self.erosion()
            if show:
                self.show_result(result, title='Erosion Effect')
            self.erosion_result = result
        
        if dilate:
            result = self.dilatation()
            self.show_result(result, title='Dilatation Effect')
            self.dilatation_result = result
        if save:
            self.save_result()
        if return_:
            print('Use EnhanceImage objects to access the both Erosion Effected Image and Dilatation Effected')
    
    @staticmethod
    def morph_shape(val):
        
        if val == 0:
            return cv.MORPH_RECT
        elif val == 1:
            return cv.MORPH_CROSS
        elif val == 2:
            return cv.MORPH_ELLIPSE
    
#end#
