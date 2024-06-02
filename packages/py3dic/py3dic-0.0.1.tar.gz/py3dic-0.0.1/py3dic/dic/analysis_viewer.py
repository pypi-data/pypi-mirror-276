#%% 
# Analysis viewer
# this is a viewer for the DIC analysis results
#
# it aims to create a class that acts as a container for the DIC analysis results
# and provides methods to visualize the results

#%%
import pathlib
from datetime import datetime
import json

import tkinter as tk
from tkinter import filedialog

import numpy as np
# import pandas as pd
# from matplotlib import pyplot as plt
# import matplotlib.tri as tri

from py3dic.dic.pydicGrid import GridSize
from py3dic.dic._pydic_support import compute_disp_and_remove_rigid_transform, compute_displacement
from py3dic.dic import DIC_Grid
from py3dic.dic.misc import get_file_list 

import logging
# logging.basicConfig(level = logging.DEBUG)
logging.basicConfig(level = logging.WARNING)
#%%
class GridDataContainer:
    """Class for storing and Grid data from DIC analysis results.

    """
    grid_size:GridSize=None

    def __init__(self, filename:str):
        """Initializes the AnalysisResults object.
        """
        self.filename = filename
        # self.xmin = None
        # self.xmax = None
        # self.xnum = None
        # self.x_window_size = None
        # self.ymin = None
        # self.ymax = None
        # self.ynum = None
        # self.y_window_size = None
        self.imagelist = []
        self.pointlist = []
        self._parse_file()

    @property
    def grid_points_ref(self) -> np.ndarray:
        """Returns the grid points in the test imagelist.

        Returns:
            np.ndarray: The grid points.
        """
        return self.pointlist[0]

    def grid_point_xy_no(self, frame_id:int) -> np.ndarray:
        """Returns the position of the grid points in the test imagelist.

        args:
            frame_id (int): The frame id.
        Returns:
            np.ndarray: The [x,y] positions for grid with frameid .
        """
        return self.pointlist[frame_id]

    @property
    def no_frames(self) -> int:
        """Returns the number of frames in the test imagelist.

        Returns:
            int: The number of frames.
        """
        return len(self.imagelist)

    def _parse_file(self):
        """Parses the result file and stores the data in the object's attributes.

        """
        with open(self.filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # # Parse grid dimensions and window sizes
        # (self.xmin, self.xmax, self.xnum, self.x_window_size) = [int(float(x)) for x in lines[0].split()]
        # (self.ymin, self.ymax, self.ynum, self.y_window_size) = [int(float(x)) for x in lines[1].split()]
        # self._gs:GridSize = GridSize(xmin=self.xmin, xmax=self.xmax, 
        #                     xnum = self.xnum, win_size_x=self.x_window_size,
        #                     ymin=self.ymin, ymax=self.ymax, 
        #                     ynum = self.ynum, win_size_y=self.y_window_size)    
        self.grid_size = GridSize.from_result_dic(self.filename)
        # Parse image and point data
        for line in lines[2:-1]:
            val = line.split('\t')
            self.imagelist.append(val[0])
            points = [np.array([float(x) for x in pair.split(',')], dtype=np.float32) for pair in val[1:-1]]
            self.pointlist.append(np.array(points))


#%%
class DICAnalysisResultContainer:
    def __init__(self, analysis_json_fname:str, img_extension = 'png') -> None:
        """Initializes the DICAnalysisResultContainer object.

        Args:
            analysis_json (str): The path to the analysis json file.
        """
        # load the analysis json file	
        self.analysis_json = analysis_json_fname
        self._load_analysis_json()

        # initialise the grid data container
        self.grid_data_container = GridDataContainer(str(self.pp_DISPL_ANALYSIS_OUTPUT))

        # load image file list:
        
        # or 'png', 'bmp', etc.
        self.image_flist = get_file_list(self.pp_IMG_DIR.absolute(), img_extension)

        # load all the csv files from the result folder
        self.csv_flist = get_file_list(str(self.pp_ANALYSIS_RES_FOLDER/"result"),
                             file_extension='csv')
        # self._load_analysis_results()

    def _load_analysis_json(self):
        """Loads the analysis json file and stores the data in the object's attributes.

        """
        # Read the contents of the JSON file
        with open(self.analysis_json, 'r', encoding='utf-8') as file:
            self.analysis_data = json.load(file)

        # print("Contents of the file:", self.analysis_data)
        self.pp_json = pathlib.Path(self.analysis_json)
        self.pp_IMG_DIR = pathlib.Path(self.analysis_data.get('Image Folder',None))
        self.pp_ANALYSIS_RES_FOLDER = self.pp_json.parent
        self.pp_DISPL_ANALYSIS_OUTPUT = self.pp_ANALYSIS_RES_FOLDER /'result.dic'

        # add analysis configuration parameters
        self.roi_window = self.analysis_data.get('ROI Selection',None)
        self.window_size = self.analysis_data.get('correl_window_size',None)
        self.grid_size = self.analysis_data.get('correl_grid_size',None)
        self.interpolation = self.analysis_data.get('interpolation',None)
        self.strain_type = self.analysis_data.get('strain type',None)
        self.remove_rigid_translation = self.analysis_data.get('remove translation',True)

    def print_analysis_data(self):
        """Prints the analysis data.

        """	
        for k,v in self.analysis_data.items():
            print(f"{k:25s} : {v:}")
        print(f"================ Config Parameters ================")
        print(f"image dir    : {self.pp_IMG_DIR}")
        print(f"analysis dir : {self.pp_ANALYSIS_RES_FOLDER}")
        print(f"analysis file: {self.pp_json}")
        print(f"ROI          : {self.roi_window}")
        print(f"window size  : {self.window_size}")
        print(f"grid size    : {self.grid_size}")
        print(f"remove rigid : {self.remove_rigid_translation}")
        print(f"interpolation: {self.interpolation}")
        print(f"strain type  : {self.strain_type}")

    @property
    def point_list(self)   -> list:
        """Returns the list for all frames with for the XY coordinate for all grid points.

        e.g. point_list[0] returns the XY coordinates for the first frame
        """ 
        return self.grid_data_container.pointlist

    def get_grid(self, frame_id:int) -> DIC_Grid:
        """Returns the grid points in the test imagelist.

        Args:
            frame_id (int): The frame id (keep in mind that it starts with 1).
        Returns:
            np.ndarray: The grid points.
        """
        assert frame_id >=1 and isinstance(frame_id, int), "frame_id must be an integer >=1"
        mygrid = self.grid_data_container.grid_size.create_DIC_Grid()

        zb_fr_id = frame_id - 1

        print("compute displacement and strain field of", self.image_flist[zb_fr_id], "...")
        disp = None
        if self.remove_rigid_translation:
            logging.info("remove rigid body transform")
            disp = compute_disp_and_remove_rigid_transform(self.point_list[zb_fr_id], self.point_list[0])
        else:
            logging.info("do not remove rigid body transform")
            disp = compute_displacement(self.point_list[zb_fr_id], self.point_list[0])
        mygrid.add_raw_data(winsize=self.grid_data_container.grid_size.win_size, 
                            reference_image=self.image_flist[0], 
                            image=self.image_flist[zb_fr_id], 
                            reference_point=self.point_list[0], correlated_point=self.point_list[zb_fr_id], 
                            disp=disp)
        
        mygrid.interpolate_displacement(self.point_list[0], disp, method=self.interpolation)

        if (self.strain_type == 'cauchy'):
            mygrid.compute_strain_field()
        elif (self.strain_type =='2nd_order'):
            mygrid.compute_strain_field_DA()
        elif (self.strain_type =='log'):
            mygrid.compute_strain_field_log()
        else:
            raise ValueError("please specify a correct strain_type : 'cauchy', '2nd_order' or 'log'")

        return mygrid
# %%

