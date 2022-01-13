---
title: 'MSMetaEnhancer: A Python package for mass spectra annotation'
tags:
  - Python
  - mass spectra
  - annotation
authors:
  - name: Matej Troják
    orcid: 0000-0003-0841-2707
    affiliation: 1
  - name: Helge Hecht
    orcid: 0000-0001-6744-996X
    affiliation: 1
  - name: Martin Čech
    orcid: 0000-0002-9318-1781
    affiliation: "1, 2"
  - name: Elliott James Price
    orcid: 0000-0001-5691-7000
    affiliation: 1

affiliations:
 - name: RECETOX, Faculty of Science, Masaryk University, Kotlarska 2, Brno 60200, Czech Republic
   index: 1
 - name: Institute of Organic Chemistry and Biochemistry of the CAS, Prague, Czech Republic
   index: 2
date: 11 January 2022
bibliography: paper.bib
 
---

# Summary

MSMetaEnhancer is a Python software package annotation of mass spectra files. 
The package uses matchms [@Huber2020] for data IO and supports `.msp` input and output data format.
It annotates given mass spectra file by adding missing metadata such as SMILES, InChI, and CAS numbers.
The package retrieves the medatada by querying several external databases, 
currently supporting CIR, CTS [@Wohlgemuth2010], ChemIDplus [@tomasulo2002chemidplus], and PubChem [@kim2021pubchem].
The package is hosted via bioconda and is available on Galaxy.

# Statement of need

Mass spectra data need to be annotated with metadata to make them more reproducible and interoperable with other datasets. 
While this metadata is mostly accessible from public chemical databases, they are not always present in the output of the mass spectrometry libraries. 
Therefore, the data needs to be post-processed and appropriate metadata gathered from reliable sources.
Such a process usually cannot be fully automated, and assistance from the user is required to specify particular annotation steps and sources. 

# State of the field

There are several packages within Python and R ecosystems which support querying external
databases. 
For example, there are R packages that provide an interface to PubChem [@guha2016,@cao2008chemminer], and a package with interface to wikidata [@keys2021]. 
Then, there are packages unifying several sources -- `webchem` [@szocs2020webchem] allows to automatically query chemical data from several web sources and `MetaFetcheR`[@yones2021metafetcher] links metabolite data from several small-compound databases, trying to resolve inconsistencies.

On the Python side, there are packages for PubChem [@swain2017], ChemSpider [@swain2018], or CIR [@swain2016]. 
However, to the best of out knowledge, there is no Python package connecting these sources into a single tool, allowing straightforward annotation of mass spectra files.

# The software package

MSMetaEnhancer 

# Example workflow

Performing annotation of a `.msp` file is straightforward, and requires to specify services to be used and a list of annotation steps.

```python
import asyncio

from MSMetaEnhancer import Application

app = Application()

# import your .msp file
app.load_spectra('input_spectra_file.msp', file_format='msp')

# specify services
services = ['CIR', 'CTS', 'PubChem']

# specify annotation steps
jobs = [('inchikey', 'inchi', 'CIR'),
        ('inchikey', 'name', 'CTS'),
        ('inchi', 'smiles', 'PubChem'),
        ('inchi', 'formula', 'PubChem')]

# run asynchronous annotation of spectra data
asyncio.run(app.annotate_spectra(services, jobs))

# export .msp file
app.save_spectra('annotated_spectra_file.msp', file_format='msp')
```

# Author's Contributions
MT wrote the manuscript and developed the software.
HH contributed to the software and the manuscript.
MČ contributed via code reviews and implementation guidance.
EJP provided conceptual oversight and contributed to the manuscript.

# Acknowledgements
The work was supported from Operational Programme Research, Development and Innovation - project RECETOX RI - CZ.02.1.01/0.0/0.0/16_013/0001761.
This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 857560.
This publication/presentation reflects only the author's view and the European Commission is not responsible for any use that may be made of the information it contains.

# References