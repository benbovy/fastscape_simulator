# Fastscape simulator

A simple simulator of landscape evolution (suited for use with an
optimization or inversion framework).

## Installation (using `conda`)

A new `conda` environment with all required dependencies can be created
and activated using the following commands:

```
$ conda env create --file environment.yml
$ source activate fastscape-simulator
```

## Usage

This simulator can be used either from within Python (>3.5) or from
the command line, e.g.,

```python
>>> from fastscape import run_fastscape
>>> run_fastscape(1e-5, 1e-3, 1e-4)
```

```
$ python fastscape.py 1e-5 1e-3 1e-4 --output out.npy
```

Other parameters can be set (see `run_fastscape` docstrings or use the
command `python fastscape.py -h`).

## Documentation

The simulator is briefly documented in the notebook `example.ipynb` in
this repository.

## Some useful references

- A general review of landscape evolution models:
  [Tucker and Hancock, 2010](http://onlinelibrary.wiley.com/doi/10.1002/esp.1952/abstract)

- A more detailed review of the stream power model:
  [Lague, 2014](http://onlinelibrary.wiley.com/doi/10.1002/esp.3462/abstract)

- The algorithm used to solve the stream power law:
  [Braun and Willett, 2013](https://www.sciencedirect.com/science/article/pii/S0169555X12004618)
