import numpy as np
import cv2
import matplotlib.pyplot as plt

from py3dic.dic import DIC_Grid

class DIC_Grid_plots:
    """This class is an attempt to replace the draw_opencv_v2 function in pydicGrid.
    
    NOTE: It is not yet complete  #TODO
    
    Each grid needs to plot:
    - grid (to current image)
    - markers (to current image)
    - displacement (to ref image)
    - strain map (to ref / current image)

    The idea for this class is to have a factory of plots and the following steps are performed:
    - create a plotter object
    - once the plotter object is created
        - set the grid
        - set the image (ref or current)
        - plot the desired plot
    - rinse and repeat
    """
    _grid:DIC_Grid = None

    gr_color:tuple=(1.,1.,1.) # grid color
    t_color=(1.,1.,1.) # Text color
    p_color=(1.,1.,0.) # marker color
    l_color=(255, 120, 255)

    def __init__(self):
        self._grid = None

    def set_grid(self, grid: DIC_Grid):
        """Set the DIC grid for the DIC_GridPlots object.

        Args:
            grid (DIC_Grid): The DIC grid to be set.

        Raises:
            ValueError: If the provided grid is not an instance of DIC_Grid.
        """
        assert isinstance(grid, DIC_Grid), ValueError('grid is not DIC_Grid')
        self._grid = grid

    
    def set_ref_image(self, ref_image: np.ndarray):
        """ Set the reference image for the DIC grid plots.

        Parameters:
            ref_image (np.ndarray): The reference image to be set.

        Returns:
            None
        """
        self.ref_image = ref_image

    def plot_markers(self,image_cv2:np.ndarray,
                p_color:tuple[float]=(1,1,0),
                text:str = None, t_color=(1,1,1)):
        """plots markers on the image
        # TODO THere seems to be a problem when the displacement is large( towards the end of the experiment)

        Args:
            image_cv2 (np.ndarray): array with image GRAYSCALE data (in opencv format?)
            p_color (tuple[float], optional): marker color. Defaults to (1,1,0).
            text(str, optional) , annotation text. 
            t_color(tuple[float], optional): Text color. Defaults to (1,1,1)):
        """        
        frame_rgb = cv2.cvtColor(image_cv2, cv2.COLOR_GRAY2RGB)

        fig, ax = plt.subplots()
        ax.imshow(frame_rgb, aspect='equal')
        points_xy = self._grid.correlated_point
        if points_xy is not None:
            for pt_xy in points_xy:
                # print(pt_xy)
                if not np.isnan(pt_xy[0]) and not np.isnan(pt_xy[1]):
                    x, y = int(pt_xy[0]), int(pt_xy[1])
                    circ = plt.Circle((x, y), 4, color=p_color)
                    ax.add_patch(circ)

        if text is not None:
            ax.text(50, 50, text, fontsize=12, color=t_color)

    def plot_grid(self,
                  image: np.ndarray, 
                  text: str = None,
                  scale: float = 1,
                  gr_color: tuple = (1, 1, 1),
                  filename: str = None,
                  *args, **kwargs):
        """Plot the grid on top of the input image.

        Args:
            image (np.ndarray): The input image.
            text (str, optional): Additional text to be displayed on the plot. Defaults to None.
            scale (float, optional): Scaling factor for the grid. Defaults to 1.
            gr_color (tuple, optional): Color of the grid lines. Defaults to (1, 1, 1).
            filename (str, optional): File path to save the plot. Defaults to None.
            *args, **kwargs: Additional arguments to be passed to the plot function.

        Returns:
            None
        """
        frame_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        
        fig, ax = plt.subplots(nrows=1, ncols=1)
        
        ax.imshow(image, cmap='gray', aspect='equal')

        if self._grid is not None:
            dic_grid = self._grid
            for i in range(dic_grid.size_x):
                for j in range(dic_grid.size_y):
                    if dic_grid.is_valid_number(i, j):
                        x = int(dic_grid.grid_x[i, j]) - int(dic_grid.disp_x[i, j] * scale)
                        y = int(dic_grid.grid_y[i, j]) - int(dic_grid.disp_y[i, j] * scale)

                        if i < (dic_grid.size_x - 1) and dic_grid.is_valid_number(i + 1, j):
                            x1 = int(dic_grid.grid_x[i + 1, j]) - int(dic_grid.disp_x[i + 1, j] * scale)
                            y1 = int(dic_grid.grid_y[i + 1, j]) - int(dic_grid.disp_y[i + 1, j] * scale)
                            ax.plot([x, x1], [y, y1], color=gr_color, linewidth=2)

                        if j < (dic_grid.size_y - 1) and dic_grid.is_valid_number(i, j + 1):
                            x1 = int(dic_grid.grid_x[i, j + 1]) - int(dic_grid.disp_x[i, j + 1] * scale)
                            y1 = int(dic_grid.grid_y[i, j + 1]) - int(dic_grid.disp_y[i, j + 1] * scale)
                            ax.plot([x, x1], [y, y1], color=gr_color, linewidth=2)

        if text is not None:
            ax.text(50, 50, text, fontsize=12, color=(1, 1, 1))

        if filename is not None:
            plt.savefig(filename)
        else:
            pass
            # plt.show()


    # def plot_disp(image, # TODO argumenttakes either an image or a filename. This should be broken up
    #     text: str = None, 
    #     # point=None, 
    #     # pointf=None, 
    #     scale: float = 1, 
    #     p_color: tuple = (0, 1, 1), 
    #     l_color: tuple = (1, 120/255,1 ), 
    #     filename=None,
    #     *args, **kwargs):
    #     """A generic function used to draw matplotlib image. Depending on the arguments it plots 

    #     - markers
    #     - grid
    #     - lines
    #     - displacement

    #     Args:
    #         image (str|np.ndarray): _description_
    #         grid (DIC_Grid): DIC_grid object
    #         text (str, optional): _description_. Defaults to None.
    #         # point (_type_, optional): arg must be an array of (x,y) point. Defaults to None.
    #         # pointf (_type_, optional): to draw lines between point and pointf, pointf  (must be an array of same lenght than the point array). Defaults to None.
    #         scale (int, optional): scaling parameter. Defaults to 1.
    #         p_color (tuple, optional): arg to choose the color of point in (r,g,b) format. Defaults to (0, 255, 255).
    #         l_color (tuple, optional): color of lines in (RGB). Defaults to (255, 120, 255).
    #         gr_color (tuple, optional): color of grid in (RGB). Defaults to (255, 255, 255).
    #         filename (_type_, optional): _description_. Defaults to None.
    #     """ 
    #     if isinstance(image, str):
    #         image = plt.imread(image, 0)

    #     fig, ax = plt.subplots()
    #     ax.imshow(image, cmap='gray')

    #     point = mgridi.reference_point.copy()
    #     if point is not None:
    #         for pt in point:
    #             if not np.isnan(pt[0]) and not np.isnan(pt[1]):
    #                 x, y = pt[0], pt[1]
    #                 ax.scatter(x, y, s=4, color=p_color, marker='o')

    #     pointf = mgridi.correlated_point.copy()
    #     if pointf is not None and point is not None:
    #         assert len(point) == len(pointf), 'size between initial  point and final point does not match.'
    #         for pt0, pt1 in zip(point, pointf):
    #             if not np.isnan(pt0[0]) and not np.isnan(pt0[1]) and not np.isnan(pt1[0]) and not np.isnan(pt1[1]):
    #                 disp_x, disp_y = (pt1[0] - pt0[0]) * scale, (pt1[1] - pt0[1]) * scale
    #                 ax.plot([pt0[0], pt1[0]], [pt0[1], pt1[1]], 
    #                         color=l_color, linewidth=1)

    #     if filename is not None:
    #         plt.savefig(filename, bbox_inches='tight')
    #         return
    #     if text is not None:
    #         plt.text(50, 50, text)
    #     #  plt.show()          