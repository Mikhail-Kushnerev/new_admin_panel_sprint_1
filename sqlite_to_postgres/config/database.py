import os

from dotenv import load_dotenv

load_dotenv()


dsl = {
    'postgres': {
        'dbname': os.getenv('POSTGRES_DB', default='postgres'),
        'user': os.getenv('POSTGRES_USER', default='postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', default='postgres'),
        'host': os.getenv('POSTGRES_HOST', default='127.0.0.1'),
        'port': os.getenv('POSTGRES_PORT', default=5432)
    },
    'sqlite': {
        'dbname': os.getenv('ORIGINAL_DB', default='sqlite.db')
    }
}
