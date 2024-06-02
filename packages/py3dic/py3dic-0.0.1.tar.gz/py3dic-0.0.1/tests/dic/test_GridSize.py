#%%
import pytest
import numpy as np
from py3dic.dic.pydicGrid import \
    GridSize, DIC_Grid

def test_winsize():
    grid_size = GridSize(xmin=0, xmax=10, xnum=11, win_size_x=10, 
            ymin=0, ymax=10, ynum=11, win_size_y=10)
    win_size = grid_size.winsize()
    assert win_size == (10, 10)

def test_prepare_gridXY_correct_shape():
    grid_size = GridSize(xmin=0, xmax=10, xnum=11, win_size_x=10, 
            ymin=0, ymax=10, ynum=21, win_size_y=10)
    grid_xy = grid_size.prepare_gridXY()
    assert grid_xy[0].shape == (11, 21)
    assert grid_xy[1].shape == (11, 21)

def test_prepare_gridXY_correct_values():
    grid_size = GridSize(xmin=0, xmax=10, xnum=11, win_size_x=10, 
            ymin=0, ymax=10, ynum=21, win_size_y=10)
    grid_xy = grid_size.prepare_gridXY()
    for i in range(10):
        for j in range(20):
            assert grid_xy[0][i, j] == i
            assert grid_xy[1][i, j] == j*0.5

def test_create_DIC_Grid_bard():
    grid_size = GridSize(xmin=0, xmax=10, xnum=11, win_size_x=10, 
            ymin=0, ymax=10, ynum=21, win_size_y=10)
    dic_grid:DIC_Grid = grid_size.create_DIC_Grid()
    assert dic_grid.size_x  == 11
    assert dic_grid.size_y  == 21
    assert dic_grid.grid_x.shape == (11, 21)
    assert dic_grid.grid_y.shape == (11, 21)

def test_from_tuplesXY_bard():
    xtuple = (0, 10, 11, 10)
    ytuple = (0, 10, 21, 10)
    grid_size = GridSize.from_tuplesXY(xtuple, ytuple)
    grid_size.prepare_gridXY()
    assert grid_size.winsize() == (10, 10)
    assert grid_size.grid_x.shape == (11,21)
    assert grid_size.grid_y.shape == (11,21)


def test_gridsize_init():
    gs = GridSize(0, 10, 5, 2, 0, 10, 5, 2)
    assert gs.xmin == 0
    assert gs.xmax == 10
    assert gs.xnum == 5
    assert gs.win_size_x == 2
    assert gs.ymin == 0
    assert gs.ymax == 10
    assert gs.ynum == 5
    assert gs.win_size_y == 2

def test_winsize():
    gs = GridSize(0, 10, 5, 2, 0, 10, 5, 2)
    assert gs.winsize() == (2, 2)

def test_prepare_gridXY():
    gs = GridSize(0, 10, 5, 2, 0, 10, 5, 2)
    grid_x, grid_y = gs.prepare_gridXY()
    assert np.array_equal(grid_x, np.mgrid[0:10:5*1j, 0:10:5*1j][0])
    assert np.array_equal(grid_y, np.mgrid[0:10:5*1j, 0:10:5*1j][1])

@pytest.mark.parametrize("xtuple, ytuple", [((0, 10, 5, 2), (0, 10, 5, 2))])
def test_from_tuplesXY(xtuple, ytuple):
    gs = GridSize.from_tuplesXY(xtuple, ytuple)
    assert gs.xmin == xtuple[0]
    assert gs.xmax == xtuple[1]
    assert gs.xnum == xtuple[2]
    assert gs.win_size_x == xtuple[3]
    assert gs.ymin == ytuple[0]
    assert gs.ymax == ytuple[1]
    assert gs.ynum == ytuple[2]
    assert gs.win_size_y == ytuple[3]

# As `create_DIC_Grid` depends on a `DIC_Grid` object which is not defined in your code snippet,
# I can't write a test for it. You may need to modify this test to fit your real situation.
def test_create_DIC_Grid():
    gs = GridSize(0, 10, 5, 2, 0, 10, 5, 2)
    dic_grid = gs.create_DIC_Grid()
    assert isinstance(dic_grid, DIC_Grid)  # Assuming DIC_Grid is your class name.
    assert np.array_equal(dic_grid.grid_x, gs.grid_x)
    assert np.array_equal(dic_grid.grid_y, gs.grid_y)
    assert dic_grid.size_x == gs.xnum
    assert dic_grid.size_y == gs.ynum

if __name__ == '__main__':
    pytest.main()