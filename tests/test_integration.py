import asyncio
import os

from MSMetaEnhancer import Application
from MSMetaEnhancer.libs.converters.web import CTS, CIR, IDSM, PubChem, BridgeDb
from MSMetaEnhancer.libs.converters.compute import RDKit
from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder

ConverterBuilder.register([CTS, CIR, IDSM, PubChem, BridgeDb, RDKit])

def test_integration(tmp_path):
    app = Application()

    # import your .msp file
    app.load_data('tests/test_data/sample.msp', file_format='msp')

    # curate given metadata (e.g. fix CAS numbers)
    app.curate_metadata()

    # specify requested services (these are supported)
    services = ['CTS', 'CIR', 'IDSM', 'PubChem', 'BridgeDb', 'RDKit']

    # specify requested jobs
    jobs = [('name', 'inchi', 'IDSM'), ('inchi', 'formula', 'IDSM'), ('inchi', 'inchikey', 'IDSM'),
            ('inchi', 'iupac_name', 'IDSM'), ('inchi', 'canonical_smiles', 'IDSM')]

    # run asynchronous annotations of spectra data
    asyncio.run(app.annotate_spectra(services, jobs))

    # export .msp file
    outpath = os.path.join(tmp_path, 'sample_out.msp')
    app.save_data(outpath, file_format='msp')
    assert os.path.isfile(outpath)

    os.remove(outpath)