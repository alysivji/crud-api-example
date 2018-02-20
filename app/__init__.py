import falcon

from .resources.movies import MoviesItemResource, MoviesCollectionResource
from .middleware.database import DatabaseCursor
from .utils.database import database_connection


# import pdb; pdb.set_trace()
app_middleware = [
    DatabaseCursor(database_connection),
]
api = falcon.API(middleware=app_middleware)


# routes
api.add_route('/movies', MoviesCollectionResource())
api.add_route('/movies/{id_:int}', MoviesItemResource())
