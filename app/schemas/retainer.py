from piccolo.utils.pydantic import create_pydantic_model

from app.models.listing.tables import Retainer

RetainerModel = create_pydantic_model(Retainer)
