import sys
from io import StringIO

import aiohttp
import pytest

from app import main
from app.structures import CityInfo, ResponseData


@pytest.fixture(autouse=True)
def session_get_mocked():
    return {
        "name": "Kalorama Triangle",
        "forecast": {
            "forecastday": [
                {
                    "date": "2021-03-26",
                    "day": {
                        "condition": {
                            "text": "Patchy rain possible",
                        },
                    },
                },
                {
                    "date": "2021-03-27",
                    "day": {
                        "condition": {
                            "text": "Partly cloudy",
                        },
                    },
                },
            ]
        },
    }


@pytest.fixture(autouse=True)
def get_city_info():
    return CityInfo(name="Warsaw", lon=56.9, lat=78.1)


class TestMain:
    class ClientSession:
        pass

    @pytest.mark.asyncio
    async def test_get_data(self, monkeypatch, session_get_mocked):

        captured_output = StringIO()
        sys.stdout = captured_output

        monkeypatch.setattr(aiohttp.ClientSession(), "get", session_get_mocked)
        monkeypatch.setattr(aiohttp.ClientResponse, "json", session_get_mocked)

        await main.print_data(ResponseData(name="Kalorama Triangle", json=session_get_mocked, error=None))

        sys.stdout = sys.__stdout__
        assert (
            captured_output.getvalue() == "Processed city Kalorama Triangle | "
            "Patchy rain possible - Partly cloudy \n"
        )

    @pytest.mark.asyncio
    async def test_get_data_connection_error(self, monkeypatch, get_city_info):
        async def session_get_mocked_error(*_):
            raise aiohttp.ClientConnectionError("Connection issue")

        captured_output = StringIO()
        sys.stdout = captured_output

        monkeypatch.setattr(aiohttp.ClientSession(), "get", session_get_mocked_error)
        monkeypatch.setattr(aiohttp.ClientResponse, "json", session_get_mocked_error)

        await main.get_data(aiohttp.ClientSession(), get_city_info)
        sys.stdout = sys.__stdout__
        assert ("Connection issue" in captured_output.getvalue()) is True

    def test_get_cities_info(self, monkeypatch):
        def mocked_get_data_from_url(*_):
            return [
                {"name": "Warsaw", "lon": 45.55, "lat": 567.0},
                {"name": "Cracow", "lon": 45.55, "lat": 567.0},
                {"name": "Sopot", "lon": 45.55, "lat": 567.0},
            ]

        monkeypatch.setattr(main, "get_data_from_url_synchronously", mocked_get_data_from_url)

        cities_info = main.get_cities_info()
        assert type(cities_info) == list
        assert len(cities_info) == len(mocked_get_data_from_url())
        assert cities_info[0].__class__ == CityInfo
        assert cities_info[-1].name == "Sopot"

    def test_get_url_for_city(self, get_city_info):

        city_info = get_city_info
        url = main.get_url_for_city(city_info)
        assert url is not None
        assert type(url) == str
        assert ("56.9" in url) is True
        assert ("78.1" in url) is True
