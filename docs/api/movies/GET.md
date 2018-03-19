# Get All Movies

Get all movies currently in the database. Returns a paginated response for the maximum allowed page.

**URL** : `/movies`

**Method** : `GET`

**Auth required** : No

**Permissions required** : None

**Data constraints** : `{}`

**Query Parameters**

|Name|Description|Field Type
|---|---|---|
|`last_id`|Cursor for pagination|Optional

## Success Responses

**Condition** : Returns paginated list of movies.

**Code** : `200 OK`

**Sample Response**

```json
{
    "data": [
        {
            "id": 1,
            "title": "Star Wars: Episode IV",
            "year": 1977,
            "description": "Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee and two droids to save the galaxy from the Empire's world-destroying battle-station while also attempting to rescue Princess Leia from the evil Darth Vader."
        },
        {
            "id": 2,
            "title": "Top Gun",
            "year": 1986,
            "description": "As students at the United States Navy's elite fighter weapons school compete to be best in the class, one daring young pilot learns a few things from a civilian instructor that are not taught in the classroom."
        },
        {
            "id": 3,
            "title": "Moneyball",
            "year": 2011,
            "description": "Oakland A's general manager Billy Beane's successful attempt to assemble a baseball team on a lean budget by employing computer-generated analysis to acquire new players."
        }
    ],
    "last_id": 3,
    "error": ""
}
```
