# posim

A library for generating simulated positioning data for testing GNSS applications.

## Introduction

Posim (short for Positioning Simulator) was created as a tool that can easily generate simualted GNSS data in any desired path, using real coordinate systems facilitated by [geographiclib](https://geographiclib.sourceforge.io/html/python/). It should however be trivial to modify the code to use a different geodesic routine library to calculate the coordinates.

See the [Wiki](https://github.com/zrowland885/posim/wiki) for documentation.

## Installation

You can install the library via PyPI (https://pypi.org/project/posim/) using:

`pip install posim`

Posim depends on the following external packages:

- ``numpy``
- ``geographiclib``
- ``matplotlib``

However, matplotlib is only used for plotting and can therefore be considered optional.

## Examples

...
