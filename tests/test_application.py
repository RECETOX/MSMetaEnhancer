import asyncio
import pytest

from MSMetaEnhancer import Application
from tests.utils import FakeMonitor, FakeAnnotator


def test_annotate_spectra_monitor_stops():
    app = Application()
    monitor = FakeMonitor()
    annotator = FakeAnnotator()

    app.load_spectra('tests/test_data/sample.msp', file_format='msp')

    asyncio.run(app.annotate_spectra([], monitor=monitor, annotator=annotator))
    assert monitor.stop_request.is_set()


def test_annotate_spectra_monitor_stops_after_exception():
    app = Application()
    monitor = FakeMonitor()
    annotator = FakeAnnotator(True)

    app.load_spectra('tests/test_data/sample.msp', file_format='msp')

    with pytest.raises(Exception):
        asyncio.run(app.annotate_spectra([], monitor=monitor, annotator=annotator))

    assert monitor.stop_request.is_set()
