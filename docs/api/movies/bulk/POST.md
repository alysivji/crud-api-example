# Add List of Movies

Create a movie that will be stored in the database.

**URL** : `/movies/bulk`

**Method** : `POST`

**Auth required** : No

**Permissions required** : None

**Content-type** : `application/json`

**Data constraints**

```json
{
    "data": [
        {
            "title": string (required),
            "year": int (required),
            "description": string (required)
        },

        ...

        {
            "title": string (required),
            "year": int (required),
            "description": string (required)
        }
    ]
}
```

**Data example**

```json
{
    "data": [
        {
            "title": "Monty Python and the Holy Grail",
            "year": 1975,
            "description": "King Arthur and his Knights of the Round Table embark on a surreal, low-budget search for the Holy Grail, encountering many, very silly obstacles."
        },
        {
            "title": "M*A*S*H",
            "year": 1970,
            "description": "The staff of a Korean War field hospital use humor and high jinks to keep their sanity in the face of the horror of war."
        }
    ]
}
```

## Success Response

**Condition** : Movie has been inserted into the database

**Code** : `201 CREATED`

**Headers** : `Location: http://sivserver/movies/123/`

Note: Will return header with id of *last* inserted movie

## Error Responses

**Condition** : If input body is malformed. Errors will describe how to fix.

**Code** : `422 UNPROCESSABLE ENTITY`

**Content example**

```json
{
    "title": "422 Unprocessable Entity",
    "errors": {
        "data": {
            "4": {
                "year": [
                    "Missing data for required field."
                ]
            }
        }
    }
}
```
