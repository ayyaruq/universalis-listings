from fastapi import FastAPI
from piccolo_admin.endpoints import create_admin
from piccolo_api.fastapi.endpoints import FastAPIWrapper, FastAPIKwargs
from piccolo_api.crud.endpoints import PiccoloCRUD
from piccolo.engine import engine_finder

from app.api.routes import listing, character, retainer
from app.models.listing.tables import Character, Retainer
from app.models.listing.piccolo_app import APP_CONFIG


app = FastAPI()

# Load our discrete Endpoints
app.include_router(listing.router)

FastAPIWrapper(
    root_url="/character/",
    fastapi_app=app,
    fastapi_kwargs=FastAPIKwargs(
        all_routes={'tags': ["Character"]},
    ),
    piccolo_crud=PiccoloCRUD(
        table=Character,
        read_only=True,
    )
)

FastAPIWrapper(
    root_url="/retainer/",
    fastapi_app=app,
    fastapi_kwargs=FastAPIKwargs(
        all_routes={'tags': ["Retainer"]},
    ),
    piccolo_crud=PiccoloCRUD(
        table=Retainer,
        read_only=True,
    )
)

# Load admin dashboard
app.mount("/admin", create_admin(
    tables=APP_CONFIG.table_classes,
    # Required when running under HTTPS:
    # allowed_hosts=['my_site.com']
    )
)


@app.on_event("startup")
async def open_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.start_connection_pool()
    except Exception:
        print("Unable to connect to the database")


@app.on_event("shutdown")
async def close_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.close_connection_pool()
    except Exception:
        print("Unable to connect to the database")
