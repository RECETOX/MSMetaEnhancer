import mock
import pytest
import requests

from MSMetaEnhancer.libs.converters.web import Wikidata
from MSMetaEnhancer.libs.utils.Generic import USER_AGENT
from MSMetaEnhancer.libs.utils.Monitor import Monitor


@pytest.mark.parametrize(
    "status_code, expected",
    [
        (200, True),
        (301, False),
        (403, False),
        (500, False),
    ],
)
def test_check_service_interprets_status_codes(status_code, expected):
    with mock.patch("MSMetaEnhancer.libs.utils.Monitor.requests.get") as get:
        get.return_value = mock.Mock(status_code=status_code)

        assert Monitor.check_service("https://example.org") is expected

    get.assert_called_once_with(
        "https://example.org", timeout=5, headers={"User-Agent": USER_AGENT}
    )


@pytest.mark.parametrize(
    "exception",
    [
        requests.exceptions.ConnectionError,
        requests.exceptions.ReadTimeout,
        TimeoutError,
    ],
)
def test_check_service_handles_request_failures(exception):
    with mock.patch("MSMetaEnhancer.libs.utils.Monitor.requests.get") as get:
        get.side_effect = exception

        assert Monitor.check_service("https://example.org") is False


def test_get_base_url():
    assert Monitor.get_base_url(Wikidata(None)) == "https://query.wikidata.org"

#TODO: add test for run method of Monitor class