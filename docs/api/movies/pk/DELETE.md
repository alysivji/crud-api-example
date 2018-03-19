# Delete Movie

Delete movie from the database

**URL** : `/movies/:pk/`

**URL Parameters** : `pk=[integer]` where `pk` is the ID of the Movie in the
database.

**Method** : `DELETE`

**Auth required** : No

**Permissions required** : None

**Data** : `{}`

## Success Response

**Condition** : If the movie exists and is deleted.

**Code** : `204 NO CONTENT`

**Content** : `{}`

## Error Responses

**Condition** : If there was no movie with that id.

**Code** : `404 NOT FOUND`

**Content** : `{}`
