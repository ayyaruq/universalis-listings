from piccolo.engine.postgres import PostgresEngine

from piccolo.conf.apps import AppRegistry


DB = PostgresEngine(
    config={
        "database": "universalis",
        "user": "universalis",
        "password": "universalis",
        "host": "localhost",
        "port": 5432,
    }
)

APP_REGISTRY = AppRegistry(
    apps=[
        "listings.piccolo_app",
        "piccolo_admin.piccolo_app"
    ]
)
