"""
This module creates the schroedinger equation and
solves this  eigenvalue equation via the basis set method.
"""

# STANDARD LIBRARY
import numpy as np
import matplotlib.pylab as plt


def plot_wfunctions_within_potential(xcoord: np.ndarray, pot: np.ndarray,
                                     lamb: np.ndarray, wavefunc: np.ndarray,
                                     xmin=-10, xmax=10, ymin=-3, ymax=12,
                                     savefig=False
                                     ) -> None:
    """
    Plots the wave functions within the corresponding potential.

    Parameters
    ----------
    xcoord : array
       x-coordinates.
    pot : arrray
       potential function range/image
    wavefunc : ndarray[:,i]
       wavefunction ranges from Schroedinger equation.
    lamb : array
       energy eigenvalues.
    xmin : float
       lower threshold for plot in respect to the coordinate x.
    xmax : float
       uper threshold for plot in respect to the coordinate x.
    ymin : float
       lower threshold for plot in respect to the function values(potential).
    ymax : float
       upper threshold for plot in respect to the function values(potential).
    savefig : bool
       if true = Figure will be saved as png
    """
    plt.figure()
    plt.axhline(y=0, color="black", linestyle="--", lw=2)
    plt.plot(xcoord, pot, lw=4, label=r"V(x)")
    for i, val in enumerate(lamb):
        wfplot = wavefunc[:, i].real + val
        plt.axhline(y=val, color="black", linestyle="--", lw=1)
        plt.plot(xcoord, wfplot, color="blue")
    plt.plot(xcoord, wfplot, color="blue", label=r"$\psi_n(x)$")
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    plt.legend()
    plt.xlabel("x/a.u.")
    plt.ylabel("E/a.u.")
    if savefig:
        plt.savefig("HO_pot_wf.png")
    plt.show()


def plot_energy_levels(lamb: np.ndarray, decimals=1, savefig=False) -> None:
    """
    plots the energy levels.

    Parameters
    ----------
    lamb : array
        energy eigenvalues.
    decimals : int
       Number of decimal places in the plot.
    savefig : bool
       if true = Figure will be saved as png
    """
    plt.figure()
    plt.axhline(y=0, color="purple", linestyle="--", lw=2)
    for _i, val in enumerate(lamb):
        plt.axhline(y=val, xmin=0.2, xmax=0.3,
                    color="black", linestyle="-", lw=2)
        plt.text(0.16, val, np.around(val, decimals=decimals))
    plt.xticks([])
    plt.yticks(fontsize=20)
    plt.xlim(0, 0.5)
    plt.xlabel("E/a.u.")
    plt.title("Energy level")
    if savefig:
        plt.savefig("HO_Elevel.png")
    plt.show()
