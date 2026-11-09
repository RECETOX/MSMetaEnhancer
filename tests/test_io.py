import pytest
import mock

from MSMetaEnhancer import Application
from MSMetaEnhancer.libs.data import Spectra, DataFrame, MzTabM


DATA = [
    {
        "formula": "H2",
        "mw": "2",
        "casno": "1333740",
        "id": "1",
        "num_peaks": "2",
        "compound_name": "Dihydrogen",
    },
    {
        "formula": "D2",
        "mw": "4",
        "casno": "7782390",
        "id": "2",
        "num_peaks": "2",
        "compound_name": "Dideuterium",
    },
    {
        "formula": "CH4",
        "mw": "16",
        "casno": "74828",
        "id": "3",
        "num_peaks": "6",
        "compound_name": "Methane",
    },
]


@pytest.mark.parametrize(
    "backend, file_type, filename",
    [
        [Spectra(), "msp", "tests/test_data/sample.msp"],
        [Spectra(), "mgf", "tests/test_data/sample.mgf"],
        [Spectra(), "json", "tests/test_data/sample.json"],
        [DataFrame(), "csv", "tests/test_data/sample_metadata.csv"],
        [DataFrame(), "tsv", "tests/test_data/sample_metadata.tsv"],
        [DataFrame(), "xlsx", "tests/test_data/sample_metadata.xlsx"],
    ],
)
def test_get_metadata(backend, file_type, filename):
    backend.load_data(filename, file_type)
    metadata = backend.get_metadata()

    # Compare lengths
    assert len(metadata) == len(DATA), (
        f"Metadata length mismatch: {len(metadata)} != {len(DATA)}"
    )

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
    for i, (fused_row, original_row) in enumerate(
        zip(df.df.to_dict(orient="records"), DATA)
    ):
        for key in original_row.keys():
            if key in fused_row:
                assert fused_row[key] == original_row[key], (
                    f"Value mismatch for key '{key}' at row {i}: {fused_row[key]} != {original_row[key]}"
                )


def test_fuse_metadata_spectra():
    spectra_fused = Spectra()
    spectra_fused.spectrums = [
        mock.Mock(metadata=dict()),
        mock.Mock(metadata=dict()),
        mock.Mock(metadata=dict()),
    ]
    spectra_fused.fuse_metadata(DATA)

    spectra_loaded = Spectra()
    spectra_loaded.load_data("tests/test_data/sample.msp", "msp")

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
    filename = "tests/test_data/sample_metadata.tsv"
    file_type = "tabular"
    df.load_data(filename, file_type)
    metadata = df.get_metadata()

    # Compare lengths
    assert len(metadata) == len(DATA), (
        f"Metadata length mismatch: {len(metadata)} != {len(DATA)}"
    )
    # Compare values of matching keys
    for i, (meta_item, data_item) in enumerate(zip(metadata, DATA)):
        for key in meta_item.keys():
            if key in data_item:
                assert meta_item[key] == data_item[key], (
                    f"Value mismatch for key '{key}' at index {i}: {meta_item[key]} != {data_item[key]}"
                )


def test_mztab_m_metadata_roundtrip(tmp_path):
    filename = tmp_path / "sample.mztab"
    filename.write_text(
        "MTD\tmzTab-version\t2.0.0-M\n"
        "SMH\tidentifier\tchemical_formula\tsmiles\tinchi\tinchi_key\tchemical_name\n"
        "SML\tHMDB:HMDB0000001\tCH4\tC\tInChI=1S/CH4/h1H4\tVNWKTOKETHGBQD-UHFFFAOYSA-N\tMethane\n"
        "SML\tnull\tC2H6\tnull\tnull\tnull\tEthane\n",
        encoding="utf-8",
    )

    backend = MzTabM()
    backend.load_data(filename, "mztab-m")
    metadata = backend.get_metadata()

    assert metadata == [
        {
            "identifier": "HMDB:HMDB0000001",
            "formula": "CH4",
            "smiles": "C",
            "inchi": "InChI=1S/CH4/h1H4",
            "inchikey": "VNWKTOKETHGBQD-UHFFFAOYSA-N",
            "compound_name": "Methane",
        },
        {"formula": "C2H6", "compound_name": "Ethane"},
    ]

    metadata[0]["casno"] = "74-82-8"
    backend.fuse_metadata(metadata)
    backend.save_data(filename)

    reloaded = MzTabM()
    reloaded.load_data(filename)
    assert reloaded.get_metadata()[0]["casno"] == "74-82-8"
    assert "opt_casno" in reloaded.header
    assert len(reloaded.get_metadata()) == 2


def test_application_loads_mztab_m(tmp_path):
    filename = tmp_path / "sample.mztab"
    filename.write_text(
        "SMH\tchemical_name\nSML\tMethane\n",
        encoding="utf-8",
    )

    app = Application()
    app.load_data(filename, file_format="mztab-m")

    assert isinstance(app.data, MzTabM)
    assert app.data.get_metadata() == [{"compound_name": "Methane"}]


@pytest.mark.parametrize(
    "backend, file_type, filename, absent_keys",
    [
        [
            DataFrame(),
            "csv",
            "tests/test_data/sample_metadata_with_na.csv",
            ["inchikey", "smiles"],
        ],
        [
            Spectra(),
            "msp",
            "tests/test_data/sample_with_na.msp",
            ["inchikey", "smiles"],
        ],
    ],
)
def test_na_values_filtered_from_metadata(backend, file_type, filename, absent_keys):
    """NA and empty values in data files should be excluded from metadata dicts."""
    backend.load_data(filename, file_type)
    metadata = backend.get_metadata()

    assert len(metadata) == 3

    for i, meta_item in enumerate(metadata):
        # Keys that had NA values must be absent
        for key in absent_keys:
            assert key not in meta_item, (
                f"NA key '{key}' should not be present at index {i}, got {meta_item.get(key)}"
            )
