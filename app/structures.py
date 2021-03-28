from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class CityInfo:
    name: str
    lon: float
    lat: float


@dataclass
class ResponseData:
    name: Optional[str]
    json: Any
    error: Optional[str]
