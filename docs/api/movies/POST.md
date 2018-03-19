# Add Movie

Create a movie that will be stored in the database.

**URL** : `/movies`

**Method** : `POST`

**Auth required** : No

**Permissions required** : None

**Content-type** : `application/json`

**Data constraints**

```json
{
    "title": string (required),
    "year": int (required),
    "description": string (required)
}
```

**Data example**

```json
{
    "title": "Return of the Jedi",
    "year": 1985,
    "description": "Chewie meets Ewoks."
}
```

## Success Response

**Condition** : Movie has been inserted into the database

**Code** : `201 CREATED`

**Headers** : `Location: http://sivserver/movies/123/`

## Error Responses

**Condition** : If input body is malformed. Errors will describe how to fix.

**Code** : `422 UNPROCESSABLE ENTITY`

**Content example**

```json
{
    "title": "422 Unprocessable Entity",
    "errors": {
        "title": [
            "Not a valid string."
        ]
    }
}
```
