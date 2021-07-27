import asyncio
from copy import copy

from app import Application


def test_annotate_MSP_file():
    app = Application()
    app.load_spectra('tests/test_data/sample.msp', file_format='msp')

    app.curate_spectra()
    services = ['PubChem', 'NLM', 'CTS', 'CIR']
    asyncio.run(app.annotate_spectra(services, repeat=True))

    result_spectra = copy(app.spectra)

    app.load_spectra('tests/test_data/sample_out.msp', file_format='msp')

    assert result_spectra == app.spectra
