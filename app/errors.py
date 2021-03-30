import enum


class Error(enum.Enum):
    NO_FORECAST_DATA = "There is no proper forecast data for the city."
    NO_CITY_NAME = "Can not process with this entry, no city name."
    NO_CONFIG_FILE = "Please, add a .config.yaml file."
