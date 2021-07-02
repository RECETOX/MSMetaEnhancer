[![Python package](https://github.com/xtrojak/pyMSPannotator/actions/workflows/python-package.yml/badge.svg)](https://github.com/xtrojak/pyMSPannotator/actions/workflows/python-package.yml)

# pyMSPannotator
Repository for tool that adds more annotations (e.g. SMILES, InChI, CAS number) to MSP files (Python version).

### How to use this tool

```python
import asyncio

from app import Application

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