"""This module includes various useful and mathematical methods."""
# IMPORTING NAMESPACES:
# STANDARD LIBRARY
import numpy as np
import scipy.linalg as sp  # science python
import warnings


def even_space_check(x: np.ndarray) -> bool:
    """ Checks if an array is evenly spaced.

    Parameters
    ----------
    x : array
       ordinary array.

    Returns
    -------
    check : bool
       evenly spaced(True), not evenly spaced(False)
    """
    dim = len(x)
    dm = []
    for i in range(dim-1):
        dm.append(x[i+1]-x[i])
    dmtest = np.full((1, len(x)-1), x[1]-x[0])
    check = np.allclose(dm, dmtest)
    return check


def _sec_derivative_matrix(dim, formula='fast'):
    """
    creates the second derivative matrix:
    (-2   1   0        ...   0 )
    ( 1  -2   1  0     ...   0 )
    ( 0   1  -2  1  0  ...   0 )

    ( ........................ )

    ( 0 ......... 0  1  -2   1 )
    ( 0 ............ 0   1  -2 )

    without the term 1/Delta^2.

    Parameters
    ----------
    dim : int
       dimension of the matrix

    Returns
    -------
    kinmat : numpy.ndarray
        kinetic matrix [dimension x dimension]
    """
    if formula == 'education':
        kinmat = np.zeros((dim, dim), dtype=complex)
        for i in range(dim):
            for j in range(dim):
                if i == j:
                    kinmat[i, j] = -2
                elif i == j + 1 or i == j - 1:
                    kinmat[i, j] = 1
    else:
        two = -2*np.ones(dim)
        ones = np.ones(dim-1)
        kinmat = (np.diagflat(two, 0)
                  + np.diagflat(ones, 1)
                  + np.diagflat(ones, -1))
    return kinmat


def second_derivative_num(x: np.ndarray, func: np.ndarray) -> np.ndarray:
    """
    Creates the second derivative using the matrix-vector formalism
    of an function with compact support (function approaches
    zero at domain edges) and a evenly spaced grid.

    finite difference method: 3-point-formalism.

    Parameters
    ----------
    x : array
       coordinates - Domain space of a function.
    func : array
       functionvalues - image space of a function.

    Returns
    -------
    d2func : array
       numerical second derivative of the given function.
    """
    check = even_space_check(x)
    if check is False:
        raise ValueError("Coordinates are not evenly spaced.")
    check = function_range_threshhold_check(func)
    if check is False:
        str1 = "The input function is non-zero on the input boundaries. "
        warn_size = str1 + "Edge of the derivation possibly unreasonable"
        warnings.warn(warn_size, stacklevel=2)
    dim = len(x)
    d = abs(x[1]-x[0])
    d2 = _sec_derivative_matrix(dim)
    d2func = np.matmul(d2, func)/d**2.  # matrix vector multiplication
    return d2func


def braket(x_coord: np.ndarray, f1: np.ndarray, f2: np.ndarray) -> np.ndarray:
    # Scalarproduct of functions/ Bra-Ket
    """
    calculates the scalar product <f,g>, where
    f,g are functions.
    and <.,.> is the sesquilinear inner product.
    The function domain and range have to be evenly spaced.

    Parameters
    ----------
    x_coord : array
        coordinates (function range of f1,f2).
    f1,f2 : array[:]
        function range/image.

    Returns
    -------
    scapr : float
    scalar product of the functions f1,f2 with their domain x_coord.
    """
    check = even_space_check(x_coord)
    if check is False:
        raise ValueError("The parameter x_coord have to be evenly spaced.")
    d = np.abs(x_coord[1]-x_coord[0])
    scapr = np.vdot(f1, f2)*d  # d = integration measure
    return scapr


def norm(x_coord: np.ndarray, f: np.ndarray) -> np.ndarray:
    # Scalarproduct  norm of functions/ Bra-Ket
    """
    calculates the scalar product norm
           ||f|| = sqrt(<f,f>),
    where f is a function.
    and <.,.> is the sesquilinear inner product.
    The function domain and range have to be evenly spaced.

    Parameters
    ----------
    x_coord : array
        coordinates (function range of f).
    f : array[:]
        function range/image.

    Returns
    -------
    scapr : float
    scalar product of the functions f1,f2 with their domain x_coord.
    """
    check = even_space_check(x_coord)
    if check is False:
        raise ValueError("The parameter x_coord have to be evenly spaced.")
    d = np.abs(x_coord[1]-x_coord[0])
    scapr = np.sqrt(np.vdot(f, f)*d)  # d = integration measure
    return scapr


def _overlapmatrix(x_coord, basis):
    """
    calculates the overlap matrix S=<fi,fj>:
    fi = basis[:,i],
    fj = basis[:,j],
    where x_coord -> fi,fj.

    Parameters
    ----------
    x_coord : numpy.array, real
       one-dimensional coordinates.
    basis : numpry.ndarray
        matrix of "i" basis functions [:,i]

    Returns
    -------
    S : numpy.ndarray
       overlap matrix.
    """
    N = len(basis[0, :])
    S = np.zeros((N, N), dtype=complex)
    for i in range(N):
        for j in range(N):
            f1 = basis[:, i]
            f2 = basis[:, j]
            S[i, j] = braket(x_coord, f1, f2)
    return S


def orthogonalization_loewdin(x_coord, basis, show=False):
    """
    calculates a loewdin orthogonalization for a given basis set
    to build a reasonable ONS.

    Parameters
    ----------
    x_coord : numpy.array, real
       one-dimensional coordinates.
    basis : numpry.ndarray
        matrix of "i" basis functions [:,i]
    show : Bool
        if True : overlap and transformation matrix will be printed.

    Returns
    -------
    Q : numpy.ndarray
       ortogonlizated basis.
    T : numpy.ndarray
       Transformation Matrix.
    """
    print("\n\n"+"---"*15+"\n Loewdin orthogonalization algorithm is used.\n")

    # Create overlap matrix
    S = _overlapmatrix(x_coord, basis)

    # Create Transformation matrix T
    def _loewdin_transformation(S):
        """
        Transformation: Q = XT = X S^(-1/2)
        X = given basis set
        T = transformation matrix
        S = overlap matrix
        Q = orthonormalized basis set
        """
        S_sqr = sp.sqrtm(S)
#        S_inv_sqr = np.linalg.inv(S_sqr)
        S_inv_sqr = sp.inv(S_sqr)
        T = S_inv_sqr
        return T

    T = _loewdin_transformation(S)

    # Orthonormalize given Basis
    Q = np.matmul(basis, T)

    # show intermediate steps
    if show:
        print("\nOverlap matrix: S= \n", np.around(S, decimals=3))
        print("\nTransformation matrix:T=S^(-1/2)= \n",
              np.around(T, decimals=3))
    return Q, T


def function_range_threshhold_check(func):
    """
    checks if the boundary values of a given function are approximately zero.

    Parameters
    ----------
    func : numpy.array
       Arbitrary function values.

    Returns
    -------
    check : bool
       True if the function is zero at the edges.
    """
    thresh = 0
    start = func[0]
    end = func[len(func)-1]
    check_start = np.isclose(start, thresh)
    check_end = np.isclose(end, thresh)
    if check_start and check_end:
        check = True
    else:
        check = False
    return check
