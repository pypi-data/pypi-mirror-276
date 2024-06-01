"""
This module creates the schroedinger equation and
solves this  eigenvalue equation via the basis set method.
"""

# IMPORTING NAMESPACES:
# PACKAGE MODULES
import QLine.math_methods as mm
import QLine.hamiltonian as ha
import QLine.basis_functions as bf
import QLine.Constants as const
# STANDARD LIBRARY
import numpy as np
import heapq


def basis_set_method(x, pot, N=10, m=1, kb=1, mb=1,
                     pre_check=True, periodic=False):
    """
    Solves the Schroedinger equation using the variational principle
    (basis set method):

    Hc = lamb*c

    Parameters
    ----------
    x : numpy.array
       x-coordinates (corresponding to the potential function).
    pot : numpy.array
       potential function range.
    N : int
       basis size and hamiltonian dimension(NxN).
    m : float
       particle mass
    kb : float; Real>0
       wave number of basis functions (harmonic oscillators).
    mb : float
       particle mass of basis functions (harmonic oscillators).

    Returns
    -------
    lamb : array
       energy eigenvalues.
    coeff : ndarray
       coefficient matrix.
    basis : ndarray[:,i]
       set of used basis functions.
    """
    # Crating basis set:
    bs = bf.Basis_Set(x, N)
    basis, basis2dev = bs.create_harmonic_oscillators_vary_n(m=mb, k=kb)
    # Creating hamiltonian:
    matrix = ha.matrix(x, basis, pre_check=pre_check, periodic=periodic)
    H = matrix.hamiltonian(basis2dev, pot, m=m)
    # Solving eigenvalue equation
    lamb, coeff = np.linalg.eigh(H)
    return lamb, coeff, basis


def wave_function_from_coeff(coeff: np.ndarray,
                             basis: np.ndarray) -> np.ndarray:
    """
    composes the coefficients and the basis function to
    the corresponding wavefunction Hpsi=Epsi with

    psi = sum_ij c[ij] * basis[:j]

    Parameters
    ----------
    coeff : ndarray
       coefficient matrix of solving Schroedinger equation(basis_set_method).
    basis : ndarray(dim(xcoord) x N)
        Set of basis functions.

    Returns
    -------
    wafu : ndarray[:,i]
       wave functions of state i.
    """
    N = len(basis[0, :])
    wafu = np.zeros((len(basis[:, 0]), int(N)), dtype=complex)
    for i in range(N):
        for j in range(N):
            wafu[:, i] = wafu[:, i] + coeff[j, i]*basis[:, j]
    return wafu


class Discretization_method(object):
    """
    Solves the one-dimensional Schroedinger equation
    via the discretization method
    (didactic verision - not optimized for perfomance).

    Parameters
    ----------
    x : numpy.array
       One-dimensional coordinates (real) corresponding to the given potential.
    pot : numpy.array
       function value of a given potential function.

    Returns
    -------
    H : numpy.ndarray
       Hamiltonian matrix.
    """

    def __init__(self, x):
        """class constructor."""
        self.x = x
        self.dim = len(x)

    def kinetic(self, m=1):
        """creates the descretized kinetical energy part
           of 1D-Schroedinger equation.

        Parameters
        ----------
        m : float>0
           particle mass.

        Returns
        -------
        T : numpy.ndarray
            kinetical part of hamiltonian.
        """
        self.m = m
        d = abs(self.x[1]-self.x[0])  # grid distance
        term = (-const.hbar**2)/(2*m*d**2)
        T = mm._sec_derivative_matrix(self.dim)
        T = term*T
        self.T = T
        return T

    def potential(self, pot):
        """creates the descretized potential energy part
           of 1D-Schroedinger equation.

        Parameters
        ----------
        pot : numpy.array
           function value of a given potential function.

        Returns
        -------
        V : numpy.ndarray
            potential part of hamiltonian.
        """
        ones = np.identity(self.dim)
        V = pot*ones
        self.pot = pot
        self.V = V
        return V

    def hamiltonian(self, pot, m=1, solve=False):
        """creates the descretized hamiltonian
           of 1D-Schroedinger equation.

        Parameters
        ----------
        pot : numpy.array
           function value of a given potential function.
        m : float>0
           particle mass.
        solve : bool
           If True: solve Hamiltonian eigenvalue problem

        Returns
        -------
        H : numpy.ndarray
            potential part of Hamiltonian.
        energies : numpy.ndarray
           energie eigenvalues.
        wavefuncs : numpy.ndarray
           corresponding wave functions. wavefuncs[:,index]
        """
        T = self.kinetic(m=m)
        V = self.potential(pot)
        H = T + V
        self.H = H
        if solve:
            eigval, eigvec = np.linalg.eig(self.H)
            # sorting eigenvalues and vectoers
            index_ew = heapq.nsmallest(self.dim, enumerate(eigval),
                                       key=lambda x: x[1])
            energies = np.zeros(self.dim, dtype=complex)
            wavefuncs = np.zeros((self.dim, self.dim), dtype=complex)
            for i in range(self.dim):
                energies[i] = eigval[index_ew[i][0]]  # Sorted eigenvalues
                # Sorted - eigenvectors (coloumn vectors)
                wavefuncs[:, i] = eigvec[:, index_ew[i][0]]
            self.energies = energies.real
            # normalize wave functions
            for i in range(self.dim):
                norm = mm.norm(self.x, wavefuncs[:, i])
                wavefuncs[:, i] = wavefuncs[:, i]/norm
            self.wavefuncs = wavefuncs
            return energies.real, wavefuncs
        else:
            return H
