---
title: 'MSMetaEnhancer: A Python package for mass spectra metadata annotation'
tags:
  - Python
  - mass spectra
  - annotation
authors:
  - name: Matej Troják
    orcid: 0000-0003-0841-2707
    affiliation: 1
  - name: Helge Hecht^[corresponding author]
    orcid: 0000-0001-6744-996X
    affiliation: 1
  - name: Martin Čech
    orcid: 0000-0002-9318-1781
    affiliation: 1
  - name: Elliott James Price
    orcid: 0000-0001-5691-7000
    affiliation: 1

affiliations:
 - name: RECETOX, Faculty of Science, Masaryk University, Kotlářská 2, Brno, Czech Republic
   index: 1
date: 11 January 2022
bibliography: paper.bib
 
---

# Summary

MSMetaEnhancer is a Python software package for the metadata enrichment of records in mass spectral library files commonly used as reference for chemical identification via mass spectrometry.
Each record contains spectral information i.e. peak mass to charge ratio (m/z) and intensities, alongside chemical & structural metadata e.g. identifiers.
The package uses matchms [@Huber2020] for data IO and supports the open, text-based `.msp` format.
It annotates given mass spectra records in the library file by adding missing metadata such as SMILES, InChI, and CAS numbers to the individual entries.
The package retrieves the respective information by querying several external databases using existing metadata (e.g., SMILES or CAS number), converting different representations or database identifiers.
Multiple databases and services are included, currently supporting the chemical identifier resolver (CIR), chemical translation service (CTS) [@Wohlgemuth2010], ChemIDplus [@tomasulo2002chemidplus], the Integrated Database for Small Molecules (IDSM) [@galgonek2021idsm], PubChem [@kim2021pubchem], and BridgeDB [@VanIersel2010].
Additionally, instead of querying external databases, computing the identifiers is also supported (e.g. molecular weight from SMILES).

# Statement of need

Mass spectra stored in a library need to be enriched with metadata (e.g chemical formula, SMILES code, InChI, the origin of the spectrum, etc.) to (1) combine spectral and structural information, (2) make the identification process more robust and reproducible, and (3) leverage the interoperability capabilities of chemical databases [@Wallace2017].
While this metadata is mostly accessible from public chemical databases, they are not always present in mass spectral library records.
Therefore, the data needs to be post-processed via enhancement with metadata.
Such a process usually cannot be fully automated, and assistance from the user is required to specify particular annotation steps and sources [@Ausloos1999].
Moreso, manual curation and addition of metadata while creating a compound library is labour intensive and error-prone [@Stravs2013;@Price2021].

# State of the field

There are several packages within Python and R ecosystems which support querying external databases. 
For example, there are R packages that provide an interface to PubChem [@guha2016; @cao2008chemminer], and a package with interface to wikidata [@keys2021]. 
Then, there are packages unifying several sources -- `webchem` [@szocs2020webchem] allows to automatically query chemical data from several web sources (similar to MSMetaEnhancer) and to interconvert between identifiers.
The `MetaFetcheR` [@yones2021metafetcher] package focuses on database-specific identifiers and links metabolite data from several small-compound databases (e.g., PubChem, the Human Metabolome Database (HMDB) [@Wishart2022]), trying to resolve inconsistencies.
Similarly, RaMP cross-references multiple database specific identifiers via their internal RaMP_ID to integrate various pathway and compound databases [@Zhang2018c].
BridgeDb is an ELIXIR project providing mapping functionality of different identifiers present in HMDB (e.g., PubChemCID, ChEBI and InChIKey), gene information and several pathway databases in an organism centric manner, exposing a Java and REST API [@VanIersel2010; @Willighagen2022].

On the Python side, there are packages providing direct API access for PubChem [@swain2017], ChemSpider [@swain2018], or CIR [@swain2016].
PubChem's public API limits programmatic access to less than ~5 requests per second, limiting the ability of advanced users to effectively mine the database.

