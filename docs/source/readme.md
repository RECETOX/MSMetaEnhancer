## MSMetaEnhancer

[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/msmetaenhancer/README.html)
[![docs](https://readthedocs.org/projects/msmetaenhancer/badge/?version=latest)](https://msmetaenhancer.readthedocs.io/en/latest/)
[![Conda](https://img.shields.io/conda/v/bioconda/msmetaenhancer)](https://anaconda.org/bioconda/msmetaenhancer)
[![PyPI - Python Version](https://img.shields.io/pypi/v/msmetaenhancer)](https://pypi.org/project/msmetaenhancer/)
[![DOI](https://joss.theoj.org/papers/10.21105/joss.04494/status.svg)](https://doi.org/10.21105/joss.04494)

**MSMetaEnhancer** is a tool used for `.msp` files annotation.
It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR](https://cactus.nci.nih.gov/chemical/structure_documentation), [CTS](https://cts.fiehnlab.ucdavis.edu/), [PubChem](https://pubchem.ncbi.nlm.nih.gov/), [IDSM](https://idsm.elixir-czech.cz/), and [BridgeDb](https://bridgedb.github.io/).
The app uses asynchronous implementation of annotation process allowing for optimal fetching speed.

If you use MSMetaEnhancer in your work, please cite the following publication:

Troják et al., (2022). MSMetaEnhancer: A Python package for mass spectra metadata annotation. Journal of Open Source Software, 7(79), 4494, https://doi.org/10.21105/joss.04494

### Usage

```python
import asyncio

from MSMetaEnhancer import Application

app = Application()

# import your .msp file
app.load_data('sample.msp', file_format='msp')

# curate given metadata (e.g. fix CAS numbers)
app.curate_metadata()

# specify requested services (these are supported)
services = ['CTS', 'CIR', 'IDSM', 'PubChem', 'BridgeDb', 'RDKit']

# specify requested jobs
jobs = [('name', 'inchi', 'IDSM'), ('inchi', 'formula', 'IDSM'), ('inchi', 'inchikey', 'IDSM'),
        ('inchi', 'iupac_name', 'IDSM'), ('inchi', 'canonical_smiles', 'IDSM')]

# run asynchronous annotations of spectra data
asyncio.run(app.annotate_spectra(services, jobs))

# export .msp file
app.save_data('sample_out.msp', file_format='msp')
```

### Installation

Prerequisites:

- Python 3.9+
- Anaconda

Install `MSMetaEnhancer` from Bioconda with:

```
# install MSMetaEnhancer in a new virtual environment to avoid dependency clashes
conda create --name MSMetaEnhancer python=3.9
conda activate MSMetaEnhancer
conda install --channel bioconda --channel conda-forge MSMetaEnhancer
```

### Developer Documentation

#### Setup

Create your development environment using the provided [script](conda/environment-dev.yml) via conda to install all required dependencies.

#### Contributing

We appreciate contributions - feel free to open an issue on our repository, create your own fork, work on the problem and post a PR.
Please add your contributions to the [changelog](CHANGELOG.md) and to adhere to the [versioning](https://semver.org/spec/v2.0.0.html).
For more information see [here](CONTRIBUTING.md).

#### Testing

All functionality is tested with the [pytest](https://docs.pytest.org/en/6.2.x/contents.html) framework.
