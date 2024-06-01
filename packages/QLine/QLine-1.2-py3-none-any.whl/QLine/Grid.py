"""This module contains methods to create a grid"""
# IMPORTING NAMESPACES:
# STANDARD LIBRARY
import numpy as np
import warnings


class Grid(object):
    """
    This class defines a grid for one-dimensional
    quantum chemisty calculations.

    Attributes
    ----------
    xmin : float
       Lower coordinate range.
    xmax : float
       Upper coordinate range.
    gpd : int
       GridPointDensity of coordinate grid.
    """

    def __init__(self):
        """ Grid constructor. """
        self.xmin = -20
        self.xmax = 20
        self.gpd = 150
        self.xcoord = []
        self.spacing = None

    def set_xrange(self, xmin, xmax):
        """ Sets the Atributes xmin, xmax."""
        self.xmin = xmin
        self.xmax = xmax
        if len(self.xcoord) != 0:
            warnings.warn("The parameters xmin and xmas were changed"
                          + " after creating a grid", stacklevel=2)

    def set_grid_point_density(self, gpd):
        """ Sets the grid point density. """
        self.gpd = gpd
        if len(self.xcoord) != 0:
            warnings.warn("The parameters gpd was changed "
                          + " after creating a grid", stacklevel=2)

    def show_attributes(self, show=False):
        """
        Shows Grid's current attributes.

        Parameters
        ----------
        show : Bool
            If True xcoords will be printed.
        """
        print('\n\n---------------')
        print('1D-GRID DETAILS')
        print('---------------')
        print('Lower coordinate range: xmin = ', self.xmin)
        print('Upper coordinate range: xmax = ', self.xmax)
        print('Grid point density:     gpd  = ', self.gpd)
        print('Evenly spaced Grid:            ', self.spacing)
        xcoord = self.xcoord
        if show:
            print('\nCoordinates: xcoord = \n', xcoord)
        lencoord = len(xcoord)
        if len(xcoord) != 0:
            if self.xmin != xcoord[0] or self.xmax != xcoord[lencoord-1]:
                warnings.warn("Warning: The set x-range parameters "
                              + " do not match the given coordinates!",
                              stacklevel=2)
            current_gpd = int(len(xcoord)/abs(xcoord[lencoord-1]-xcoord[0]))
            if self.gpd != current_gpd:
                warnings.warn("Warning: The set gpd do not match "
                              + " with the given coordinates!", stacklevel=2)

    def create_linear_grid(self):
        """
        Creates a linear grid space with evenly spaced numbers.

        Returns
        -------
        x : float (real numbers)
           real linear coordinate space.
        """
        if len(self.xcoord) != 0:
            warnings.warn("A grid already exists.", stacklevel=2)
        # define number of gridpoints with gpd
        deltaX = abs(self.xmax-self.xmin)
        ngp = int(deltaX*self.gpd)
        x = np.linspace(self.xmin, self.xmax, num=ngp)
        self.xcoord = x
        self.spacing = True
        return x

    def set_default(self):
        """ Sets all attributes to default."""
        self.xmin = -20
        self.xmax = 20
        self.gpd = 150
        self.xcoord = []
        self.spacing = None

    def delete(self):
        """ delets all attributes to None or empty lists."""
        self.xmin = None
        self.xmax = None
        self.gpd = None
        self.xcoord = []
        self.spacing = None


def customized_linear_grid(xmin=-20, xmax=20, gpd=150, show=False):
    """
    creates a customized linear (evenly spaced)
    one dimensinal grid (x-coordinates).

    Parameters
    ----------
    xmin : float
       Lower coordinate range.
    xmax : float
       Upper coordinate range.
    gpd : int
       GridPointDensity of coordinate grid.
    Returns
    -------
    x : float (real numbers)
       real linear coordinate space.
    """
    grid = Grid()
    grid.set_xrange(xmin, xmax)
    grid.set_grid_point_density(gpd)
    x = grid.create_linear_grid()
    grid.show_attributes(show=show)
    return x
