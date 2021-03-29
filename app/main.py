import asyncio
import sys
from typing import Any, List, Optional

import aiohttp
import yaml

from app.errors import Error
from app.structures import CityInfo, ResponseData
from app.utils import get_data_from_url_synchronously, logged_method

with open(".config.yaml") as ymlfile:
    config = yaml.safe_load(ymlfile)

AIOHTTP_CLIENT_TIMEOUT = aiohttp.ClientTimeout(total=30)
FORECAST_DAYS = config.get("forecast_days", 2)
WEATHER_API_CODE = config.get("weather_api_code", None)
MUSEMENT_CITIES_ENDPOINT = config.get("musement_cities_endpoint", "https://sandbox.musement.com/api/v3/cities")


def get_url_for_city(city: CityInfo) -> str:
    return (
        f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_CODE}&"
        f"q={city.lat},{city.lon}&days={FORECAST_DAYS}"
    )


async def print_data(response_data: ResponseData):
    if response_data.name:
        text_first_part = f"Processed city {response_data.name}"

        if response_data.error:
            text_second_part = response_data.error
        else:
            try:
                text_second_part = " - ".join(
                    [
                        response_data.json["forecast"]["forecastday"][i]["day"]["condition"]["text"]
                        for i in range(FORECAST_DAYS)
                    ],
                )
            except KeyError:
                text_second_part = Error.NO_FORECAST_DATA.value
            except IndexError:
                text_second_part = Error.NO_FORECAST_DATA.value

        sys.stdout.write(f"{text_first_part} | {text_second_part} \n")


@logged_method()
async def get_data(session: aiohttp.ClientSession, city: CityInfo):
    res: Any = None
    error: Optional[str] = None
    try:
        async with session.get(get_url_for_city(city)) as res:
            res = await res.json()
    except aiohttp.ClientConnectionError as error_message:
        error = str(error_message)
        sys.stdout.write(error)
    except asyncio.TimeoutError as error_message:
        error = str(error_message)
        sys.stdout.write(error)

    await print_data(ResponseData(city.name, res, error))


@logged_method()
async def main(cities: List[CityInfo]) -> None:

    tasks = []
    async with aiohttp.ClientSession(loop=loop, connector=aiohttp.TCPConnector(ssl=False)) as session:
        for city in cities:
            tasks.append(get_data(session, city))
        await asyncio.gather(*tasks)


@logged_method(show_len=True)
def get_cities_info() -> List[CityInfo]:
    cities_raw = get_data_from_url_synchronously(MUSEMENT_CITIES_ENDPOINT)

    cities_info = []
    for city_raw in cities_raw:

        city_info = CityInfo(
            name=city_raw.get("name", None),
            lon=city_raw.get(
                "longitude",
                None,
            ),
            lat=city_raw.get("latitude", None),
        )
        cities_info.append(city_info)

    return cities_info


if __name__ == "__main__":
    urls = get_cities_info()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(urls))
