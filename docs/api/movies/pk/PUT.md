# Update Movie

Update the movie with the provided information

**URL** : `/api/accounts/:pk/`

**URL Parameters** : `pk=[integer]` where `pk` is the ID of the movie in the database

**Method** : `PUT`

**Auth required** : No

**Permissions required** : User is Account Owner

**Data constraints**

```json
{
    "title": string (required),
    "year": int (required),
    "description": string (required)
}
```

**Data example** Partial data is allowed, but there is only one field.

```json
{
    "title": "Top Gun",
    "year": 1986,
    "description": "Greatest movie ever. Watch it."
}
```

## Success Responses

**Condition** : Update can be performed either fully or partially.

**Code** : `200 OK`

**Content example** : For the example above, when the 'description' is updated and posted to `/api/accounts/123/`...

```json
{
    "id": 123,
    "name": "New project name",
    "enterprise": false,
    "url": "http://testserver/api/accounts/123/"
}
```

## Error Response

**Condition** : Movie does not exist at URL

**Code** : `404 NOT FOUND`

**Content** : `{}`
