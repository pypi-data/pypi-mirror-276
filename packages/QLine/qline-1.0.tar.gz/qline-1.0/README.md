# QuantumLine(QLine)

Quantumline (QLine) is a python package for solving one-dimensional Schroedinger equations 
using the variational principle and to plot the results in a comfortable way.

## Requirements/Dependencies

Vibrations is an independent code that for running needs only Python3 standard 
packages, extended with NumPy, Scipy and Matplotlib 
(see environment.yml/requierements.txt file in `qline/requirements/`).


## Installation

Just clone this repository, update $PYTHONPATH environment variable accordinly or use pip install in the main folder:

 `qline/ % pip install .` 


Run the tests in `unittests/` folder for verification:

    qline/ % cd unittests/
    qline/unittets/ % pytest -v

For more detailed information, see the installation instructions in `qline/requirements/installationreadme.md`.

## Documentation

The documentation is given in the form of docstrings in the source 
and with examples (jupyter notebooks)

In addition, there is a pdf explaining the quantum mechanics and mathematics of the implementation
(see `qLine/doc/QLine_manual.pdf`)

Create html documentation:

Install the packages from the file:

`qline/requirements/% python -m pip install -r requirements_documenation.txt`

Build HTML documentation with sphinx:

`qline/doc/html_autodoc/% sphinx-build . Build`

To open the html-doc in the browser do the following:

`qline/doc/html_autodoc/Build/$ open index.html`

This HTML is identical to the GitLabPages homepage on:

https://gitlab.com/micwe/qline

https://micwe.gitlab.io/qline/

## Usage

See `examples` directory for some examples of typical runs.

QLines can be run using Python's interpreter, or interactively with
some of the interactive Python consoles.

Any suggestions and improvements are welcome.
