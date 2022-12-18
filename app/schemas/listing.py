from datetime import datetime
from piccolo.utils.pydantic import create_pydantic_model
from pydantic import BaseModel, ValidationError, validator, conlist

from app.models.listing.tables import Listing


sort_by_slot = lambda x: x['slot_id']


class MateriaModel(BaseModel):
    slot_id: int
    materia_id: int

    def __getitem__(self, item):
        return getattr(self, item)


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
    materia: conlist(MateriaModel, min_items=0, max_items=5)
    unit_price: int
    quantity: int
    retainer: RetainerBase

    @validator('materia')
    def sequential_slots(cls, v):
        sorted_materia = sorted(v, key=sort_by_slot)
        if [x['slot_id'] for x in sorted_materia] != list(range(0, len(v))):
            raise ValidationError("oh fuck")

        return v


# A stripped down listing
class ListingSummary(ListingBase):
    last_upload_time: datetime
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
    last_review_time: datetime

    def __getitem__(self, item):
        return getattr(self, item)

    @validator('last_review_time', pre=True)
    def epoch_to_datetime(cls, v):
        return datetime.fromtimestamp(v)


    class Config:
        json_encoders = {
            datetime: lambda v: int(v.timestamp()),
        }
        json_decoders = {
            datetime: lambda v: datetime.fromtimestamp(v),
        }
