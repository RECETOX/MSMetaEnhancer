import pytest
import pandas
import mock

from MSMetaEnhancer.libs.data import Spectra, DataFrame


DATA = [{'formula': 'H2', 'mw': '2', 'casno': '1333740', 'id': '1', 'num_peaks': '2', 'compound_name': 'Hydrogen'},
        {'formula': 'D2', 'mw': '4', 'casno': '7782390', 'id': '2', 'num_peaks': '2', 'compound_name': 'Deuterium'},
        {'formula': 'CH4', 'mw': '16', 'casno': '74828', 'id': '3', 'num_peaks': '6', 'compound_name': 'Methane'}]


@pytest.mark.parametrize('backend, file_type, filename', [
    [Spectra(), 'msp', 'tests/test_data/sample.msp'],
    [DataFrame(), 'csv', 'tests/test_data/sample_metadata.csv'],
    [DataFrame(), 'tsv', 'tests/test_data/sample_metadata.tsv'],
    [DataFrame(), 'xlsx', 'tests/test_data/sample_metadata.xlsx']
])
def test_get_metadata(backend, file_type, filename):
    backend.load_data(filename, file_type)
    assert backend.get_metadata() == DATA


def test_fuse_metadata_dataframe():
    pandas_df = pandas.read_csv('tests/test_data/sample_metadata.csv', dtype=str)
    df = DataFrame()
    df.fuse_metadata(DATA)
    assert pandas_df.equals(df.df)


def test_fuse_metadata_spectra():
    spectra_fused = Spectra()
    spectra_fused.spectrums = [mock.Mock(metadata=dict()), mock.Mock(metadata=dict()), mock.Mock(metadata=dict())]
    spectra_fused.fuse_metadata(DATA)

    spectra_loaded = Spectra()
    spectra_loaded.load_data('tests/test_data/sample.msp', 'msp')

    assert spectra_fused.get_metadata() == spectra_loaded.get_metadata()
