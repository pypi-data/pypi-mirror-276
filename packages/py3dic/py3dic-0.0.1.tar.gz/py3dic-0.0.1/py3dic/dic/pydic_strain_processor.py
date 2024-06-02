#%%[markdown ]
# # Dic_processor.py
#
# Python module that handles batch Digital Image Correlation (DIC) processing. 
# Provides a class `DICProcessorBatch` that takes a result file and optional parameters 
# to process DIC data.
#
# ## Classes
#
# ### `DICProcessorBatch`
#
# An object-oriented representation of a batch DIC processor. Provides methods to process 
# DIC data, save images, compute displacement and strain, add metadata, and more.
#
# #### Attributes:
#
# - `result_file` : A result file given by the init() function
# - `interpolation` : Interpolation type for smoothing data
# - `save_image` : Boolean to decide if result images are saved
# - `scale_disp` : Scale to amplify the displacement of images
# - `scale_grid` : Scale to amplify the grid of images
# - `strain_type` : Strain type, can be 'cauchy', '2nd_order' or 'log'
# - `rm_rigid_body_transform` : Boolean for removing rigid body displacement
# - `meta_info_file` : Path to a meta info file, a csv file with additional data
# - `unit_test_mode` : Boolean to run in unit test mode
#
# #### Methods:
#
# - `__init__()` : Initializes a DICProcessorBatch object
# - `grids()` : Returns the grid list
# - `process_data()` : Main function for processing files
# - `add_metadata_to_grid_object()` : Adds metadata to grid object
# - `write_image_files()` : Writes image files (marked, displacement, grid)
# - `_process_single_grid()` : Processes a single grid
# - `plot_strain_map_with_id()` : Plots strain map with ID
# - `read_meta_info_file()` : Reads the meta info file
# - `read_result_file()` : Reads the result file

#%%
import copy
import os
import pathlib
import sys


import pandas as pd
import numpy as np
from py3dic.dic.pydicGrid import DIC_Grid

import logging
from ._pydic_support import (compute_disp_and_remove_rigid_transform,
                             compute_displacement)
#%%
# write a function that takes a 2d numpy array and returns all the element except the border. Make sure that you assert that its a 2d array and it has more than 3 element in each direction. Please also add type annotation and a description of the function
def remove_border(array:np.ndarray)->np.ndarray:
    """Removes the border of a 2d numpy array.

    Args:
        array (np.ndarray): 2d numpy array

    Returns:
        np.ndarray: 2d numpy array without the border
    """
    assert array.ndim == 2, "array should be 2d"
    assert array.shape[0] > 3 and array.shape[1] > 3, "array should have more than 3 elements in each direction"
    return array[1:-1, 1:-1]



#%%


