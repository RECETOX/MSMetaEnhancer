[![Python package](https://github.com/xtrojak/pyMSPannotator/actions/workflows/python-package.yml/badge.svg)](https://github.com/xtrojak/pyMSPannotator/actions/workflows/python-package.yml)

# pyMSPannotator
Repository for tool that adds more annotations (e.g. SMILES, InChI, CAS number) to MSP files (Python version).

### How to use this tool

```python
# import MSP class
from libs.MSP import MSP

# create MSP object and import your .msp file
msp = MSP()
msp.load_msp_file('path_to_my_file.msp')

# specify required annotations to be added to the MSP file (possible a subset of these)
required_annotations = ['inchikey', 'smiles', 'inchi', 'name', 'IUPAC', 'formula']
# main function to annotate the fule
msp.annotate_spectrums(required_annotations)

# export file 
msp.save_msp_file('path_to_a_new_file.msp')
```
