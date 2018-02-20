import falcon

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
    cursor.execute(query, params)
    return cursor.fetchone()


class MoviesItemResource:
    GET_ITEM_QUERY = """
        SELECT  *
        FROM    movie
        WHERE   id=%(id)s"""

    def on_get(self, req, resp, id):
        movie = get_only_result(
            req.cursor,
            self.__class__.GET_ITEM_QUERY,
            {'id': id})

        if not movie:
            raise falcon.HTTPNotFound()

        resp.status = falcon.HTTP_OK
        resp.media = movie

    def on_put(self, req, resp, id):
        # check to see if exists
        movie = get_only_result(
            req.cursor,
            self.__class__.GET_ITEM_QUERY,
            {'id': id})

        if not movie:
            raise falcon.HTTPNotFound()

        # if it exists update everything
        pass

    def on_delete(self, req, resp, id):
        # should we check to see if it exists before deleting? try it
        pass


class MoviesCollectionResource:
    GET_COLLECTION_QUERY = """
        SELECT  *
        FROM    movie"""

    GET_COLLECTION_PAGINATION_QUERY = """
        SELECT  *
        FROM    movie
        WHERE   id > %(start_with)s"""

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

    ADD_MOVIE_QUERY = """
        INSERT INTO     movie(title, year, description)
        VALUE           (%(title)s, %(year)s, %(description)s)"""

    # What about posting more than one?
    def on_post(self, req, resp):
        data = req.media
        req.cursor.execute(self.__class__.ADD_MOVIE_QUERY, data)
        movie_id = req.cursor.lastrowid
        resp.location = '/movies/' + str(movie_id)

        resp.status = falcon.HTTP_CREATED
