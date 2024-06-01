"""This module contains methods to create basis functions and a basis set."""

# IMPORTING NAMESPACES:
# PACKAGE MODULES
import QLine.Constants as const
# STANDARD LIBRARY
import math as ma
import numpy as np


class Basis_Functions(object):
    """ Class of basis functions.

    Attributes
    ----------
    xcoord : np.ndarray real
       x-coordinates in one-dimension.
    psi : np.ndarray  complex
       Function values of the basis function to
       the corresponding given x-coodinates.
    d2_psi : np.ndarray complex
       Second derivative of the corresponding psi function.
    """

    def __init__(self, xcoord):
        """
        Basis_Functions constructor
        - For Details see Basis_Function docstring.
        """
        self.xcoord = xcoord
        self.psi = []
        self.d2_psi = []

    def create_harmonic_oscillator(self, v, m=1, k=1, show=False):
        """
        Creates harmonic oscillator functions.

        Parameters
        ----------
        v : int
           Quantum number.
        m : float; Real>0
           Particle mass.
        k : float; Real>0
           wave number.

        Returns
        -------
        Psi : float; array(Real)
        Harmonic oscillator function values (physically scaled).
        """
        if show:
            print('\n\n--- Harmonic Oscillator Attributes ---')
            print('       Quantum number, v = ', v)
            print('       Particle mass,  m = ', m)
            print('       Wavenumber,     k = ', k)
            print('--------------------------------------')
        # Normalizations and scalings:
        alph = np.sqrt(k*m/const.hbar)  # Norm scale term
        norm = 1/(np.sqrt(2**float(v)*ma.factorial(v)))  # norm of function
        chi = alph**0.5*self.xcoord  # scaling parameter for hermite polynom
        pre_term = (alph/ma.pi)**0.25  # Expanded Pre-Term
        # Needed Functions:

        def _gauss(z):
            """Gaussian."""
            gauss = np.exp(-z**2/2)  # gauss function
            return gauss

        def _hermite_polynom(z, n):
            """
            Creates hermite polynoms (physical version).

            Parameters
            ----------
            z : float ; Real
               (Physically) Scaled coordinates.
            n : int
               Hermite polynom order.

            Returns
            -------
            H : array(1 x dim(x-coordinates))
            Functionsvalues of a hermite polynom in order n.
            """
            # Hermite polynomial - recursive formula
            H = [np.ones(len(z)), 2.*z]
            for i in range(1, n+1):
                Hn = 2.*z*H[i]-2.*i*H[i-1]
                H.append(Hn)
            return H[n]

        hermit = _hermite_polynom(chi, v)  # Hermite Polynomfunction
        gauss = _gauss(chi)
        psi = norm*pre_term*hermit*gauss  # Harmonic oscillator
        self.psi = psi
        return psi

    def create_sec_derivative_of_harmonic_oscillator(self, v, m=1, k=1):
        """
        Creates the analytical second derivative of the harmonic oscillator.

        For attributes, parameters and returns see at
        create_harmonic_oscillator().
        """
        dim = len(self.xcoord)
        alph = np.sqrt(k*m/const.hbar)  # Pre-Term
        chi = alph**0.5*self.xcoord  # scaling parameter for hermite polynom
        ones = np.ones(dim)
        term = chi**2 - ones - 2*ones*v
        ps = self.create_harmonic_oscillator(v, m=m, k=k)
        d2_psi = term*ps*alph
        self.d2_psi = d2_psi
        self.psi = ps
        return d2_psi


class Basis_Set(object):
    """
    Creates a basis set.

    Attributes
    ----------
    xcoord : array
       x-coordinates.
    N : int
       Basis set size.
    basis_set : ndarray(dim(xcoord) x N)
        Set of basis functions.
    deriv_basis_set : ndarray(dim(xcoord) x N)
        Second derivatives of the corresponding basis functions.
    analytic_deriv : Bool
        Second derivative is analytical(True)/numerical(False)
    """
    def __init__(self, xcoord, N):
        """Basis_Set constructor - For Details see Basis_Set docstring."""
        self.xcoord = xcoord
        self.N = int(N)
        self.basis_set = []
        self.deriv2_basis_set = []
        self.analytic_deriv = None

    def create_harmonic_oscillators_vary_n(self, m=1, k=1, analytical=True):
        """
        Creates a base set consisting of harmonic oscillators
        (and their seond derivatives) ordered by quantum number.

        Parameters
        ----------
        m : float; Real>0
           Particle mass.
        k : float; Real>0
           wave number.
        analytical : Bool
           Second derivative is analytical (True) or numerical (False)

        Returns
        -------
        basis_set[:,v] : float; ndarray(dim(xcoord x N)), Real
           Set of harmonic oscillator functions (physically scaled).
        deriv2_basis_set[:,v] : float; ndarray(dim(xcoord x N)), Real
           Set of second derivatives of corresponding
           harmonic oscillator functions.
        """
        self.analytic_deriv = analytical
        dim_coord = len(self.xcoord)
        # Create basis functions
        self.basis_set = np.zeros((dim_coord, self.N))
        BF = Basis_Functions(self.xcoord)
        for v in range(self.N):
            self.basis_set[:, v] = BF.create_harmonic_oscillator(v, m=m, k=k)
        # Create second derivatives of basis functions
        self.deriv2_basis_set = np.zeros((dim_coord, self.N))
        if analytical:  # Analytical
            for v in range(self.N):
                self.deriv2_basis_set[:, v] = (
                   BF.create_sec_derivative_of_harmonic_oscillator(v, m=m, k=k)
                )
        return self.basis_set, self.deriv2_basis_set
