from fastapi import FastAPI
from piccolo_admin.endpoints import create_admin
from piccolo.engine import engine_finder


from routers import listing, character, retainer


app = FastAPI()

# Load our discrete Endpoints
app.include_router(
    listing.router,
    tags=["Listings"]
)

# These might be better with Piccolo's auto CRUD
app.include_router(character.router, prefix="/character")
app.include_router(retainer.router, prefix="/retainer")

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
