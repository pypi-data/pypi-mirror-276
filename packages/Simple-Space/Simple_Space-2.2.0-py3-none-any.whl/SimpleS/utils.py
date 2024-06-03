import datetime
import os

def save_path_generator(filename = None, path = None, flag = None):
        
        try:
                if path is not None:
                        if not path.endswith('.png') or not path.endswith('.jpg'):
                                path = path
                        else:
                                path = 'results'
                else:
                        path = 'results'
                os.makedirs(path,exist_ok=True)
                if filename is not None:
                        if not filename.endswith('.png') or not filename.endswith('.jpg'):
                                filename = filename + '.png'
                        else:
                                filename = filename
                else:
                        now = datetime.datetime.now()
                        now = now.strftime('%Y%m%d-%H%M%S')
                        filename = f'Fig{now}.png'
                if flag is not None:
                        filename = str(flag) + filename
                savepath = os.path.join(path,filename)
        except Exception as e:
                raise Exception(f"{e}")
        
        return savepath


def split_dim(arr):
        
        X = [point[0] for point in arr]
        Y = [point[1] for point in arr]
        
        return X, Y


def arr_to_list(arr):
        
        temp = []
        for i, j in arr :
                temp.append((int(i),int(j)))
        
        return temp
