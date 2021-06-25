[![Python package](https://github.com/xtrojak/pyMSPannotator/actions/workflows/python-package.yml/badge.svg)](https://github.com/xtrojak/pyMSPannotator/actions/workflows/python-package.yml)

# pyMSPannotator
Repository for tool that adds more annotations (e.g. SMILES, InChI, CAS number) to MSP files (Python version).

### How to use this tool

```python
# import MSP class
from libs.Spectra import Spectra

# create MSP object and import your .msp file
spectra = Spectra()
spectra.load_msp_file('path_to_my_file.msp')

# main function to annotate the MSP file using all available approaches
spectra.annotate_spectrums_all_attributes()

# alternatively, it is possible to specify just particular jobs to do
jobs = [('name', 'inchi', 'PubChem'),
        ('casno', 'inchikey', 'CTS')]
spectra.annotate_spectrums(jobs)

# to get available jobs
available_jobs = spectra.get_available_jobs()

# export file 
spectra.save_msp_file('path_to_a_new_file.msp')
```
