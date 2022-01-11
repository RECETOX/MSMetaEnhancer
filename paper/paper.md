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

MSMetaEnhancer is a software package annotation of mass spectra files. 
The package uses matchms [@Huber2020] for data IO and supports `.msp` input and output data formats.
It annotates given mass spectra file by adding missing metadata such as SMILES, InChI, and CAS numbers.
The package retrieves the medatada by querying several external databases, 
currently supporting CIR, CTS [@Wohlgemuth2010], ChemIDplus [@tomasulo2002chemidplus], and PubChem [@kim2021pubchem].
The package is hosted via bioconda and is available on Galaxy.

# Statement of need

TBD

- single python package connecting multiple services
- efficient performance
- adjustable annotation process

# State of the field

TBD

- [@yones2021metafetcher]
- webchem

# Example of use

TBD

# Author's Contributions
HT wrote the manuscript and developed the software.
HH contributed to the software and the manuscript.
MČ contributed via code reviews and implementation guidance.
EJP provided conceptual oversight and contributed to the manuscript.

# Acknowledgements
The work was supported from Operational Programme Research, Development and Innovation - project RECETOX RI - CZ.02.1.01/0.0/0.0/16_013/0001761.
This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 857560.
This publication/presentation reflects only the author's view and the European Commission is not responsible for any use that may be made of the information it contains.

# References