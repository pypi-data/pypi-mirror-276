import numpy as np


class Space:
    
    def __init__(self, p1 = None, p2 = None, points = None, p3 = None, line = None, circle = None):
        """
        line is like -> [ P, P] or -> [(i,j), (i,j)] -> it is two points!
        p is (i, j) -> is two axis atleast -> (i, j ,k) for 3 dim
        """
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.points = points
        self.line = line
        self.circle = circle
        
        if points is not None:
            self.points_y_min = None
            self.points_y_max = None
            self.points_x_min = None
            self.points_x_max = None
            self.points_x = None
            self.points_y = None
            self.points_list = None
            self.points_arr = None
            
            self.__check_points__()
    
    
    def __check_points__(self):
        
        if isinstance(self.points , list) :
            if self.points_list is None:
                self.points_list = self.points.copy()
                self.points_arr = np.asarray(self.points)
            else:
                self.points_list2 = self.points.copy()
                self.points_arr2 = np.asarray(self.points)
        else:
            try:
                if self.points_list is None:
                    self.points_list = list(self.points)
                    self.points_arr = np.array(self.points)
                else:
                    self.points_list2 =  list(self.points)
                    self.points_arr2 = np.array(self.points)
            except Exception as e:
                print( "Please pass your points in whether a list or an array ")
                raise Exception(e)
        self.points = None
        self.__handle_points__()
    
    
    def __handle_points__(self):
        
        if self.points_x is None:
            points_z = None
            self.points_x = self.points_arr[:,0]
            self.points_y = self.points_arr[:,1]
            try:
                points_z = self.points_arr[:,2]
            except:
                pass
            if points_z is not None:
                self.points_z = points_z
                points_z = None
        if hasattr(self, 'points_arr2'):
            points2_z = None
            self.points2_x = self.points_arr2[:,0]
            self.points2_y = self.points_arr2[:,1]
            try:
                points2_z = self.points_arr2[:,2]
            except:
                pass
            if points2_z is not None:
                self.points2_z = points2_z
                points2_z = None
        
        self.__find_min__()
        self.__find_max__()
    
    
    def __find_min__(self):
        
        if self.points_y_min is None:
            points_x_min_i = np.min(self.points_x)
            points_x = list(self.points_x)
            points_x_min_i_where = points_x.index(points_x_min_i)
            points_x_min_j = self.points_y[points_x_min_i_where]
            self.points_x_min = (points_x_min_i, points_x_min_j)
            points_y_min_j = np.min(self.points_y)
            points_y = list(self.points_y)
            points_y_min_j_where = points_y.index(points_y_min_j)
            points_y_min_i = self.points_x[points_y_min_j_where]
            self.points_y_min = (points_y_min_i, points_y_min_j)
        if hasattr(self, 'points2_x'):
            points2_x_min_i = np.min(self.points2_x)
            points2_x = list(self.points2_x)
            points2_x_min_i_where = points2_x.index(points2_x_min_i)
            points2_x_min_j = self.points2_y[points2_x_min_i_where]
            self.points2_x_min = (points2_x_min_i, points2_x_min_j)
            points2_y_min_j = np.min(self.points2_y)
            points2_y = list(self.points2_y)
            points2_y_min_j_where = points2_y.index(points2_y_min_j)
            points2_y_min_i = self.points2_x[points2_y_min_j_where]
            self.points2_y_min = (points2_y_min_i, points2_y_min_j)
    
    
    def __find_max__(self):
        
        if self.points_y_max is None:
            points_x_max_i = np.max(self.points_x)
            points_x = list(self.points_x)
            points_x_max_i_where = points_x.index(points_x_max_i)
            points_x_max_j = self.points_y[points_x_max_i_where]
            self.points_x_max = (points_x_max_i, points_x_max_j)
            points_y_max_j = np.max(self.points_y)
            points_y = list(self.points_y)
            points_y_max_j_where = points_y.index(points_y_max_j)
            points_y_max_i = self.points_x[points_y_max_j_where]
            self.points_y_max = (points_y_max_i, points_y_max_j)
        
        if hasattr(self, 'points2_x'):
            points2_x_max_i = np.max(self.points2_x)
            points2_x = list(self.points2_x)
            points2_x_max_i_where = points2_x.index(points2_x_max_i)
            points2_x_max_j = self.points2_y[points2_x_max_i_where]
            self.points2_x_max = (points2_x_max_i, points2_x_max_j)
            points2_y_max_j = np.max(self.points2_y)
            points2_y = list(self.points2_y)
            points2_y_max_j_where = points2_y.index(points2_y_max_j)
            points2_y_max_i = self.points2_x[points2_y_max_j_where]
            self.points2_y_max = (points2_y_max_i, points2_y_max_j)
    
#end#