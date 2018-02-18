class DatabaseCursor(object):

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def process_request(self, req, resp):

        if req is not None:
            req.db = self.db_conn()
            req.cursor = req.db.cursor(dictionary=True)

    def process_response(self, req, resp, resource, req_succeeded):
        if hasattr(req, 'cursor'):
            req.cursor.close()
        if hasattr(req, 'db'):
            req.db.close()
