# Behaverse Python Package

This package is a Python implementation of the Behaverse API. It allows you to interact with the Behaverse datasets in Python.

## Installation

To install the package, you can use pip:

```bash
pip install behaverse
```

## Usage

See the [Behaverse website](https://behaverse.github.io/) for more information on how to use the package.

## License

TODO

## Contributing


### Development

Before starting development, you need to install the dependencies. You can do this by creating a new conda environment as defined in the `environment.yml` file:

```bash
mamba env create -f environment.yml
mamba activate behaverse
```

### Documentation

To generate documentations and API reference, run the following commands from the main directory of the project:

```bash
cd docs
quartodoc build && quartodoc interlinks && quarto preview
```

The documentation will be available in the `docs/_site/` directory.



## Acknowledgements

TODO

## Citation

TODO
