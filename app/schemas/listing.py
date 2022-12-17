import json
from piccolo.utils.pydantic import create_pydantic_model
from pydantic import BaseModel, Json, ValidationError, validator

from app.models.listing.tables import Listing


class MateriaModel(BaseModel):
    slot_id: int
    materia_id: int


class NamePairModel(BaseModel):
    name: str
    id: int

class CharacterBase(NamePairModel):
    pass


class RetainerBase(NamePairModel):
    city: int


# A single listing, with char+retainer expanded
ListingModel = create_pydantic_model(Listing, nested=True)


class ListingBase(BaseModel):
    listing_id: str
    world_id: int
    item_id: int
    hq: bool
    materia: list[MateriaModel]
    unit_price: int
    quantity: int
    retainer: RetainerBase


# A stripped down listing
class ListingSummary(ListingBase):
    last_upload_time: int
    creator: CharacterBase | None


# Query params for filtering responses
class ListingFilter(BaseModel):
    world_id: int
    dc_id: int
    region_id: int


# The listing upload
class ListingIn(ListingBase):
    uploader_id: str
    seller_id: str
    creator: CharacterBase | None
    on_mannequin: bool
    dye_id: int
    last_review_time: int
