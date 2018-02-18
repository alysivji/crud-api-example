import mysql.connector as mysqldb
from urllib.parse import urlparse
from app.config import DATABASE_URL


def database_connection(db_url=DATABASE_URL):
    parsed = urlparse(db_url)
    user = parsed.username
    password = parsed.password
    host = parsed.hostname
    port = parsed.port
    database = parsed.path.strip('/')

    config = {
        'host': host,
        'port': port,
        'user': user,
        'password': password,
        'database': database,
        'use_unicode': True,
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_general_ci',
        'autocommit': True,
    }

    connection = mysqldb.connect(**config)

    return connection