However, to the best of our knowledge, there is no Python package connecting these sources into a single tool, allowing straightforward metadata annotation of large mass spectral libraries with various identifiers and cross-references to different databases in a user-friendly way.


# The software package

MSMetaEnhancer is a tool to enhance the metadata content of records in mass spectral library files.
It takes as input a single `.msp` file with multiple mass spectra records and a list of annotation steps.
These steps consist of specifying what service should be used to obtain a particular metadata attribute based on another already existing attribute.
To improve the performance of the tool, we use services with high-throughput APIs when available (e.g. IDSM [@galgonek2021idsm], which can be used to access PubChem database).
The supported metadata attributes include InChI, InChIKey, SMILES, IUPAC chemical name, chemical formula, CAS number, and others. 
The particular available conversions can be found in the documentation via https://msmetaenhancer.readthedocs.io/ and are open to extension.
Finally, the obtained metadata are validated to ensure their correct form (currently, `matchms` validators are employed for this task).

![Schematic overview of MSMetaEnhancer annotation workflow. \label{fig:scheme}](scheme.png)

The tool processes the spectral library by iteratively executing all steps for each entry until no new metadata is found. 
This happens for each spectral record in the provided file. 
Since it takes some non-trivial time for the services to respond to a query, this task is suitable for the asynchronous approach, making the tool computationally efficient.
Additionally, results containing all metadata related to a compound are cached, making access to all available metadata for a compound result in only a single query.
For services with limited access rate (i.e., PubChem), we implemented a throttling mechanism -- maximizing performance while mitigating restrictions from the requested webservice.
Besides querying external services, we also support converters to compute identifiers based on existing ones.
For demonstration, we employed computation of molecular weight from SMILES using RDKit [@landrum2006rdkit].
Any issues regarding the annotation process (such as the absence of target data or unavailability of a service) are recorded in a detailed log file, which can be specified as an optional output of the tool.

To improve the usability of the tool, a Galaxy [@galaxy] wrapper was created to provide a user-friendly interface and a simple way of reproducible data processing and analysis.
The tool is hosted on the Galaxy instance available at https://umsa.cerit-sc.cz/, among others [@umsa]. Moreover, the tool is available from bioconda [@bioconda] as a standalone package.

# Example workflow

Performing annotation of a `.msp` file is straightforward and requires to specify services to be used and a list of annotation steps.

```python
import asyncio
from MSMetaEnhancer import Application

app = Application()
# import your .msp file
app.load_spectra('input_spectra_file.msp', file_format='msp')
# specify services
services = ['CIR', 'CTS', 'IDSM']

# specify annotation steps
jobs = [('inchikey', 'inchi', 'CIR'),
        ('inchikey', 'iupac_name', 'CTS'),
        ('inchi', 'canonical_smiles', 'IDSM'),
        ('inchi', 'formula', 'IDSM')]

# run asynchronous annotation of spectra data
asyncio.run(app.annotate_spectra(services, jobs))
# export .msp file
app.save_spectra('annotated_spectra_file.msp', file_format='msp')
```

# Author's Contributions
MT wrote the manuscript and developed the software.
HH contributed to the manuscript and via code reviews and implementation guidance.
MČ contributed via code reviews and implementation guidance.
EJP provided conceptual oversight and contributed to the manuscript.

# Acknowledgements
Authors thank to Research Infrastructure RECETOX RI (No LM2018121) financed by the Ministry of Education, Youth and Sports, and OP RDE project CETOCOEN EXCELLENCE (No CZ.02.1.01/0.0/0.0/17_043/0009632) for supportive background.
EJP was supported from OP RDE - Project \"MSCAfellow4\@MUNI\" (No. CZ.02.2.69/0.0/0.0/20_079/0017045).
This project was supported from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 857560.
This publication reflects only the author’s view and the European Commission is not responsible for any use that may be made of the information it contains

# References
