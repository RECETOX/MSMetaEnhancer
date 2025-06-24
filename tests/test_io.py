import pytest
import mock

from MSMetaEnhancer.libs.data import Spectra, DataFrame


DATA = [{'formula': 'H2', 'mw': '2', 'casno': '1333740', 'id': '1', 'num_peaks': '2', 'compound_name': 'Hydrogen'},
        {'formula': 'D2', 'mw': '4', 'casno': '7782390', 'id': '2', 'num_peaks': '2', 'compound_name': 'Deuterium'},
        {'formula': 'CH4', 'mw': '16', 'casno': '74828', 'id': '3', 'num_peaks': '6', 'compound_name': 'Methane'}]


@pytest.mark.parametrize('backend, file_type, filename', [
    [Spectra(), 'msp', 'tests/test_data/sample.msp'],
    [Spectra(), 'mgf', 'tests/test_data/sample.mgf'],
    [Spectra(), 'json', 'tests/test_data/sample.json'],
    [DataFrame(), 'csv', 'tests/test_data/sample_metadata.csv'],
    [DataFrame(), 'tsv', 'tests/test_data/sample_metadata.tsv'],
    [DataFrame(), 'xlsx', 'tests/test_data/sample_metadata.xlsx']
])
def test_get_metadata(backend, file_type, filename):
    backend.load_data(filename, file_type)
    metadata = backend.get_metadata()

    # Compare lengths
    assert len(metadata) == len(DATA), f"Metadata length mismatch: {len(metadata)} != {len(DATA)}"

    # Compare values of matching keys
    for i, (meta_item, data_item) in enumerate(zip(metadata, DATA)):
        for key in meta_item.keys():
            if key in data_item:
                assert meta_item[key] == data_item[key], (
                    f"Value mismatch for key '{key}' at index {i}: {meta_item[key]} != {data_item[key]}"
                )

def test_fuse_metadata_dataframe():
    df = DataFrame()
    df.fuse_metadata(DATA)
    # Compare row by row, ignoring mismatched keys
    for i, (fused_row, original_row) in enumerate(zip(df.df.to_dict(orient='records'), DATA)):
        for key in original_row.keys():
            if key in fused_row:
                assert fused_row[key] == original_row[key], (
                    f"Value mismatch for key '{key}' at row {i}: {fused_row[key]} != {original_row[key]}"
                )


def test_fuse_metadata_spectra():
    spectra_fused = Spectra()
    spectra_fused.spectrums = [mock.Mock(metadata=dict()), mock.Mock(metadata=dict()), mock.Mock(metadata=dict())]
    spectra_fused.fuse_metadata(DATA)

    spectra_loaded = Spectra()
    spectra_loaded.load_data('tests/test_data/sample.msp', 'msp')

    # Compare metadata row by row, ignoring mismatched keys
    fused_metadata = spectra_fused.get_metadata()
    loaded_metadata = spectra_loaded.get_metadata()

    for i, (fused_item, loaded_item) in enumerate(zip(fused_metadata, loaded_metadata)):
        for key in loaded_item.keys():
            if key in fused_item:
                assert fused_item[key] == loaded_item[key], (
                    f"Value mismatch for key '{key}' at index {i}: {fused_item[key]} != {loaded_item[key]}"
                )


def test_tabular_data():
    """
    Test loading and comparing tabular (TSV) data using the DataFrame backend.
    """
    df = DataFrame()
    filename = 'tests/test_data/sample_metadata.tsv'
    file_type = 'tabular'
    df.load_data(filename, file_type)
    metadata = df.get_metadata()

    # Compare lengths
    assert len(metadata) == len(DATA), f"Metadata length mismatch: {len(metadata)} != {len(DATA)}"
    # Compare values of matching keys
    for i, (meta_item, data_item) in enumerate(zip(metadata, DATA)):
        for key in meta_item.keys():
            if key in data_item:
                assert meta_item[key] == data_item[key], (
                    f"Value mismatch for key '{key}' at index {i}: {meta_item[key]} != {data_item[key]}"
                )
