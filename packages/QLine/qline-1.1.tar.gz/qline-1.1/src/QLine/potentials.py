"""This module contains several potential functions."""
# IMPORTING NAMESPACES:
# STANDARD LIBRARY
import numpy as np
import math as ma
# PACKAGE MODULES
import QLine.Constants as const


def harmonic_potential(x, k=1):
    """Creates a harmonic potential.

    Parameters
    ----------
    k : float
       harmonic force constant.
    x : ndarray
       coordinates.

    Returns
    -------
    v : ndarray
    Harmonic potential function (range).
    """
    v = 0.5*k*x**2
    return v


def harmonic_potential_mass_freq(x, m=1, w=1):
    """Creates a harmonic potential.

    Parameters
    ----------
    w : float>0
       frequency
    x : ndarray
       coordinates.

    Returns
    -------
    v : ndarray
    Harmonic potential function (range).
    """
    v = 0.5*m*w**2*x**2
    return v


def force_constant_harmonic_osc(m, w):
    """
    calculates the harmonic oscillator force constant
    based on the mass m and frequency w.
    k = mw^2

    Parameters
    ----------
    m : float>0
       particle mass
    w : float>0
       frequency

    Returns
    -------
    k : float>0
       force constant
    """
    k = m*w**2
    return k


def frequency_harmonic_osc(m, k):
    """
    calculates the harmonic oscillator frequency
    based on the mass m and frequency w.
    w = sqrt(k/m)

    Parameters
    ----------
    m : float>0
       particle mass
    k : float>0
       force constant

    Returns
    -------
    w : float>0
       frequency
    """
    w = np.sqrt(k/m)
    return w


def energy_harmonic_osc(m, w, N):
    """
    calculates the anlytical energy of
    a harmonic oscillator.
    En  = hbar*w(0.5+n)

    Parameters
    ----------
    m : float>0
       particle mass
    w : float>0
       frequency
    N : int
       Number of energies to be displayed starting from the lowest one.

    Returns
    -------
    E : list(float)
       List of energies of the harmonic oscillator.
    """
    E = []
    for i in range(N):
        Ei = const.hbar*w*(i+0.5)
        E.append(Ei)
    return E


def morse_potential(x, De, ke=1, x0=0):
    """ Creates a morse potential.

    Parameters
    ----------
    x : ndarray
       coorinates.
    De : float
       Potential well depth.
    ke : float
       Morse force constant.
    x0 : float
       point of equilibrium.

    Returns
    -------
    v : ndarray
    Morse potential function (range).
    """
    a = ma.sqrt(ke/(2.*De))
    t1 = np.exp(-2.*a*(x-x0))
    t2 = np.exp(-a*(x-x0))
    v = De*(t1-2.*t2)
    return v
