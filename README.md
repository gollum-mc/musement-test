# Musement-test

A powerful tool for fast and resource-saving weather data processing. The app presents the weather data for 
all cities listed under Musement api endpoint:

``` 
GET https://sandbox.musement.com/api/v3/cities
```
The app works only with the WeatherAPI (see [https://www.weatherapi.com/][Weather API]):
```
GET http://api.weatherapi.com/v1/forecast.json?key=[WEATHER_API_CODE]&q=[city.lat],[city.lon]&days=[FORECAST_DAYS]
```

You'll get printed to the console all results for cities in the format below:

```
Processed city <CITY> | <weather forecast text for today> - <weather forecast text for tomorrow>
```

In case of technical issues a proper error messages will be printed.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and 
testing purposes as well as instructions for docker deployment.

### Prerequisites

- The app requires Python 3.8 and Docker
- Remember about filling in the `.config.yaml` file with your WeatherApi code - you can find the 
  blueprint as `.config_.yaml`, remember to rename it to `.config.yaml`

### Installing

Make sure you have a docker installed

go into the project folder

```
cd <name of the project>
```

clone project repository
```
git clone https://Gollum_mc@bitbucket.org/Gollum_mc/load-time-controller.git
```

build a docker image - make sure you do not set the detached mode as it you will not be able to see the results 
printed out to the console
```
docker build -t musement .
```

run the container - and that's it! Enjoy!
```
docker run musement
```

### Development
For development purposes use the `requirements-dev.txt` dependencies. 
Feel free to modify `pre-commit-config.yaml` by setting your own tool, however base tool are ready to use.

## Authors

* **Marta Chludzińska**


[Weather API]: https://www.weatherapi.com/my/upgrade.aspx