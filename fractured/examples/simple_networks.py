"""
Various method for creating grids for relatively simple fracture networks.

The module doubles as a test framework (though not unittest), and will report
on any problems if ran as a main method.

"""
import sys
import getopt
import numpy as np
import matplotlib.pyplot as plt
import time


from gridding.fractured import meshing
from viz import plot_grid


def single_isolated_fracture(**kwargs):
    """
    A single fracture completely immersed in a boundary grid.
    """
    f_1 = np.array([[-1, 1, 1, -1 ], [0, 0, 0, 0], [-1, -1, 1, 1]])
    domain = {'xmin': -2, 'xmax': 2, 'ymin': -2, 'ymax': 2, 'zmin': -2, 'zmax':
              2}
    grids = meshing.create_grid([f_1], domain, **kwargs)

    return grids


def two_intersecting_fractures(**kwargs):
    """
    Two fractures intersecting along a line.
    """

    f_1 = np.array([[-1, 1, 1, -1 ], [0, 0, 0, 0], [-1, -1, 1, 1]])
    f_2 = np.array([[0, 0, 0, 0], [-1, 1, 1, -1 ], [-.7, -.7, .8, .8]])
    domain = {'xmin': -2, 'xmax': 2, 'ymin': -2, 'ymax': 2, 'zmin': -2, 'zmax':
              2}
    grids = meshing.create_grid([f_1, f_2], domain, **kwargs)

    return grids


def three_intersecting_fractures(**kwargs):
    """
    Three fractures intersecting, with intersecting intersections (point)
    """

    f_1 = np.array([[-1, 1, 1, -1 ], [0, 0, 0, 0], [-1, -1, 1, 1]])
    f_2 = np.array([[0, 0, 0, 0], [-1, 1, 1, -1 ], [-.7, -.7, .8, .8]])
    f_3 = np.array([[-1, 1, 1, -1], [-1, -1, 1, 1], [0, 0, 0, 0]])
    domain = {'xmin': -2, 'xmax': 2, 'ymin': -2, 'ymax': 2, 'zmin': -2, 'zmax':
              2}
    grids = meshing.create_grid([f_1, f_2, f_3], domain, **kwargs)

    return grids


if __name__ == '__main__':
    # If invoked as main, run all tests
    try:
        print(sys.argv[1:])
        opts, args = getopt.getopt(sys.argv[1:], 'v:', ['gmsh_path=',
                                                       'verbose=',
                                                        'visualize='])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    gmsh_path = None
    verbose = 1
    visualize=0
    # process options
    for o, a in opts:
        if o == '--gmsh_path':
            gmsh_path = a
        elif v in ('-v', '--verbose'):
            verbose = a

    success_counter = 0
    failure_counter = 0

    time_tot = time.time()

    #######################
    # Single fracture
    if verbose > 0:
        print('Run single fracture example')
    try:
        time_loc = time.time()
        g = single_isolated_fracture(gmsh_path=gmsh_path, verbose=verbose,
                                     gmsh_verbose=0)
        assert len(g) == 4
        assert len(g[0]) == 1
        assert len(g[1]) == 1
        assert len(g[2]) == 0
        assert len(g[3]) == 0
        print('Single fracture example completed successfully')
        print('Elapsed time ' + str(time.time() - time_loc))
        success_counter += 1
    except Exception:
        print('\n')
        print(' ***** FAILURE ****')
        print('Gridding of single isolated fracture failed')
        failure_counter += 1

    ##########################
    # Two fractures, one intersection
    #
    if verbose > 0:
        print('Run two intersecting fractures example')
    try:
        time_loc = time.time()
        g = two_intersecting_fractures(gmsh_path=gmsh_path, verbose=verbose,
                                     gmsh_verbose=0)
        assert len(g) == 4
        assert len(g[0]) == 1
        assert len(g[1]) == 2
        assert len(g[2]) == 1
        assert len(g[3]) == 0
        print('Two fractures example completed successfully')
        print('Elapsed time ' + str(time.time() - time_loc))
        success_counter += 1
    except Exception:
        print('\n')
        print(' ***** FAILURE ****')
        print('Gridding of two intersecting fractures failed')
        failure_counter += 1

    ##########################
    # Three fractures, three intersection lines
    #
    if verbose > 0:
        print('Run three intersecting fractures example')
    try:
        time_loc = time.time()
        g = three_intersecting_fractures(gmsh_path=gmsh_path, verbose=verbose,
                                     gmsh_verbose=0)
        assert len(g) == 4
        assert len(g[0]) == 1
        assert len(g[1]) == 3
        assert len(g[2]) == 6
        assert len(g[3]) == 1
        print('Three fractures example completed successfully')
        print('Elapsed time ' + str(time.time() - time_loc))
        success_counter += 1
    except Exception:
        print('\n')
        print(' ***** FAILURE ****')
        print('Gridding of three intersecting fractures failed')
        failure_counter += 1
    print('\n')
    print(' --- ')
    print('Ran in total ' + str(success_counter + failure_counter) + ' tests,' \
         +' out of which ' + str(failure_counter) + ' failed.')
    print('Total elapsed time is ' + str(time.time() - time_tot) + ' seconds')
    print('\n')

