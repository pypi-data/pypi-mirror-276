#%%
import copy
import glob
import pathlib
import cv2
import numpy as np

from .misc import EnumInteropolation, EnumStrainType, EnumTrackingMethodType

from ._pydic_support import (AreaSelector,
                             compute_disp_and_remove_rigid_transform,
                             compute_displacement, remove_point_outside)
from .pydicGrid import DIC_Grid, draw_opencv_v2, GridSize
import logging



class SingleImageDisplacementProcessor:

    points_ref:np.ndarray = None   # array with initial X,Y position of markers
    img_ref:np.ndarray = None      # reference image

    def __init__(self, 
            reference_image:np.ndarray, 
            win_size_px:tuple, 
            grid_size_px:tuple,
            area_of_interest:list[tuple]=None, 
            verbosity:int = 1, 
            *args, **kwargs):
        """
        Initialize the ImageDisplacementProcessor.

        Args:
            reference_image (numpy.ndarray): a reference image (the result of imread)
            win_size_px (tuple): Size in pixels of the correlation windows as a (dx, dy) tuple.
            grid_size_px (tuple): Size of the correlation grid as a (dx, dy) tuple.
            result_file (str): Name of the result file.
            area_of_interest (list of two tuples, optional): Area of interest in [(top left x, top left y), (bottom right x, bottom right y)] format.
            verbosity (int) : verbosity level (0 is none e.g. testing, 5 is maximum)
        """
        # self.img_ref = cv2.imread(self.img_list[0], 0)
        self.img_ref = reference_image.copy()
        self._last_img = reference_image.copy()
        self._curr_img = reference_image.copy()

        #
        self.win_size_px = win_size_px
        self.grid_size_px = grid_size_px
        self.area_of_interest = area_of_interest
        self._verbosity_level = verbosity

        self.kwargs = kwargs
    
        self.preprocess()

    def preprocess(self):

        # TODO Remove this. 
        if self.area_of_interest is None:
            assert self._verbosity_level>0 , ""
            print("please pick your area of interest on the picture")
            print("Press 'c' to proceed")
            areaSelector = AreaSelector(self.img_ref)
            self.area_of_interest = areaSelector.pick_area_of_interest()

        self.init_correlation_grid()

        self.points_in = remove_point_outside(self.points_ref, self.area_of_interest, shape='box')

        if self._verbosity_level >=3:
            self.display_markers(self.points_in)

    def init_correlation_grid(self)-> np.ndarray:
        """
        Initialize the correlation grid with points of interest.

        Returns:
            points (array): Array of points of interest in the image sequence.
        """
        area = self.area_of_interest
        points = []

        if 'unstructured_grid' in self.kwargs:
            block_size, min_dist = self.kwargs['unstructured_grid']
            feature_params = dict(maxCorners=50000,
                                  qualityLevel=0.01,
                                  minDistance=min_dist,
                                  blockSize=block_size)
            points = cv2.goodFeaturesToTrack(self.img_ref, mask=None, **feature_params)[:, 0]
        else:
            # this is for deepflow and Lucas-Kanade method
            if 'deep_flow' in self.kwargs:
                points_x = np.float64(np.arange(area[0][0], area[1][0], 1))
                points_y = np.float64(np.arange(area[0][1], area[1][1], 1))
            else:
                points_x = np.float64(np.arange(
                    start= area[0][0], 
                    stop= area[1][0], 
                    step = self.grid_size_px[0]))
                points_y = np.float64(np.arange(
                    start=area[0][1], 
                    stop=area[1][1], 
                    step=self.grid_size_px[1]))
            for x in points_x:
                for y in points_y:
                    points.append(np.array([np.float32(x), np.float32(y)]))
            points = np.array(points)
            self.points_x = points_x
            self.points_y = points_y
        self.points_ref = points.copy()
        
        return self.points_ref

    def display_markers(self, points_in):
        """
        Display the markers on the reference image.

        Args:
            points (array): Array of points of interest in the image sequence.
        """
        img_ref = self.img_ref.copy()
        img_ref = cv2.putText(img_ref, "Displaying markers... Press any buttons to continue", 
                              (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4)
        draw_opencv_v2(img_ref, point=points_in)

    def process_image(self, new_img:np.ndarray):
        """
        workhorse of the code

        Compute the grid and save it in the result file.
        """

        # replacing image with last image
        self._last_img = self._curr_img.copy()
        self._curr_img = new_img.copy()

        # param for correlation 
        lk_params = dict( winSize  = self.win_size_px, maxLevel = 10,
                          criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        point_to_process = self.points_in

        # image_ref = cv2.imread(self.img_list[i], flag =cv2.IMREAD_GRAYSCALE)
        last_image = self._last_img.copy()
        # image_str = cv2.imread(self.img_list[i+1], flag = cv2.IMREAD_GRAYSCALE)
        curr_image = self._curr_img.copy()

        if 'deep_flow' in self.kwargs:
            winsize_x = self.win_size_px[0]
            final_point = cv2.calcOpticalFlowFarneback(last_image, curr_image, 
                                                       None, 0.5, 3, 
                                                       winsize_x,
                                                        10, 5, 1.2, 0)
            index = 0
            ii_max = final_point.shape[0]
            jj_max = final_point.shape[1]

            for jj in range(jj_max):
                for ii in range(ii_max):
                    if (jj >= self.area[0][0] and jj < self.area[1][0] and
                        ii >= self.area[0][1] and ii < self.area[1][1]):
                        point_to_process[index] += final_point[ii,jj]
                        index += 1

        else:
            #  Lucas-Kanade method
            final_point, st, err = cv2.calcOpticalFlowPyrLK(last_image, curr_image, point_to_process, None, **lk_params)
            point_to_process = final_point
        # self.write_result( self.img_list[i+1], point_to_process)
        self.points_in = point_to_process.copy()
        # return
        return {"img":curr_image,"prev_img":last_image, "point_to_process":point_to_process.copy()}

    def dic_parameters(self):
        """returns the configuration parameters

        Returns:
            _type_: _description_
        """        
        xmin = self.points_x[0]
        xmax = self.points_x[-1]
        xnum = len(self.points_x)
        ymin = self.points_y[0]
        ymax = self.points_y[-1] 
        ynum = len(self.points_y)
        dic = {"xmin":xmin, "xmax":xmax,"xnum": int(xnum), "x_win_size_px":int(self.win_size_px[0]),
                "ymin":ymin, "ymax":ymax,"ynum": int(ynum), "y_win_size_px":int(self.win_size_px[1])}
        # self.result_file.write(str(xmin) + '\t' + str(xmax) + '\t' + str(int(xnum)) + '\t' + str(int(self.win_size_px[0])) + '\n')
        # self.result_file.write(str(ymin) + '\t' + str(ymax) + '\t' + str(int(ynum)) + '\t' + str(int(self.win_size_px[1])) + '\n')
        return dic

    def get_dic_gridsize(self)->GridSize:
        """returns the configuration parameters

        Returns:
            _type_: _description_
        """        
        xmin = self.points_x[0]
        xmax = self.points_x[-1]
        xnum = len(self.points_x)
        ymin = self.points_y[0]
        ymax = self.points_y[-1] 
        ynum = len(self.points_y)
        gridsize_obj = GridSize(
            xmin=xmin, xmax=xmax, xnum=int(xnum), win_size_x=int(self.win_size_px[0]),
            ymin=ymin, ymax=ymax, ynum=int(ynum), win_size_y=int(self.win_size_px[1]))
        return gridsize_obj

    def write_result(self, image, points):
        """
        Used by the class to write the data for a file.

        Args:
            image (str): The name of the image file.
            points (list of tuples()): List of point coordinates.
        """
        self.result_file.write(image + '\t')
        for p in points:
            self.result_file.write(str(p[0]) + ',' + str(p[1]) + '\t')
        self.result_file.write('\n')

    @property
    def last_image_array(self):
        return self._last_img
    
    @property
    def curr_image_array(self):
        return self._curr_img
    
    @property
    def ref_image_array(self):
        return self.img_ref
    
    @property
    def current_point_position(self):
        return self.points_in

#%% 
class DICProcessorRolling:
    # grid_list:list[DIC_Grid] = [] # saving grid here
    # STRAINS_TIME_XLSX_FILE:str = "df_strain_wt.xlsx"
    _counter = 0   # number of images processed
    disp_list = [] # array with the calculated displacements

    def __init__(self,
            sidp:SingleImageDisplacementProcessor,
            interpolation:str=EnumInteropolation.RAW.value, 
            strain_type:str=EnumStrainType.CAUCHY.value, 
            scale_disp:float=1., scale_grid:float=1., 
            rm_rigid_body_transform:bool=True,
            save_image:bool=False
            ,*args, **kwargs
            ):
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
        self.sidp = sidp
        self._dic_grid_size = self.sidp.get_dic_gridsize()
        
        self.interpolation = interpolation
        self.strain_type = strain_type
        
        self.save_image = save_image
        self.scale_disp = scale_disp
        self.scale_grid = scale_grid
        self.rm_rigid_body_transform = rm_rigid_body_transform

        self._prepare_grid()

        self.meta_info = {}

    def _prepare_grid(self):
        xmin = self._dic_grid_size.xmin
        xmax = self._dic_grid_size.xmax
        xnum = self._dic_grid_size.xnum
        self.win_size = self._dic_grid_size.winsize()

        self.__grid_x, self.__grid_y = self._dic_grid_size.prepare_gridXY()
        # The new grid is used fo
        self.__newgrid = DIC_Grid(self.__grid_x, self.__grid_y, int(self._dic_grid_size.xnum), int(self._dic_grid_size.ynum))

    def create_new_grid(self):
        return copy.deepcopy(self.__newgrid)
    
    @property
    def ref_points(self):
        return self.sidp.points_ref

    def process_new_image(self, new_image:np.ndarray) -> DIC_Grid:
        """_summary_

        Args:
        """        
        mygrid:DIC_Grid = self.create_new_grid()
        
        res = self.sidp.process_image(new_img=new_image)
        self._counter +=1

        logging.info(f"compute displacement and strain field of img no: {self._counter} ...")
        disp = None
        self.point_list0 = self.sidp.points_ref
        self.point_listi = self.sidp.current_point_position
        # TODO chekc shape of points_ref and self.point_list[0]
        if self.rm_rigid_body_transform:
            logging.info("   - remove rigid body transform")
            disp = compute_disp_and_remove_rigid_transform(self.point_listi, self.point_list0)
        else:
            logging.info("   - rigid body transform is not removed")
            disp = compute_displacement(self.point_listi, self.point_list0)
        mygrid.add_raw_data(winsize=self.win_size, 
                reference_image="ref image", 
                image=str("i"), 
                reference_point=self.point_list0, 
                correlated_point=self.point_listi, 
                disp=disp)
        
        self.disp_list.append(disp)
        mygrid.interpolate_displacement(self.point_list0, disp, method=self.interpolation)

        if (self.strain_type == EnumStrainType.CAUCHY.value):
            mygrid.compute_strain_field()
        elif (self.strain_type == EnumStrainType.SECOND_ORDER.value):
            mygrid.compute_strain_field_DA()
        elif (self.strain_type == EnumStrainType.LOG.value):
            mygrid.compute_strain_field_log()
        else:
            raise ValueError("please specify a correct strain_type : 'cauchy', '2nd_order' or 'log'")

        # # write image files
        # TODO write to file, or delegate that to another class
        # if (self.save_image):
        #     self.write_image_files(mygrid)

        # # add meta info to grid if it exists
        # self.add_metadata_to_grid_object(mygrid)
        return mygrid


    def add_metadata_to_grid_object(self, mygrid):
        """Adds metadata to grid object.

        TODO I need to understand how this works in the original code
        or in DICProcessorBatch

        This could eventually add time and force info in the grid

        Args:
            mygrid (_type_): _description_
        """ 
        pass        
        # if (len(self.meta_info) > 0):
        #     img = os.path.basename(mygrid.image)
        #         #if not meta_info.has_key(img):
        #     if img not in self.meta_info.keys():
        #         print("warning, can't affect meta data for image", img)
        #     else:
        #         mygrid.add_meta_info(self.meta_info.get(img))
        #         print('add meta info', self.meta_info.get(img))


