import falcon
from webargs import fields
from webargs.falconparser import use_args

# Done
# Create
#   * collection
#       * only updates 1
#       * TODO create /movies/bulk endpoint
#           * do we send back location header or locations in body?
# Read
#   * collection: 200;
#       * Pagination should be set up via page and implemented with index and
#         offset behind the scenes
#   * item: 200 or 404
# Update
#   * collection: PUT and PATCH not allowed
#   * item: PUT allowed, PATCH not allowed. what if item
# Delete
#   * collection: DELETE not allowed
#   * item: delete item, return something in response body or 404
#       * ASK CHRIS


def get_only_result(cursor, query, params):
    """Given cursor, query, and params, return item"""
    cursor.execute(query, params)
    return cursor.fetchone()


request_args = {
    'id': fields.Int(location='json'),
    'title': fields.String(location='json'),
    'year': fields.Int(location='json'),
    'description': fields.String(location='json'),
}

bulk_request_args = {
    'data': fields.List(
        fields.Nested({
            'title': fields.String(location='json'),
            'year': fields.Int(location='json'),
            'description': fields.String(location='json'),
        })
    )
}

# queries
DELETE_MOVIE_QUERY = """
    DELETE FROM     movie
    WHERE           id=%(id)s"""

GET_COLLECTION_PAGINATION_QUERY = """
    SELECT  *
    FROM    movie
    WHERE   id > %(start_with)s;"""

GET_COLLECTION_QUERY = """
    SELECT  *
    FROM    movie;"""

GET_ITEM_QUERY = """
    SELECT  *
    FROM    movie
    WHERE   id=%(id)s;"""

INSERT_MOVIE_QUERY = """
    INSERT INTO     movie(title, year, description)
    VALUE           (%(title)s, %(year)s, %(description)s)"""

UPDATE_MOVIE_QUERY = """
    UPDATE  movie
    SET     title=%(title)s,
            year=%(year)s,
            description=%(description)s
    WHERE   id=%(id)s;"""


class MoviesItemResource:
    """Single resource"""

    def on_get(self, req, resp, id_):
        movie = get_only_result(req.cursor, GET_ITEM_QUERY, {'id': id_})

        if not movie:
            raise falcon.HTTPNotFound()

        resp.status = falcon.HTTP_OK
        resp.media = movie

    @use_args(request_args)
    def on_put(self, req, resp, args, id_):
        # check to see if exists
        movie = get_only_result(req.cursor, GET_ITEM_QUERY, {'id': id_})

        if not movie:
            raise falcon.HTTPNotFound()

        try:
            data = {
                'id': id_,
                'title': args['title'],
                'year': args['year'],
                'description': args['description'],
            }
        except KeyError:
            raise falcon.HTTPBadRequest()

        req.cursor.execute(UPDATE_MOVIE_QUERY, data)
        resp.status = falcon.HTTP_OK

    def on_delete(self, req, resp, id_):
        # check to see if exists
        movie = get_only_result(req.cursor, GET_ITEM_QUERY, {'id': id_})

        if not movie:
            raise falcon.HTTPNotFound()

        req.cursor.execute(DELETE_MOVIE_QUERY, {'id': id_})
        resp.status = falcon.HTTP_OK


class MoviesCollectionResource:
    """Movie collection"""

    def on_get(self, req, resp):
        # TODO add pagination
        # use page=2 and limit and offset in the backend
        # what param should we send back to get it working?
        if 'next_record' in req.params:
            pass

        req.cursor.execute(GET_COLLECTION_QUERY)
        movies = req.cursor.fetchall()

        if not movies:
            raise falcon.HTTPNotFound()

        resp.status = falcon.HTTP_OK
        resp.media = movies

    @use_args(request_args)
    def on_post(self, req, resp, args):
        try:
            data = {
                'title': args['title'],
                'year': args['year'],
                'description': args['description'],
            }
        except KeyError:
            raise falcon.HTTPBadRequest()

        req.cursor.execute(INSERT_MOVIE_QUERY, data)

        movie_id = req.cursor.lastrowid
        resp.location = '/movies/' + str(movie_id)
        resp.status = falcon.HTTP_CREATED


class MoviesBulkAddResource:
    """Movies Bulk Add Resource"""
    # TODO this might be a place to use Marshmallow, look into usecases

    @use_args(bulk_request_args)
    def on_post(self, req, resp, args):
        try:
            movies = args['data']
        except KeyError:
            raise falcon.HTTPBadRequest()

        # TODO: should we do a try here?
        req.cursor.executemany(INSERT_MOVIE_QUERY, movies)

        movie_id = req.cursor.lastrowid
        resp.location = '/movies/' + str(movie_id)
        resp.status = falcon.HTTP_CREATED
