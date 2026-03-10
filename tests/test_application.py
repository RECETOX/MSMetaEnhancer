import asyncio
import pytest

from MSMetaEnhancer import Application
from MSMetaEnhancer.libs.converters.web import IDSM, PubChem
from MSMetaEnhancer.libs.utils.ConverterBuilder import ConverterBuilder
from tests.utils import FakeMonitor, FakeAnnotator
from MSMetaEnhancer.libs.utils.Generic import is_na_value


def test_annotate_spectra_monitor_stops():
    app = Application()
    monitor = FakeMonitor()
    annotator = FakeAnnotator()

    app.load_data("tests/test_data/sample.msp", file_format="msp")

    asyncio.run(app.annotate_spectra([], monitor=monitor, annotator=annotator))
    assert monitor.stop_request.is_set()


def test_annotate_spectra_monitor_stops_after_exception():
    app = Application()
    monitor = FakeMonitor()
    annotator = FakeAnnotator(True)

    app.load_data("tests/test_data/sample.msp", file_format="msp")

    with pytest.raises(Exception):
        asyncio.run(app.annotate_spectra({}, monitor=monitor, annotator=annotator))

    assert monitor.stop_request.is_set()


def test_application_sparse():
    ConverterBuilder.register([PubChem, IDSM])
    app = Application()
    app.load_data("tests/test_data/sparse.tsv", file_format="tabular")
    asyncio.run(app.annotate_spectra(["PubChem", "IDSM"]))

    actual = [x.get("canonical_smiles") for x in app.data.get_metadata()]
    assert not any([is_na_value(x) for x in actual])
