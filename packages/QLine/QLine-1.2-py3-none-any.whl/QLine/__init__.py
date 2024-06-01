""" This is the creator method for the QLine package."""

from QLine.Constants import *
from QLine.Grid import *
from QLine.basis_functions import *
from QLine.math_methods import *
from QLine.potentials import *
from QLine.hamiltonian import *
from QLine.schroedinger_eq import *
from QLine.plotting import *

import os
import QLine
path = os.path.dirname(QLine.__file__)


print("=========================================")
print("        Python showcase package")
print("                QLine  ")
print("             Version: 1.0            2023")
print("-----------------------------------------")
print("Author: Michael Welzel")
print("location: ", path)
print("License: GNU GENERAL PUBLIC LICENSE")
print("-----------------------------------------")
print("Everything is calculated in atomic units")
print('=========================================')
