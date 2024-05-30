"""This module creates the hamiltonian and correspondings matrices."""

# IMPORTING NAMESPACES:
# PACKAGE MODULES
import QLine.math_methods as mm
# STANDARD LIBRARY
import numpy as np
import warnings


class matrix(object):
    """
    Creates a matrix object with Matrix:=<X|O|X">,
    where <.,.> is a scalar product, O an Operator,
    X the basis function and X" the second derivative
    of the basis function.
    The basis set have to be orthonormalized set.

    Parameters
    ----------
    coord : np.ndarray
       Coordinates 1D.
    basis_set : np.ndarray[:,i]
        basis functions, numpy.array[:,i]; where i is the function set
        index number.
    N : int
       matrix dimensions and basis set size.
    pre_check : bool
       If True - checks the input data for correctness
       in respect to the basis set.
    loew_T : numpy.ndarray or None
       loewdin orthonormalization transformation matrix
       (see src/math_methods.py).
    periodic : bool
       if True: basis functions have not to reach zero
       at coordinate limits(periodic basis functions).
    """
    def __init__(self, x_coord, basis_set, pre_check=True, periodic=False):
        """matrix constructor - For Details see matrix docstring."""
        self.x_coord = x_coord
        self.basis_set = basis_set
        self.N = len(basis_set[0, :])
        self.loew_T = None

        # checking the input data for correctness:
        self.pre_check = pre_check
        if self.pre_check:

            # Dimensional check for basis set input
            if len(basis_set[0, :]) >= len(basis_set[:, 0]):
                warn_size = ("Dimensions of your basis functions"
                             + " could be arranged incorrectly.")
                warnings.warn(warn_size, stacklevel=2)

            # Verifying that basis set approch zero at long distances
            if periodic is False:
                for i in range(self.N):
                    check = mm.function_range_threshhold_check(basis_set[:, i])
                    if check is False:
                        raise ValueError("The basis set functions must reach"
                                         + " zero at coordinate limits.")

            # verifying:  orthonormality and linear dependency
            S = self.overlap()
            # linear dependency
            det = np.linalg.det(S)
            print('det=', det)
            if np.isclose(det, 0):
                raise ValueError("The given basis set is "
                                 + "linearly dependend.")
            # Orthonormality
            ref_ONB = np.identity(self.N)
            if np.allclose(abs(S), abs(ref_ONB)) is False:
                warn_ONB = ("The given basis is not orthonormalized and thus "
                            + "unreasonable results are possible.")
                warnings.warn(warn_ONB, stacklevel=2)
                print("If you do not want to perform orthonormalization, "
                      + "suppress the pre-check:")
                print('matrix(x_coord,basis_set,pre_check=False)')
                print('                         ---------------')
                # try loewdin orthonormalization:
                Q, T = mm.orthogonalization_loewdin(self.x_coord,
                                                    self.basis_set)
                self.basis_set = Q
                self.loew_T = T
                print('Basis set Matrix       [dim(x) times N] : B')
                print('Orthonormalized Matrix [dim(x) times N] : Q')
                print('Transformation matrix       [N times N] : trans')
                print('-----------------------------------------------')
                print('Q = B*trans')

    def overlap(self, show=False) -> np.ndarray:
        """
        Calculates the overlapp matrix S_ij = <f_i|f_j>,
        where f_i are the basis functions with index i and j.

        Parameters
        ----------
        show : bool
           If True - printing overlap/orthonormality matrix.

        Returns
        -------
        S_mat : ndarray[N,N]
        overlap matrix.
        """
        S_mat = mm._overlapmatrix(self.x_coord, self.basis_set)
        if show:
            print("\nOrthonormality/overlap matrix: S=\n",
                  np.around(S_mat, decimals=2))
        return S_mat

    def kinetic(self, sec_derivative: np.ndarray,
                m=1, show=False) -> np.ndarray:
        """
        Creates the matrix of kinetic energy Tij=(-1/(2m))<f_i,f"_j>,
        where f_i are the basis functions with index i and j.
        f" is the corresponding second derivative.

        Parameters
        ----------
        sec_derivative : ndarray[:,i]
             have to be the set of second derivatives of the given basis set.
        m : float
            particle mass.
        show : bool
           If True - printing overlap/orthonormality matrix.

        Returns
        -------
        T : ndarray[N,N]
        Matrix of kinetic energy.
        """
        N = self.N
        if np.shape(self.loew_T) == (N, N):
            sec_derivative = np.matmul(sec_derivative, self.loew_T)
            str1_1 = "2nd derivatives of the given (untransformed) "
            str1_2 = "basis functions were transformed "
            str1 = str1_1 + str1_2
            str2 = "according to loewdin-orthonormalization which which has "
            str3 = "already been performed for the given basis.\n"
            print("\nFor your information:\n"+str1+str2+str3)
            print("2nd derivative basis set Matrix       "
                  + "[dim(x) times N] : B\'\'")
            print("Orthonormalized 2nd derivative Matrix "
                  + "[dim(x) times N] : Q\'\'")
            print("Transformation matrix       [N times N] : trans")
            print("----------------------------------------------------------")
            print("Q\'\' = B\'\'*trans")
        T = np.zeros((N, N), dtype=complex)
        pre_factor = (-1.)/(2.*m)
        for i in range(N):
            for j in range(N):
                f1 = self.basis_set[:, i]
                f2 = sec_derivative[:, j]
                T[i, j] = mm.braket(self.x_coord, f1, f2)*pre_factor
        if show:
            print("\nKinetic matrix: T=\n", np.around(T, decimals=2))
        return T

    def potential(self, pot: np.ndarray, show=False) -> np.ndarray:
        """
        Creates the matrix of potential energy Vij=<f_i,V*f_j>,
        where f_i are the basis functions with index i and j.
        V is the potential function.

        Parameters
        ----------
        pot : array
           Potential function (range/image).
        show : bool
           If True - printing overlap/orthonormality matrix.

        Returns
        -------
        V : ndarray[N,N]
        Matrix of potential energy.
        """
        N = self.N
        V = np.zeros((N, N), dtype=complex)
        dim = len(self.basis_set[:, 0])
        pot_basis = np.zeros((dim, N), dtype=complex)
        for j in range(N):
            pot_basis[:, j] = self.basis_set[:, j]*pot[:]
        for i in range(N):
            for j in range(N):
                f1 = self.basis_set[:, i]
                f2 = pot_basis[:, j]
                V[i, j] = mm.braket(self.x_coord, f1, f2)
        if show:
            print("\nPotential matrix: V=\n", np.around(V, decimals=2))
        return V

    def hamiltonian(self, sec_derivative, pot, m=1, show=False):
        """
        Creates the hamiltonian Hij= Tij + Vij based on
        the matrix of kinetic energy Tij and potential energy Vij.

        Parameters
        ----------
        sec_derivative : ndarray[:,i]
             have to be the set of second derivatives of the given basis set.
        m : float
            particle mass.
        pot : array
           Potential function (range/image).
        show : bool
           If True - printing overlap/orthonormality matrix.

        Returns
        -------
        H : ndarray[N,N]
        Hamiltonian matrix.
        """
        T = self.kinetic(sec_derivative, m=m, show=show)
        V = self.potential(pot, show=show)
        H = T + V
        if show:
            print('\n\nHamiltonian: H=\n', np.around(H, decimals=2))
        return H
