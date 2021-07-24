# positioning-sim

A library for generating simulated positioning data for testing GNSS applications.

## Introduction

Positioning-Sim was created as a tool that can easily generate simualted GNSS data in any desired path, using real coordinate systems facilitated by [geographiclib](https://geographiclib.sourceforge.io/html/python/). It should however be trivial to modify the code to use a different geodesic routine library to calculate the coordinates.

## Installation

You can install the library via PyPI using:

`pip install positioning-sim`

Positioning-Sim depends on the following external packages:

- numpy
- geographiclib
- matplotlib

However, matplotlib is only used for plotting and can therefore be considered optional. The following packages from the Python standard library are alo used in the library:

- math
- concurrent
- datetime

## Examples

...
