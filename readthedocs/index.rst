Welcome to pyMSPannotator's documentation!
==========================================

**pyMSPannotator** is a tool used for `.msp` files annotation.
It supports four services: CIR, CTS, NLM, and PubChem.
The app uses asynchronous implementation of annotation process,
benefiting from non-trivial amount of time spent by waiting for a web query response.

.. note::

   This project is under active development.

Contents
========

.. toctree::

   API <api.rst>

Installation
============

Prerequisites:

- Python 3.7 or 3.8
- Anaconda

Install `pyMSPannotator` from Bioconda with

.. code-block:: console

  # install pyMSPannotator in a new virtual environment to avoid dependency clashes
  conda create --name pyMSPannotator python=3.8
  conda activate pyMSPannotator
  conda install --channel bioconda --channel conda-forge pyMSPannotator

Example
=======

.. testcode::
    import asyncio
    from pyMSPannotator.app import Application

    app = Application()

    # import your .msp file
    app.load_spectra('tests/test_data/sample.msp', file_format='msp')

    # curate given metadata (e.g. fix CAS numbers)
    app.curate_spectra()

    # specify requested services (these are supported)
    services = ['CTS', 'CIR', 'NLM', 'PubChem']

    # specify requested jobs
    jobs = [('name', 'inchi', 'PubChem'),
            ('inchi', 'formula', 'PubChem'),
            ('inchi', 'inchikey', 'PubChem'),
            ('inchi', 'iupac_name', 'PubChem'),
            ('inchi', 'smiles', 'PubChem')]

    # run asynchronous annotations of spectra data
    asyncio.run(app.annotate_spectra(services, jobs))

    # alternatively, execute without jobs parameter to run all possible jobs
    asyncio.run(app.annotate_spectra(services))

    # export .msp file
    app.save_spectra('tests/test_data/sample_out.msp', file_format='msp')

