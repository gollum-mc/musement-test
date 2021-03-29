# Step 2 | API design

### Forecast as endpoint
I would recommend creation of a new `/api/v3/forecasts` endpoint for GET and POST methods ans maybe other in the future. 
I rejected the nested endpoints solution basing on `/api/v3/cities` endpoint (`GET /api/v3/cities/{id}/forecast?day=2021-03-27`) 
even though at the first glance it looks more logical, as the forecast constitutes the element of the city 
resources and it is related to the city.
I assumed that the weather forecast is a significant feature (for example for a mobile app) and can be accessed for 
many cities for one user, so, the extracted forecast endpoint, detached from the city will save web resources.
Moreover, there's a possibility that in the future there will be a nid to update or delete forecasts and it will be 
just easier and more efficient to access it via `/api/v3/forecasts` endpoint.
What's more, many development tools allow to save much time via automated creation of model-based endpoints 
while it is not easy to automate the creation of nested endpoints.

## Endpoint to set the forecast for a specific city

Endpoint:
```
POST /api/v3/forecasts
```
Request json body structure:
```
{
"city_id": int,
"date": str,
"text": str
}
```
Sample request body:
```
{
"city_id": 2,
"date": 2021-03-20,
"text": "Partly cloudly"
}
```
Response json body structure:


```
{
"id": int,
"city_id": int,
"date": str,
"text": str
}
```


Sample response, HTTP CODE 200:

```
{
"id": 10,
"city_id": 2,
"date": 2021-03-20,
"text": "Partly cloudly"
}

```

Sample response, HTTP CODE 400:

```
{
"error": 
    {
    "message": "There is no such city.",
    "code": 234,
    "parameter": "city_id"
    }
}

```
Request payload

| element                    | description                 | required         | type / format      |
|:-----------------------------|:----------------------------|:-----------------|:-------------------|
| `city_id`                    |id of a city from `cities` endpoint | True | integer
| `date`| date of the weather forecast | True | string / YYYY-MM-DD
| `text`                   | weather forecast content | True | string / 2 - 200 characters

## Endpoint to read the forecast for a specific city

Endpoint:
```
GET /api/v3/forecasts
```
Request URL structure:
```
GET /api/v3/forecasts?city_ids=[city_id,city_id]&date_from=[YYYY-MM_DD]&date_to=[YYYY-MM-DD]
```
Sample request url:
```
GET /api/v3/forecasts?city_ids=1,67,90&date_from=2021-03-21&date_to=2021-03-25
```
Response json body structure:


```
{
"forecasts": [
    {
    "id": int,
    "city_id": int,
    "city_name": str,
    "date": str,
    "text": str
    },
    {
    "id": int,
    "city_id": int,
    "city_name": str,
    "date": str,
    "text": str
    }
]
}
```


Sample response, HTTP CODE 200:

```
{
"forecasts": [
    {
    "id": 10,
    "city_id": 2,
    "city_name": "Warsaw",
    "date": "2021-03-21",
    "text": "Heavy rain"
    },
    {
    "id": 11,
    "city_id": 2,
    "city_name": "Warsaw",
    "date": "2021-03-22",
    "text": "Sunny"
    }
]
}

```

Sample response, HTTP CODE 400:

```
{
"error": 
    {
    "message": "Wrong date format, required: YYYY-MM-DD.",
    "code": 345,
    "parameter": null
    }
}

```
Request query params

| parameter                    | description                 | required         | format             |
|:-----------------------------|:----------------------------|:-----------------|:-------------------|
| `city_ids`                   |coma separated list of city ids | True | integer
| `date_from`| start date of the weather forecast, default today | False | YYYY-MM-DD
| `date_to`| end date of the weather forecast, required when `date_to` set to a specific value | False | YYYY-MM-DD

## Musement API resources

| resource      | description                       |
|:--------------|:----------------------------------|
| `/cities`      | returns a list of all cities 
| `/forecasts`    | returns a list of all forecasts for the given day, default - today



