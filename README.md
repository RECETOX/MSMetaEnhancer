# MSMetaEnhancer

[![Python package](https://github.com/RECETOX/MSMetaEnhancer/actions/workflows/python-package.yml/badge.svg)](https://github.com/RECETOX/MSMetaEnhancer/actions/workflows/python-package.yml)
[![Python package using Conda](https://github.com/RECETOX/MSMetaEnhancer/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/RECETOX/MSMetaEnhancer/actions/workflows/python-package-conda.yml)

## Overview

Repository for tool that adds more annotations (e.g. SMILES, InChI, CAS number) to MSP files.

## Usage

MSMetaEnhancer provides top level `Application` which implements interface for `.msp` files manipulation and annotation. 
It supports several services which can be used to obtained desired annotation. 
The app uses asynchronous implementation of annotation process, benefiting from non-trivial amount of time spent by waiting for a web query response.

### Example

```python
import asyncio

from MSMetaEnhancer import Application

app = Application()

# import your .msp file
app.load_spectra('tests/test_data/sample.msp', file_format='msp')

# curate given metadata (e.g. fix CAS numbers)
app.curate_spectra()

# specify requested services (these are supported)
services = ['CTS', 'CIR', 'NLM', 'PubChem']

# specify requested jobs
jobs = [('name', 'inchi', 'PubChem'), ('inchi', 'formula', 'PubChem'), ('inchi', 'inchikey', 'PubChem'),
        ('inchi', 'iupac_name', 'PubChem'), ('inchi', 'smiles', 'PubChem')]

# run asynchronous annotations of spectra data
asyncio.run(app.annotate_spectra(services, jobs))

# execute without jobs parameter to run all possible jobs
asyncio.run(app.annotate_spectra(services))

# export .msp file 
app.save_spectra('tests/test_data/sample_out.msp', file_format='msp')
```

## Installation

Installation is currently possible by creating the conda environment with 

`conda env create -f conda/environment-dev.yml`

The tool will be published via pypi and bioconda soon!

## Developer Documentation

### Setup

Create your development environment using the provided [script](conda/environment-dev.yml) via conda to install all required dependencies.

### Contributing

We appreciate contributions - feel free to open an issue on our repository, create your own fork, work on the problem and pose a PR. 
Make sure to add your contributions to the [changelog](CHANGELOG.md) and to adhere to the [versioning](https://semver.org/spec/v2.0.0.html).

### Testing

All functionality is tested with the [pytest](https://docs.pytest.org/en/6.2.x/contents.html) framework.
