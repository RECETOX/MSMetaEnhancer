[![Python package](https://github.com/xtrojak/pyMSPannotator/actions/workflows/python-package.yml/badge.svg)](https://github.com/xtrojak/pyMSPannotator/actions/workflows/python-package.yml)

# pyMSPannotator
Repository for tool that adds more annotations (e.g. SMILES, InChI, CAS number) to MSP files (Python version).

### How to use this tool

```python
import asyncio

from app import Application
from libs.Spectra import Spectra
from libs.Curator import Curator

# create Spectra object and import your .msp file
spectra = Spectra()
spectra.load_msp_file('tests/test_data/sample.msp')

# curate given metadata (e.g. fix CAS numbers)
curator = Curator()
spectra = curator.curate_spectra(spectra)

# specify requested services and create Application
services = ['CTS', 'CIR', 'NLM', 'PubChem']
app = Application(services)

# specify requested jobs
jobs = [('name', 'inchi', 'PubChem'), ('inchi', 'formula', 'PubChem'), 
        ('inchi', 'inchikey', 'PubChem'), ('inchi', 'smiles', 'PubChem')]
# run asynchronous annotations of spectra data
spectra.spectrums = asyncio.run(app.annotate_spectra(spectra, jobs))

# export .msp file 
spectra.save_msp_file('tests/test_data/sample_out.msp')
```