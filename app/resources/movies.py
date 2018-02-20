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


class MoviesItemResource:
    """Single resource"""

    GET_ITEM_QUERY = """
        SELECT  *
        FROM    movie
        WHERE   id=%(id)s;"""

    def on_get(self, req, resp, id_):
        movie = get_only_result(
            req.cursor,
            self.__class__.GET_ITEM_QUERY,
            {'id': id_})

        if not movie:
            raise falcon.HTTPNotFound()

        resp.status = falcon.HTTP_OK
        resp.media = movie

    UPDATE_MOVIE_QUERY = """
        UPDATE  movie
        SET     title=%(title)s,
                year=%(year)s,
                description=%(description)s
        WHERE   id = %(id)s;"""

    @use_args(request_args)
    def on_put(self, req, resp, args, id_):
        # check to see if exists
        movie = get_only_result(
            req.cursor,
            self.__class__.GET_ITEM_QUERY,
            {'id': id_})

        if not movie:
            raise falcon.HTTPNotFound()

        data = {
            'id': id,
            'title': args['title'],
            'year': args['year'],
            'description': args['description']
        }
        req.cursor.execute(self.__class__.UPDATE_MOVIE_QUERY, data)

        resp.status = falcon.HTTP_OK

    def on_delete(self, req, resp, id_):
        # check to see if exists
        movie = get_only_result(
            req.cursor,
            self.__class__.GET_ITEM_QUERY,
            {'id': id_})

        if not movie:
            raise falcon.HTTPNotFound()


class MoviesCollectionResource:
    """Movie collection"""

    GET_COLLECTION_QUERY = """
        SELECT  *
        FROM    movie;"""

    GET_COLLECTION_PAGINATION_QUERY = """
        SELECT  *
        FROM    movie
        WHERE   id > %(start_with)s;"""

    def on_get(self, req, resp):
        # TODO add pagination
        # what param should we send back to get it working?
        if 'next_record' in req.params:
            pass

        req.cursor.execute(self.__class__.GET_COLLECTION_QUERY)
        movies = req.cursor.fetchall()

        if not movies:
            raise falcon.HTTPNotFound()

        resp.status = falcon.HTTP_OK
        resp.media = movies

    INSERT_MOVIE_QUERY = """
        INSERT INTO     movie(title, year, description)
        VALUE           (%(title)s, %(year)s, %(description)s)"""

    @use_args(request_args)
    def on_post(self, req, resp, args):
        # what happens if we send more than one? try that in the test

        data = req.media
        req.cursor.execute(self.__class__.INSERT_MOVIE_QUERY, data)
        movie_id = req.cursor.lastrowid
        resp.location = '/movies/' + str(movie_id)

        resp.status = falcon.HTTP_CREATED
