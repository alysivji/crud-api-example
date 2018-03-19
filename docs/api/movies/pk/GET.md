# Get Movies

Get a single movie from the database.

**URL** : `/movies/:pk`

**URL Parameters** : `pk=[integer]` where `pk` is the ID of the movie in the database

**Method** : `GET`

**Auth required** : No

**Permissions required** : None

**Data constraints** : `{}`

## Success Responses

**Condition** : Movie exists in the database.

**Code** : `200 OK`

**Sample Response**

```json
{
    "data": {
        "id": 2,
        "title": "Top Gun",
        "year": 1986,
        "description": "As students at the United States Navy's elite fighter weapons school compete to be best in the class, one daring young pilot learns a few things from a civilian instructor that are not taught in the classroom."
    },
    "error": ""
}
```

## Error Responses

**Condition** : If movie does not exist with `id` of provided `pk` parameter.

**Code** : `404 NOT FOUND`

**Content** : `{}`