class DICProcessorBatch:
    grid_list:list[DIC_Grid] = [] # saving grid here
    STRAINS_TIME_XLSX_FILE:str = "df_strain_wt.xlsx"

    def __init__(self, result_file, 
            interpolation='raw', 
            save_image=True, 
            scale_disp=4., scale_grid=25., 
            strain_type='cauchy', 
            rm_rigid_body_transform=True, 
            meta_info_file=None,
            unit_test_mode:bool = False,
            analysis_folder:str= None):
        """* required argument:
        - the first arg 'result_file' must be a result file given by the init() function
        * optional named arguments ;
        - 'interpolation' the allowed vals are 'raw', 'spline', 'linear', 'delaunnay', 'cubic', etc... 
        a good value is 'raw' (for no interpolation) or spline that smooth your data.
        - 'save_image ' is True or False. Here you can choose if you want to save the 'disp', 'grid' and 
        'marker' result images
        - 'scale_disp' is the scale (a float) that allows to amplify the displacement of the 'disp' images
        - 'scale_grid' is the scale (a float) that allows to amplify the 'grid' images
        - 'meta_info_file' is the path to a meta info file. A meta info file is a simple csv file 
        that contains some additional data for each pictures such as time or load values.
        - 'strain_type' should be 'cauchy' '2nd_order' or 'log'. Default value is cauchy (or engineering) strains. You 
        can switch to log or 2nd order strain if you expect high strains. 
        - 'rm_rigid_body_transform' for removing rigid body displacement (default is true)
        """
        self.result_file = result_file
        self.interpolation = interpolation
        self.save_image = save_image
        self.scale_disp = scale_disp
        self.scale_grid = scale_grid
        self.strain_type = strain_type
        self.rm_rigid_body_transform = rm_rigid_body_transform
        self.meta_info_fname = meta_info_file
        self.__unit_test_mode = unit_test_mode
        self._analysis_folder = analysis_folder
        self.meta_info = {}

        if self.meta_info_fname:
            self.read_meta_info_file()

    @property
    def grids(self)->list:
        """retuns the grid list. 

        Returns:
            _type_: _description_
        """        
        return self.grid_list
    
    def get_grid(self, id:int)->DIC_Grid:
        """function that returns one of the grids in the analysis. 

        Args:
            id (int): _description_

        Returns:
            DIC_Grid: _description_
        """        
        return self.grid_list[id]

    def process_data(self):
        """main function for processing files
        """        
        self.grid_list = [] # saving grid here
        
        # read dic result file
        self.read_result_file()
        # compute displacement and strain
        for i, mygrid in enumerate(self.grid_list):
            self._process_single_grid(i, mygrid)
            # write image files
            if (self.save_image):
                self.write_image_files(mygrid)

            if not self.__unit_test_mode:
                # write result file
                mygrid.write_result(analysis_folder=self._analysis_folder)

            # add meta info to grid if it exists
            self.add_metadata_to_grid_object(mygrid)

    def add_metadata_to_grid_object(self, mygrid):
        """Adds metadata to grid object.

        Args:
            mygrid (_type_): _description_
        """        
        if (len(self.meta_info) > 0):
            img = os.path.basename(mygrid.image)
                #if not meta_info.has_key(img):
            if img not in self.meta_info.keys():
                print("warning, can't affect meta deta for image", img)
            else:
                mygrid.add_meta_info(self.meta_info.get(img))
                print('add meta info', self.meta_info.get(img))

    def write_image_files(self, mygrid:DIC_Grid):
        """write timage files (marked, displacement, grid)

        Args:
            mygrid (_type_): _description_
        """        
        win_size_x, win_size_y = self.win_size[0], self.win_size[1]
        mygrid.draw_marker_img(analysis_folder=self._analysis_folder)
        mygrid.draw_disp_img(self.scale_disp, analysis_folder=self._analysis_folder)
        mygrid.draw_grid_img(self.scale_grid, analysis_folder=self._analysis_folder)
        if win_size_x == 1 and win_size_y == 1 : 
            mygrid.draw_disp_hsv_img()

    def _process_single_grid(self, i:int, mygrid:DIC_Grid):
        """_summary_

        Args:
            i (int): _description_
            mygrid (grid): I could use self.grid_list[i] instead of mygrid
        """        
        print("compute displacement and strain field of", self.image_list[i], "...")
        disp = None
        if self.rm_rigid_body_transform:
            print("remove rigid body transform")
            disp = compute_disp_and_remove_rigid_transform(self.point_list[i], self.point_list[0])
        else:
            print("do not remove rigid body transform")
            disp = compute_displacement(self.point_list[i], self.point_list[0])
        mygrid.add_raw_data(winsize=self.win_size, 
                            reference_image=self.image_list[0], 
                            image=self.image_list[i], 
                            reference_point=self.point_list[0], correlated_point=self.point_list[i], 
                            disp=disp)
        
        self.disp_list.append(disp)
        mygrid.interpolate_displacement(self.point_list[0], disp, method=self.interpolation)

        if (self.strain_type == 'cauchy'):
            mygrid.compute_strain_field()
        elif (self.strain_type =='2nd_order'):
            mygrid.compute_strain_field_DA()
        elif (self.strain_type =='log'):
            mygrid.compute_strain_field_log()
        else:
            raise ValueError("please specify a correct strain_type : 'cauchy', '2nd_order' or 'log'")

    def plot_strain_maps(self, id=100):
        """function for plotting all three strain types. 
        # TODO remove dependence on plotfield/simplify.

        Args:
            id (int, optional): _description_. Defaults to 100.
        """        
        self.plot_strain_map_with_id(id, strain_type='xx')
        self.plot_strain_map_with_id(id, strain_type='yy')
        self.plot_strain_map_with_id(id, strain_type='xy')


    def plot_strain_map_with_id(self, id, strain_type:str):
        assert (id < len(self.grid_list) and id>0),  "id does not correspond to an image" 
        assert strain_type in ['xx', 'yy', 'xy'], "strain type should be one of ['xx', 'yy', 'xy']"
        # tmp_grid = self.grid_list[id]
        tmp_grid = self.get_grid(id)
        if strain_type == 'xx':
            # TODO replace with 
            # tmp_grid.plot_field(tmp_grid.strain_xx, title= 'xx strain')
            tmp_grid.plot_field(tmp_grid.strain_xx, 'xx strain')
        elif strain_type == 'yy':
            tmp_grid.plot_field(tmp_grid.strain_yy, 'yy strain')
        elif strain_type == 'xy':
            tmp_grid.plot_field(tmp_grid.strain_xy, 'xy strain')
        
    def read_meta_info_file(self):
        """ Read the meta info file and store the information in the meta_info dictionary.

        This function reads the meta info file specified by the `self.meta_info_file` attribute. The file
        should be in CSV format, with the first row as the header containing field names. The following
        rows should contain values corresponding to the field names. The function parses the file and
        stores the information in the `self.meta_info` dictionary, with the first value in each row as
        the key and the rest of the values as a dictionary.

        Example of meta info file format:
            image , time, load
            img_001, 0.1, 500
            img_002, 0.2, 520
            img_003, 0.3, 550

        The resulting self.meta_info dictionary will look like:
            {
                "img_001": {"time": 0.1, "load": 500},
                "img_002": {"time": 0.2, "load": 520},
                "img_003": {"time": 0.3, "load": 550},
            }
        """
        print(f'read meta info file{self.meta_info_fname}...')
        with open(self.meta_info_fname) as f:
            lines = f.readlines()
            header = lines[0]
            field = header.split()
            for l in lines[1:-1]:
                val = l.split()
                if len(val) > 1:
                    dictionary = dict(zip(field, val))
                    self.meta_info[val[0]] = dictionary

    def read_result_file(self):
        """ Read the result file and extract the grid, point_list, image_list, and disp_list.

        NOTE: this method 
        -  reads the results file and 
        - produces a gridXY which is then used to 
        - initialize a mygrid object. 
        - the mygrid object is copied and it initialises the grid list

        Additionally 

        This method reads the result file provided by the user, parses the contents of the file,
        and extracts the grid parameters, point_list, image_list, and disp_list from it. The
        extracted data is then stored as instance variables of the class for further processing.

        Args:
            self (object): The instance of the class for which the method is called.

        Attributes:
            win_size (tuple): A tuple containing the dimensions of the window size (win_size_x, win_size_y).
            point_list (list): A list of arrays containing the points extracted from the result file.
            image_list (list): A list of image names (strings) extracted from the result file.
            disp_list (list): A list of displacement values extracted from the result file.
            grid_list (list): A list of grids created from the parsed result file.

        """
        # first create a pristine version of the grid
        with open(self.result_file) as f:
            head = f.readlines()[0:2]
        (xmin, xmax, xnum, win_size_x) = [float(x) for x in head[0].split()]
        (ymin, ymax, ynum, win_size_y) = [float(x) for x in head[1].split()]
        self.win_size = (win_size_x, win_size_y)
        
        grid_x, grid_y = np.mgrid[xmin:xmax:int(xnum)*1j, ymin:ymax:int(ynum)*1j]
        mygrid = DIC_Grid(grid_x, grid_y, int(xnum), int(ynum))

        # the results
        self.point_list = []
        self.image_list = []
        self.disp_list = []

        # parse the result file
        with open(self.result_file, 'r', encoding='utf-8') as f:
            res = f.readlines()[2:-1]
            for line in res:
                # this repeats for all the images
                val = line.split('\t')
                self.image_list.append(val[0])
                point = []
                for pair in val[1:-1]:
                        (x,y) = [float(x) for x in pair.split(',')]
                        point.append(np.array([np.float32(x),np.float32(y)]))
                self.point_list.append(np.array(point))

                # Create a copy of mygrid 
                self.grid_list.append(copy.deepcopy(mygrid))
        f.close()

    def obtain_strain_curve(self, func=None)->pd.DataFrame:
        """this is a function that calculates the strain curve based on vs the image number. 

        # TODO: if func is 
        #    - callable the provide it as is.
        #    - float between [0,1] then use it in fraction
        #    - None: use fraction 0

        Returns:
            pd.DataFrame: dataframe that contains (mean xx, std_ xx, mean e_yy, std_yy) for all images
        """
        def portion_function(fraction:float):
            def inner(array):
                xmax, ymax = array.shape
                x_start, x_end = np.floor(fraction*xmax).astype('int'), np.ceil((1-fraction)*xmax).astype('int')
                y_start, y_end = np.floor(fraction*ymax).astype('int'), np.ceil((1-fraction)*ymax).astype('int')
                # print([x_start,x_end, y_start, y_end])
                portion = array[x_start:x_end, y_start:y_end]
                return portion
            return inner

        
        # TODO: comment/uncomment the following two lines to change the default behaviour
        # that makes use of the border removal function. 
        # needs checks and tests to see if the std indeed improves.
        # func = portion_function(fraction=0) if func is None else func
        func = remove_border if func is None else func
        assert callable(func), "func needs to be callable or a function"

        grid_list = self.grid_list
        adic = []  # list of dictionaries that will become rows
        for j, gr in enumerate(grid_list):
            portion_xx = func(gr.strain_xx) 
            portion_yy = func(gr.strain_yy)
            adic.append({"id":j+1, "file": pathlib.Path(gr.image).name,
                         "e_xx":portion_xx.mean(), "e_xx_std": portion_xx.std(),
                         "e_yy":portion_yy.mean(), "e_yy_std": portion_yy.std()})
        df = pd.DataFrame(adic)
        return df
    
    def get_df_with_time(self, func=None, save_to_file:bool=False)->pd.DataFrame:
        """Merges the results from the images with the meta_data file

        Args:
            func (_type_, optional): _description_. Defaults to None.

        Returns:
            pd.DataFrame: _description_
        """
        df_dic_notime = self.obtain_strain_curve(func=func)
        # Read the data from the *_meta-data.txt* 
        df_img_meta = pd.read_csv(self.meta_info_fname, sep="\t")

        # merge the two files
        df_dic_tot = pd.merge(df_dic_notime, df_img_meta, how="inner", on="file")
        if save_to_file:
            
            pp_outputdir = pathlib.Path(self._analysis_folder)
            pp_outputdir.mkdir(parents=True, exist_ok=True)
            DIC_EXCEL_OUTPUT = pp_outputdir/self.STRAINS_TIME_XLSX_FILE
            df_dic_tot.to_excel(DIC_EXCEL_OUTPUT)
            df_dic_tot.to_csv(DIC_EXCEL_OUTPUT.with_suffix(".csv")) # keep this if there are any change when changing the code observe changes during code refactoring
            logging.info(f"Saved df with time to :{DIC_EXCEL_OUTPUT}")
        return df_dic_tot
