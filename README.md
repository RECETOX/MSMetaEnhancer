## MSMetaEnhancer

[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/msmetaenhancer/README.html)
[![docs](https://readthedocs.org/projects/msmetaenhancer/badge/?version=latest)](https://msmetaenhancer.readthedocs.io/en/latest/)
[![Conda](https://img.shields.io/conda/v/bioconda/msmetaenhancer)](https://anaconda.org/bioconda/msmetaenhancer)
[![PyPI - Python Version](https://img.shields.io/pypi/v/msmetaenhancer)](https://pypi.org/project/msmetaenhancer/)
[![DOI](https://joss.theoj.org/papers/10.21105/joss.04494/status.svg)](https://doi.org/10.21105/joss.04494)

**MSMetaEnhancer** is a tool used for `.msp` files annotation.
It adds metadata like SMILES, InChI, and CAS number fetched from the following services: [CIR](https://cactus.nci.nih.gov/chemical/structure_documentation), [CTS](https://cts.fiehnlab.ucdavis.edu/), [PubChem](https://pubchem.ncbi.nlm.nih.gov/), [IDSM](https://idsm.elixir-czech.cz/), [BridgeDb](https://bridgedb.github.io/), [Wikidata](https://www.wikidata.org/), and [ChEBI](https://www.ebi.ac.uk/chebi/).
The app uses asynchronous implementation of annotation process allowing for optimal fetching speed.

If you use MSMetaEnhancer in your work, please cite the following publication:

Troják et al., (2022). MSMetaEnhancer: A Python package for mass spectra metadata annotation. Journal of Open Source Software, 7(79), 4494, https://doi.org/10.21105/joss.04494

### Usage

```python
import asyncio

from MSMetaEnhancer import Application
from MSMetaEnhancer.libs.converters.web import (
    CTS,
    CIR,
    IDSM,
    PubChem,
    BridgeDb,
    Wikidata,
    ChEBI,
)
from MSMetaEnhancer.libs.converters.compute import RDKit
from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder

ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, Wikidata, ChEBI, RDKit])

app = Application()

# import your .msp file
app.load_data('sample.msp', file_format='msp')

# curate given metadata (e.g. fix CAS numbers)
app.curate_metadata()

# specify requested services (these are supported)
services = ['CTS', 'CIR', 'IDSM', 'PubChem', 'BridgeDb', 'Wikidata', 'ChEBI', 'RDKit']

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

- Python 3.10 - 3.13

Install `MSMetaEnhancer` from Bioconda with:

```
# install MSMetaEnhancer in a new virtual environment to avoid dependency clashes
conda create --name MSMetaEnhancer python=3.12
conda activate MSMetaEnhancer
conda install --channel bioconda --channel conda-forge MSMetaEnhancer
```

Alternatively, install it from PyPI into any environment of your choice:

```
pip install msmetaenhancer
```

### Developer Documentation

#### Setup

Development dependencies, the virtual environment and the package itself are all managed
by [uv](https://docs.astral.sh/uv/). Install uv once (e.g. `pip install uv`, or
`conda install --channel conda-forge uv`), clone the repository and run:

```
uv sync
```

This creates `.venv` in the repository root, installs the locked dependencies together with
the `dev` group, and installs `MSMetaEnhancer` in editable mode. A conda environment can
still be created from the provided [script](conda/environment-dev.yml) if you prefer conda;
it provides `uv` and Python, and `uv sync` then fills in the rest.

Run everything through `uv run` so that it uses this environment:

```
uv run pytest                                          # tests
uv run ruff check .                                    # lint
uv run pre-commit install                              # git hooks
uv run --group docs sphinx-build -b html docs/source docs/build/html   # documentation
```

Dependencies are pinned in the committed `uv.lock`. After changing the dependencies in
`pyproject.toml`, refresh the lock with `uv lock` and reinstall with `uv sync` — CI installs
with `uv sync --frozen` and therefore fails if the two are out of sync.

#### Contributing

We appreciate contributions - feel free to open an issue on our repository, create your own fork, work on the problem and post a PR.
Please add your contributions to the [changelog](CHANGELOG.md) and to adhere to the [versioning](https://semver.org/spec/v2.0.0.html).
For more information see [here](CONTRIBUTING.md).

#### Testing

All functionality is tested with the [pytest](https://docs.pytest.org/en/6.2.x/contents.html) framework.
Run the test suite with `uv run pytest`.
