import os

DATABASE_URL = os.getenv('DATABASE_URL', 'mysql://sivpack:sivpack_dev@db:3306/sivdev')
