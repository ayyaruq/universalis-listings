from piccolo.utils.pydantic import create_pydantic_model

from app.models.listing.tables import Character

CharacterModel = create_pydantic_model(Character)
