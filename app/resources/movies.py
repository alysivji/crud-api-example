import falcon


class MoviesCollectionResource:
    GET_COLLECTION_QUERY = """
        SELECT  *
        FROM    movie"""

    ADD_MOVIE_QUERY = """
        INSERT INTO     movie(title, year, description)
        VALUE           (%(title)s, %(year)s, %(description)s)"""

    def on_get(self, req, resp):
        req.cursor.execute(self.__class__.GET_COLLECTION_QUERY)
        movies = req.cursor.fetchall()

        if not movies:
            raise falcon.HTTPNotFound()

        resp.status = falcon.HTTP_OK
        resp.media = movies

    def on_post(self, req, resp):
        data = req.media
        req.cursor.execute(self.__class__.ADD_MOVIE_QUERY, data)
        movie_id = req.cursor.lastrowid
        resp.location = '/movies/' + str(movie_id)

        resp.status = falcon.HTTP_CREATED


class MoviesResource:
    GET_ITEM_QUERY = """
        SELECT  *
        FROM    movie
        WHERE   id=%(id)s"""

    def on_get(self, req, resp, id):
        req.cursor.execute(
            self.__class__.GET_ITEM_QUERY,
            {'id': id})
        movie = req.cursor.fetchone()

        if not movie:
            raise falcon.HTTPNotFound()

        resp.status = falcon.HTTP_OK
        resp.media = movie
