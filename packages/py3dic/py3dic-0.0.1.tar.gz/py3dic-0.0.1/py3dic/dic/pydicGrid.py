import math
import pathlib
import copy

import cv2
import numpy as np
import scipy.interpolate

from matplotlib import pyplot as plt
from matplotlib.widgets import Button, RadioButtons, Slider
from scipy.interpolate import Rbf, griddata
from .dic2d_contour_plot import DIC2DContourInteractivePlot

__ADD_IMAGE_NAME__ = False

def draw_opencv_v2(
    image, # TODO argumenttakes either an image or a filename. This should be broken up
    text: str = None, 
    point=None, # used in marker plotting
    pointf=None, 
    grid: 'DIC_Grid' = None,
    scale: float = 1, 
    p_color: tuple = (0, 255, 255), 
    l_color: tuple = (255, 120, 255), 
    gr_color: tuple = (255, 255, 255), 
    filename=None,
    *args, **kwargs):
    """A generic function used to draw opencv image. Depending on the arguments it plots 

    - markers
    - grid
    - lines
    - displacement

    Args:
        image (str|np.ndarray): _description_
        text (str, optional): _description_. Defaults to None.
        point (_type_, optional): arg must be an array of (x,y) point. Defaults to None.
        pointf (_type_, optional): to draw lines between point and pointf, pointf  (must be an array of same lenght than the point array). Defaults to None.
        scale (int, optional): scaling parameter. Defaults to 1.
        p_color (tuple, optional): arg to choose the color of point in (r,g,b) format. Defaults to (0, 255, 255).
        l_color (tuple, optional): color of lines in (RGB). Defaults to (255, 120, 255).
        gr_color (tuple, optional): color of grid in (RGB). Defaults to (255, 255, 255).
        filename (_type_, optional): _description_. Defaults to None.
    """ 
    if isinstance(image, str):
        image = cv2.imread(image, 0)

    if text is not None and __ADD_IMAGE_NAME__:
        # text = pathlib.Path(text).name # consider this alternatively needs testing.
        image = cv2.putText(image, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4)

    frame = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    if point is not None:
        for pt in point:
            if not np.isnan(pt[0]) and not np.isnan(pt[1]):
                x, y = int(pt[0]), int(pt[1])
                frame = cv2.circle(frame, (x, y), 4, p_color, -1)

    if pointf is not None and point is not None:
        assert len(point) == len(pointf), 'size between initial  point and final point does not match.'
        for pt0, pt1 in zip(point, pointf):
            if not np.isnan(pt0[0]) and not np.isnan(pt0[1]) and not np.isnan(pt1[0]) and not np.isnan(pt1[1]):
                disp_x, disp_y = (pt1[0] - pt0[0]) * scale, (pt1[1] - pt0[1]) * scale
                frame = cv2.line(frame, (int(pt0[0]), int(pt0[1])), (int(pt0[0] + disp_x), int(pt0[1] + disp_y)), l_color, 2)

    if grid is not None:
        # this requires a grid object. 
        dic_grid = grid
        assert isinstance(dic_grid, DIC_Grid), "grid should be DIC_Grid"
        for i in range(dic_grid.size_x):
            for j in range(dic_grid.size_y):
                if dic_grid.is_valid_number(i, j):
                    x = int(dic_grid.grid_x[i, j]) - int(dic_grid.disp_x[i, j] * scale)
                    y = int(dic_grid.grid_y[i, j]) - int(dic_grid.disp_y[i, j] * scale)

                    if i < (dic_grid.size_x - 1) and dic_grid.is_valid_number(i + 1, j):
                        x1 = int(dic_grid.grid_x[i + 1, j]) - int(dic_grid.disp_x[i + 1, j] * scale)
                        y1 = int(dic_grid.grid_y[i + 1, j]) - int(dic_grid.disp_y[i + 1, j] * scale)
                        frame = cv2.line(frame, (x, y), (x1, y1), gr_color, 2)

                    if j < (dic_grid.size_y - 1) and dic_grid.is_valid_number(i, j + 1):
                        x1 = int(dic_grid.grid_x[i, j + 1]) - int(dic_grid.disp_x[i, j + 1] * scale)
                        y1 = int(dic_grid.grid_y[i, j + 1]) - int(dic_grid.disp_y[i, j + 1] * scale)
                        frame = cv2.line(frame, (x, y), (x1, y1), gr_color, 4)

    if filename is not None:
        cv2.imwrite(filename, frame)
        return

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', frame.shape[1], frame.shape[0])
    cv2.imshow('image', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

  
class DIC_Grid:
    """The DIC_Grid class is the main class of pydic. This class embed a lot of usefull
    method to treat and post-treat results
    """
    def __init__(self, grid_x:np.ndarray, grid_y:np.ndarray,
                size_x:int, size_y:int):
        """Construct a new DIC_Grid object with 

        Args:
            grid_x (np.ndarray): x coordinate (grid_x) for each marker
            grid_y (np.ndarray): y coordinate (grid_x) for each marker
            size_x (int): number of point along x (size_x)
            size_y (int): number of point along y (size_y)
        """
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.size_x = size_x
        self.size_y = size_y
        self.disp_x =  self.grid_x.copy().fill(0.)
        self.disp_y =  self.grid_y.copy().fill(0.)
        self.strain_xx = None
        self.strain_yy = None
        self.strain_xy = None

    def add_raw_data(self,
            winsize:tuple,
            reference_image:str,
            image:str,
            reference_point:np.ndarray,
            correlated_point:np.ndarray,
            disp:list[tuple]):
        """Save raw data to the current object. 
        
        These raw data are used as initial data 
        for digital image correlation

        Args:
            winsize (tuple): the size in pixel of the correlation windows
            reference_image (str): filename of the reference image
            image (str): filename of the current image
            reference_point (np.ndarray[(size_x*size_y),2]): Reference coordinates for each marker 
            correlated_point (np.ndarray[(size_x*size_y),2]): Current coordinate for each marker
            disp (list of tuples): List of tuples with dispacement for each marker (first column, then second column ....)
        """
        self.winsize = winsize
        self.reference_image = reference_image
        self.image = image
        self.reference_point = reference_point
        self.correlated_point = correlated_point
        self.disp = disp

    def add_meta_info(self, meta_info):
        """Save the related meta info into the current DIC_Grid object"""
        self.meta_info = meta_info

    def is_valid_number(self, i:int, j:int):
        """check if grid_x, grid_y, disp_x, and disp_y at i,j are nan

        Args:
            i (int): index in x direction
            j (int): index in y direction

        Returns:
            _type_: _description_
        """
        return  (not math.isnan(self.grid_x[i,j]) and
            not math.isnan(self.grid_y[i,j]) and
            not math.isnan(self.disp_x[i,j]) and
            not math.isnan(self.disp_y[i,j]))       

    def prepare_saved_file(self, prefix, extension, analysis_folder=None):
        """prepares the filename in the form:

        <analysis_folder or image_folder>/pydic/<prefix>/<image_name>_<prefix>.<extension>

        Args:
            prefix (str): folder that the file will be saved in the pydic folder structure
            extension (str): File extension
            analysis_folder (str): the main folder where the image will be saved

        Returns:
            str: the prepared file path
        """

        if analysis_folder:
            folder = pathlib.Path(analysis_folder)
            if not folder.is_dir():
                raise ValueError(f"{analysis_folder} is not a valid directory.")
            folder = folder / prefix
        else:
            # if analyis folder is None
            folder = pathlib.Path(self.image).parent / 'pydic' / prefix

        folder.mkdir(parents=True, exist_ok=True)
        base = pathlib.Path(self.image).stem
        name = folder / f"{base}_{prefix}.{extension}"
        print("saving", name, "file...")
        return str(name)

    def draw_marker_img(self,analysis_folder=None):
        """Draw marker image"""
        name = self.prepare_saved_file(prefix ='marker',
            extension='png', analysis_folder=analysis_folder)
        draw_opencv_v2(self.image, point=self.correlated_point,
                l_color=(0,0,255), p_color=(255,255,0),
                filename=name, text=name)

    def draw_disp_img(self, scale,analysis_folder=None):
        """Draw displacement image. 
        A scale value can be passed to amplify the displacement field
        """
        name = self.prepare_saved_file('disp', 'png',analysis_folder=analysis_folder)
        draw_opencv_v2(self.reference_image,
                    point=self.reference_point,
                    pointf=self.correlated_point,
                    l_color=(0,0,255), p_color=(255,255,0),
                    scale=scale,
                    filename=name, text=name)

    def draw_disp_hsv_img(self,analysis_folder=None, *args, **kwargs):
        """Draw displacement image in a hsv view."""
        name = self.prepare_saved_file('disp_hsv', 'png',analysis_folder=analysis_folder)
        img = self.reference_image
        if isinstance(img, str):
            img = cv2.imread(img, 0)

        disp = self.correlated_point - self.reference_point
        fx, fy = disp[:,0], disp[:,1]
        v_all = np.sqrt(fx*fx + fy*fy)
        v_max = np.mean(v_all) + 2.*np.std(v_all)

        rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)

        if v_max != 0.:
            for i, val in enumerate(self.reference_point):
                disp = self.correlated_point[i] - val
                ang = np.arctan2(disp[1], disp[0]) + np.pi
                v = np.sqrt(disp[0]**2 + disp[1]**2)
                pt_x = int(val[0])
                pt_y = int(val[1])

                hsv[pt_y,pt_x, 0] = int(ang*(180/np.pi/2))
                hsv[pt_y,pt_x, 1] = 255 if int((v/v_max)*255.) > 255 else int((v/v_max)*255.)
                hsv[pt_y,pt_x, 2] = 255 if int((v/v_max)*255.) > 255 else int((v/v_max)*255.)

        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        bgr = cv2.putText(bgr, name, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),4)

        if 'save_img' in kwargs:
            cv2.imwrite(name, bgr)
        if 'show_img' in kwargs:
            cv2.namedWindow('image', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('image', bgr.shape[1], bgr.shape[0])
            cv2.imshow('image', bgr)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


    def draw_grid_img(self, scale, analysis_folder=None):
        """Draw grid image. 
        
        A scale value can be passed to amplify the displacement field
        """
        name = self.prepare_saved_file('grid', 'png', analysis_folder=analysis_folder)
        draw_opencv_v2(self.reference_image,
                    grid = self,
                    scale=scale, gr_color=(255,255,250),
                    filename=name, text=name)

    def write_result(self,analysis_folder=None):
        """write a raw csv result file. 

        Indeed, you can use your favorite tool to post-treat this file
        """
        name = self.prepare_saved_file('result', 'csv',analysis_folder=analysis_folder)
        with open(name, 'w', encoding='utf-8') as f:
            f.write("index" + ',' + "index_x" + ',' + "index_y" + ',' +
                    "pos_x"     + ',' + "pos_y"     + ',' +
                    "disp_x"    + ',' + "disp_y"    + ',' + 
                    "strain_xx" + ',' + "strain_yy" + ',' + "strain_xy" + '\n')
            index = 0
            for i in range(self.size_x):
                for j in range(self.size_y):
                    f.write(str(index)   + ',' +
                        str(i)                   + ',' + str(j)                   + ',' +
                        str(self.grid_x[i,j])    + ',' + str(self.grid_y[i,j])    + ',' +
                        str(self.disp_x[i,j])    + ',' + str(self.disp_y[i,j])    + ',' +
                        str(self.strain_xx[i,j]) + ',' + str(self.strain_yy[i,j]) + ',' +
                        str(self.strain_xy[i,j]) + '\n')
                    index = index + 1
            f.close()

    def plot_field(self, field, title):
        """Plot the chosen field such as strain_xx, disp_xx, etc. 
        in a matplotlib interactive map
        # TODO Rename to Plot interactive
        """
        image_ref = cv2.imread(self.image, 0)
        DIC2DContourInteractivePlot(image_ref, self, field, title)

    def interpolate_displacement(self, point:np.ndarray, disp:np.ndarray,
        # *args,
        **kwargs):
        """Interpolate the displacement field.
        
        It allows to:
        (i) construct the displacement grid and to 
        (ii) smooth the displacement field thanks to the chosen method (raw, linear, spline,etc.)

        Args:
            point (np.ndarray): Original position (rows x 2 columns)
            disp (np.ndarray): New position (rows x 2 columns)
            TODO method(str): Interpolation method
        """
        x = np.array([p[0] for p in point])
        y = np.array([p[1] for p in point])
        dx = np.array([d[0] for d in disp])
        dy = np.array([d[1] for d in disp])
        method = kwargs.get('method','linear')

        print(f'interpolate displacement with {method} method.')
        #TODO enumerate interpolation method
        if method=='delaunay':
            inter_x = scipy.interpolate.LinearNDInterpolator(point, dx)
            inter_y = scipy.interpolate.LinearNDInterpolator(point, dy)
            self.disp_x = inter_x(self.grid_x, self.grid_y)
            self.disp_y = inter_y(self.grid_x, self.grid_y)

        elif method=='raw':
            # need debugging
            self.disp_x = self.grid_x.copy()
            self.disp_y = self.grid_y.copy()

            assert self.disp_x.shape[0] == self.disp_y.shape[0], "bad shape"
            assert self.disp_x.shape[1] == self.disp_y.shape[1], "bad shape"
            assert len(dx) == len(dy), "bad shape"
            assert self.disp_x.shape[1]*self.disp_x.shape[0] == len(dx), "bad shape"
            count = 0
            for i in range(self.disp_x.shape[0]):
                for j in range(self.disp_x.shape[1]):
                    self.disp_x[i,j] = dx[count]
                    self.disp_y[i,j] = dy[count]
                    count = count + 1

        elif method=='spline':
            # x displacement
            tck_x = scipy.interpolate.bisplrep(self.grid_x, self.grid_y, dx, kx=5, ky=5)
            self.disp_x = scipy.interpolate.bisplev(self.grid_x[:,0], self.grid_y[0,:],tck_x)
    	    # y displacement
            tck_y = scipy.interpolate.bisplrep(self.grid_x, self.grid_y, dy, kx=5, ky=5)
            self.disp_y = scipy.interpolate.bisplev(self.grid_x[:,0], self.grid_y[0,:],tck_y)
        else:
            self.disp_x = griddata((x, y), dx, (self.grid_x, self.grid_y), method=method)
            self.disp_y = griddata((x, y), dy, (self.grid_x, self.grid_y), method=method)



    def compute_strain_field(self):
        """Compute strain field from displacement using numpy
        """
        #get strain fields
        dx = self.grid_x[1][0] - self.grid_x[0][0]
        dy = self.grid_y[0][1] - self.grid_y[0][0]

        
        strain_xx, strain_xy = np.gradient(self.disp_x, dx, dy, edge_order=2)
        strain_yx, strain_yy = np.gradient(self.disp_y, dx, dy, edge_order=2)

        self.strain_xx = strain_xx + .5*(np.power(strain_xx,2) + np.power(strain_yy,2))
        self.strain_yy = strain_yy + .5*(np.power(strain_xx,2) + np.power(strain_yy,2))
        self.strain_xy = .5*(strain_xy + strain_yx + strain_xx*strain_xy + strain_yx*strain_yy)

    def compute_strain_field_DA(self):
        """Compute strain field from displacement field using a  large strain method 

        TODO: refactor this piece of code
        """
        smap_shape = self.disp_x.shape
        self.strain_xx = np.full(smap_shape, np.NaN)
        self.strain_xy = np.full(smap_shape, np.NaN)
        self.strain_yy = np.full(smap_shape, np.NaN)
        self.strain_yx = np.full(smap_shape, np.NaN)

        dx = self.grid_x[1][0] - self.grid_x[0][0]
        dy = self.grid_y[0][1] - self.grid_y[0][0]

        for i in range(self.size_x):
            for j in range(self.size_y):
                du_dx = 0.
                dv_dy = 0. 
                du_dy = 0.
                dv_dx = 0.

                if i-1 >=0 and i+1< self.size_x:
                    du1 = (self.disp_x[i+1,j] - self.disp_x[i-1,j])/2.
                    du_dx = du1/dx
                    dv2 = (self.disp_y[i+1,j] - self.disp_y[i-1,j])/2.
                    dv_dx = dv2/dx

                if j-1>=0 and j+1 < self.size_y:
                    dv1 = (self.disp_y[i,j+1] - self.disp_y[i,j-1])/2.
                    dv_dy = dv1/dx
                    du2 = (self.disp_x[i,j+1] - self.disp_x[i,j-1])/2.
                    du_dy = du2/dy

                self.strain_xx[i,j] = du_dx + .5*(du_dx**2 + dv_dx**2)
                self.strain_yy[i,j] = dv_dy + .5*(du_dy**2 + dv_dy**2)
                self.strain_xy[i,j] = .5*(du_dy + dv_dx + du_dx*du_dy + dv_dx*dv_dy)

    def compute_strain_field_log(self):
        """Compute strain field from displacement field for large strain (logarithmic strain)
        """
        smap_shape = self.disp_x.shape
        self.strain_xx = np.full(smap_shape, np.NaN)
        self.strain_xy = np.full(smap_shape, np.NaN)
        self.strain_yy = np.full(smap_shape, np.NaN)
        self.strain_yx = np.full(smap_shape, np.NaN)

        dx = self.grid_x[1][0] - self.grid_x[0][0]
        dy = self.grid_y[0][1] - self.grid_y[0][0]
        for i in range(self.size_x):
            for j in range(self.size_y):
                du_dx = 0.
                dv_dy = 0. 
                du_dy = 0.
                dv_dx = 0.


                if i-1 >= 0 and i+1 < self.size_x:
                    du1 = (self.disp_x[i+1,j] - self.disp_x[i-1,j])/2.
                    du_dx = du1/dx
                    dv2 = (self.disp_y[i+1,j] - self.disp_y[i-1,j])/2.
                    dv_dx = dv2/dx
                      
                if j-1 >= 0 and j+1 < self.size_y:
                    dv1 = (self.disp_y[i,j+1] - self.disp_y[i,j-1])/2.
                    dv_dy = dv1/dx
                    du2 = (self.disp_x[i,j+1] - self.disp_x[i,j-1])/2.
                    du_dy = du2/dy
                t11=1+2.*du_dx+du_dx**2+dv_dx**2
                t22=1+2.*dv_dy+dv_dy**2+du_dy**2
                t12=du_dy+dv_dx+du_dx*du_dy+dv_dx*dv_dy
                deflog=np.log([[t11,t12],[t12,t22]])

                self.strain_xx[i,j] = .5*deflog[0,0]
                self.strain_yy[i,j] = .5*deflog[1,1]
                self.strain_xy[i,j] = .5*deflog[0,1]

    def average(self, value, x_range, y_range):
        """Get the average value in the specified 
        x,y range of the given field

        TODO: check if its used
        """
        val = []
        for x in x_range:
            for y in y_range:
                if not np.isnan(value[x,y]):
                    val.append(value[x,y])
        return np.average(val)

    def std(self, value, x_range, y_range):
        """Get the standard deviation value in the specified x,y range of the given field

        TODO: check if its used
        """
        val = []
        for x in x_range:
            for y in y_range:
                if not np.isnan(value[x,y]):
                    val.append(value[x,y])
        return np.std(val)
    
    def obtain_strains(self, func=None)->dict:
        """this is a function that calculates the strains xx, yy, xy  on this grid. 

        Returns:
            dict: dataframe that contains (e_xx, e_xx_std, e_yy, e_yy_std, e_xy, e_xy_std) for this grid
        """

        def portion_function(fraction:float = 0):
            """factory function that generates a function that takes a portion of the elemetns of an array 

            Args:
                fraction (float, optional): _description_. Defaults to 0.
            """
            assert fraction<=0.5 and fraction>=0, 'Fraction should be between 0 and 0.5 (0 select all, 0.5 only most central points)'
            def inner(array:np.ndarray):
                xmax, ymax = array.shape
                x_start, x_end = np.floor(fraction*xmax).astype('int'), np.ceil((1-fraction)*xmax).astype('int')
                y_start, y_end = np.floor(fraction*ymax).astype('int'), np.ceil((1-fraction)*ymax).astype('int')
                # print([x_start,x_end, y_start, y_end])
                portion = array[x_start:x_end, y_start:y_end]
                return portion
            return inner

        func = portion_function(fraction=0) if func is None else func
        assert callable(func), "func needs to be callable or a function"

        portion_xx = func(self.strain_xx) 
        portion_yy = func(self.strain_yy)
        portion_xy = func(self.strain_xy)
        adic = {"e_xx":portion_xx.mean(), "e_xx_std": portion_xx.std(),
                "e_yy":portion_yy.mean(), "e_yy_std": portion_yy.std(),
                "e_xy":portion_xy.mean(), "e_xy_std": portion_xy.std()}

        return adic     




class GridSize():
    """The GridSize class is used to define the grid size for DIC analysis.
    """
    xmin:int = None
    xmax:int = None
    xnum:int = None
    win_size_x:int= None
    ymin:int= None
    ymax:int= None
    ynum:int= None
    win_size_y:int= None

    def __init__(self, xmin:int = None
                 ,xmax:int = None
                 ,xnum:int = None 
                 , win_size_x:int= None
                 , ymin:int= None
                , ymax:int= None
                ,ynum:int= None
                ,win_size_y:int= None):
        self.xmin = xmin
        self.xmax = xmax
        self.xnum = xnum
        self.win_size_x = win_size_x

        self.ymin = ymin
        self.ymax = ymax
        self.ynum = ynum
        self.win_size_y = win_size_y

        # calculate the grid size
        # TODO: check if the grid size is integer
        self.x_grid_size = int((self.xmax - self.xmin)/(self.xnum - 1))
        self.y_grid_size = int((self.ymax - self.ymin)/(self.ynum - 1))

    def winsize(self) ->tuple[int]:
        """
        Returns the size of the DIC window as a tuple (win_size_x, win_size_y).

        higher number means
         - wider area to check for tracking
         - greater confidence in the tracking
         - slower tracking (more computaional effort)
        """
        return (self.win_size_x, self.win_size_y)

    def prepare_gridXY(self) -> tuple[np.ndarray]:
        """
        Prepare the grid for X and Y coordinates.

        Returns:
            A tuple containing the grid arrays for X and Y coordinates.
        """
        self.grid_x, self.grid_y = np.mgrid[self.xmin:self.xmax:int(self.xnum)*1j, self.ymin:self.ymax:int(self.ynum)*1j]
        return (self.grid_x.copy(), self.grid_y.copy())

    def create_DIC_Grid(self) -> 'DIC_Grid':
        """
        Creates a DIC_Grid object based on the current grid parameters.

        Returns:
            DIC_Grid: A new DIC_Grid object.
        """
        # xmin = self.xmin
        # xmax = self.xmax
        # xnum = self.xnum
        self.win_size = self.winsize()

        self.prepare_gridXY()
        # The new grid is used fo
        self.__newgrid = DIC_Grid(
            grid_x=self.grid_x, grid_y=self.grid_y,
            size_x=int(self.xnum), size_y=int(self.ynum))
        return copy.deepcopy(self.__newgrid)

    @classmethod
    def from_tuplesXY(cls, xtuple, ytuple):
        """Create a new instance of the class using two tuples for x and y coordinates.

        Args:
            cls: The class itself.
            xtuple: Tuple containing x coordinates.
            ytuple: Tuple containing y coordinates.

        Returns:
            An instance of the class with x and y coordinates initialized from the given tuples.
        """
        return cls(*xtuple, *ytuple)

    @classmethod
    def from_result_dic(cls, fname):
        """Create a GridSize object from a result DIC file.

        This is useful when reading a completed analysis
        
        Parameters:
        - fname (str): The path to the result.dic DIC file.

        Returns:
        - GridSize: The GridSize object created from the result DIC file.
        """
        with open(fname, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Parse grid dimensions and window sizes
            (xmin, xmax, xnum, x_window_size) = [int(float(x)) for x in lines[0].split()]
            (ymin, ymax, ynum, y_window_size) = [int(float(x)) for x in lines[1].split()]
        return cls(xmin=xmin, xmax=xmax,
                   xnum=xnum, win_size_x=x_window_size,
                   ymin=ymin, ymax=ymax,
                   ynum=ynum, win_size_y=y_window_size)
